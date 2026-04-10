# Lab 03: NYC Taxi SQL — Window Functions, EXPLAIN, Indexes

## Goal
Load a NYC TLC Yellow Taxi sample into PostgreSQL, write five window-function queries, run `EXPLAIN ANALYZE` on one, add an index, and compare the before/after plans.

## Prerequisites
- Lab L1 completed — `postgres` from `04_docker/labs/lab_L1_compose_healthcheck` is running and healthy
- `psql` client (installed on the host or accessed via `docker exec`)
- ~50 MB free disk
- A NYC TLC Yellow Taxi CSV sample of ~50k rows. The NYC TLC publishes monthly trip-record files; the canonical landing page is [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). Recent months are distributed as Parquet; for a lab CSV, either convert a Parquet file with DuckDB or ship a local `yellow_sample.csv` with the columns used below.

## Setup

Open a psql shell against the lab container:

```bash
docker exec -it lab-postgres-1 psql -U "${POSTGRES_USER:-lab}" -d "${POSTGRES_DB:-lab}"
```

Create the table and load the CSV. [`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) is the fastest bulk loader:

```sql
CREATE TABLE yellow_trips (
  vendor_id            smallint,
  tpep_pickup_datetime timestamp NOT NULL,
  tpep_dropoff_datetime timestamp NOT NULL,
  passenger_count      smallint,
  trip_distance        numeric(8,2),
  pu_location_id       integer,
  do_location_id       integer,
  fare_amount          numeric(10,2),
  tip_amount           numeric(10,2),
  total_amount         numeric(10,2)
);

\copy yellow_trips FROM 'yellow_sample.csv' WITH (FORMAT csv, HEADER true);
ANALYZE yellow_trips;
SELECT count(*) FROM yellow_trips;
```
Expected output:
```
 count
-------
 50000
(1 row)
```

## Steps

1. **Ranking — top 5 pickup zones by trip count per day.** Uses `ROW_NUMBER` over a partition ([window functions](https://www.postgresql.org/docs/current/functions-window.html)).
   ```sql
   WITH daily AS (
     SELECT tpep_pickup_datetime::date AS day,
            pu_location_id,
            count(*) AS trips
     FROM yellow_trips
     GROUP BY 1, 2
   )
   SELECT day, pu_location_id, trips
   FROM (
     SELECT day, pu_location_id, trips,
            ROW_NUMBER() OVER (PARTITION BY day ORDER BY trips DESC) AS rn
     FROM daily
   ) t
   WHERE rn <= 5
   ORDER BY day, rn;
   ```

2. **7-day rolling revenue per pickup zone.** Explicit `ROWS BETWEEN` frame ([window function calls](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)).
   ```sql
   WITH daily AS (
     SELECT tpep_pickup_datetime::date AS day,
            pu_location_id,
            sum(total_amount) AS revenue
     FROM yellow_trips
     GROUP BY 1, 2
   )
   SELECT day, pu_location_id, revenue,
          SUM(revenue) OVER (
            PARTITION BY pu_location_id
            ORDER BY day
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
          ) AS rolling_7d_revenue
   FROM daily
   ORDER BY pu_location_id, day;
   ```

3. **Day-over-day delta with `LAG`.**
   ```sql
   WITH daily AS (
     SELECT tpep_pickup_datetime::date AS day,
            count(*) AS trips
     FROM yellow_trips
     GROUP BY 1
   )
   SELECT day, trips,
          trips - LAG(trips) OVER (ORDER BY day) AS delta_trips
   FROM daily
   ORDER BY day;
   ```

4. **Percentile bucket of fares with `NTILE(10)`.**
   ```sql
   SELECT pu_location_id,
          fare_amount,
          NTILE(10) OVER (ORDER BY fare_amount) AS fare_decile
   FROM yellow_trips
   WHERE fare_amount > 0
   LIMIT 20;
   ```

5. **`DENSE_RANK` — busiest hour of day.**
   ```sql
   SELECT extract(hour FROM tpep_pickup_datetime)::int AS hour,
          count(*) AS trips,
          DENSE_RANK() OVER (ORDER BY count(*) DESC) AS busy_rank
   FROM yellow_trips
   GROUP BY 1
   ORDER BY busy_rank;
   ```

6. **Baseline `EXPLAIN ANALYZE` on a selective time filter.** See [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html).
   ```sql
   EXPLAIN ANALYZE
   SELECT count(*), sum(total_amount)
   FROM yellow_trips
   WHERE tpep_pickup_datetime >= '2024-01-15 00:00:00'
     AND tpep_pickup_datetime <  '2024-01-16 00:00:00';
   ```
   Expected (abridged) — note the `Seq Scan`:
   ```
   Aggregate  (cost=... rows=1 ...) (actual time=42.1..42.1 rows=1 loops=1)
     ->  Seq Scan on yellow_trips  (cost=... rows=... ) (actual time=... rows=... loops=1)
           Filter: ((tpep_pickup_datetime >= ...) AND (tpep_pickup_datetime < ...))
           Rows Removed by Filter: ...
   Planning Time: ...
   Execution Time: 42.5 ms
   ```

7. **Add a B-tree index and refresh stats.** See [Indexes](https://www.postgresql.org/docs/current/indexes.html).
   ```sql
   CREATE INDEX idx_yellow_trips_pickup ON yellow_trips (tpep_pickup_datetime);
   ANALYZE yellow_trips;
   ```

8. **Re-run the same `EXPLAIN ANALYZE`.** Expected — `Index Scan` or `Bitmap Index Scan` replaces `Seq Scan` and `Execution Time` drops:
   ```
   Aggregate  ... (actual time=3.2..3.2 rows=1 loops=1)
     ->  Index Scan using idx_yellow_trips_pickup on yellow_trips ...
           Index Cond: ((tpep_pickup_datetime >= ...) AND (tpep_pickup_datetime < ...))
   Planning Time: ...
   Execution Time: 3.5 ms
   ```
   Exact numbers vary by machine and sample — the qualitative change (`Seq Scan` → `Index Scan`, lower `Execution Time`) is the verifiable outcome.

## Verify
- [ ] All five analytical queries return rows without error
- [ ] Query 6's first `EXPLAIN ANALYZE` shows `Seq Scan on yellow_trips`
- [ ] Query 8's second `EXPLAIN ANALYZE` shows `Index Scan` (or `Bitmap Index Scan`) using `idx_yellow_trips_pickup` and a lower `Execution Time`
- [ ] `\d yellow_trips` lists the new index

## Cleanup
```sql
DROP INDEX IF EXISTS idx_yellow_trips_pickup;
DROP TABLE IF EXISTS yellow_trips;
\q
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `\copy` error "could not open file" | Run `\copy` (client-side) not `COPY` (server-side); file path is relative to the psql host |
| `EXPLAIN` still shows `Seq Scan` after index | Filter too wide (planner thinks seq scan is cheaper) — narrow the time range |
| Estimated vs actual row counts very different | Run `ANALYZE yellow_trips;` |
| `COPY` slow | Drop indexes before load, `CREATE INDEX` after — the pattern used here |

## Stretch goals
- Add a multicolumn index `(pu_location_id, tpep_pickup_datetime)` and compare with query 2's plan. See [multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html).
- Create a **partial index** for weekend trips only and measure its size with `pg_relation_size`. See [partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html).
- Enable `pg_stat_statements` (`CREATE EXTENSION pg_stat_statements;` after adding `shared_preload_libraries='pg_stat_statements'` in postgres config), run all five queries, and rank them by `total_exec_time`. See [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html).

## References
See `../../references.md` (module-level).
