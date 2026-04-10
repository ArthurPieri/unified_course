# Lab L2: Star Schema + SCD Type 2 in PostgreSQL

## Goal
Design and load a `dim_customer` (SCD Type 2) + `fct_orders` star schema in PostgreSQL, then answer "revenue per customer as of date X" with a point-in-time query.

## Prerequisites
- Docker installed ([docker run reference](https://docs.docker.com/reference/cli/docker/container/run/))
- Familiarity with `psql` and SQL DDL ([PostgreSQL CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html))
- Completed `phase_1_foundations/05_sql_postgres/` (reuses the same Postgres container pattern)

## Setup
Start a Postgres container (same image used in Phase 1 lab L1):

```bash
docker run -d --name pg-l2 \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16

# wait for readiness, then connect
docker exec -it pg-l2 psql -U postgres
```

## Steps

**1. Create dimensions and fact.** `dim_customer` is SCD2 — a single `customer_id` may have multiple rows distinguished by `[valid_from, valid_to)`, of which exactly one has `is_current = true`. `customer_sk` is the surrogate key the fact references.

```sql
CREATE TABLE dim_customer (
    customer_sk   bigserial PRIMARY KEY,
    customer_id   int         NOT NULL,        -- natural/business key
    customer_name text        NOT NULL,
    address       text        NOT NULL,
    region        text        NOT NULL,
    valid_from    timestamp   NOT NULL,
    valid_to      timestamp,                   -- NULL = still current
    is_current    boolean     NOT NULL
);

CREATE INDEX ix_dim_customer_bk ON dim_customer (customer_id, valid_from);

CREATE TABLE dim_date (
    date_sk  int  PRIMARY KEY,   -- yyyymmdd
    full_date date NOT NULL UNIQUE,
    year     int  NOT NULL,
    month    int  NOT NULL,
    day      int  NOT NULL
);

CREATE TABLE fct_orders (
    order_sk      bigserial PRIMARY KEY,
    order_id      int       NOT NULL,
    customer_sk   bigint    NOT NULL REFERENCES dim_customer(customer_sk),
    order_date_sk int       NOT NULL REFERENCES dim_date(date_sk),
    order_ts      timestamp NOT NULL,          -- event timestamp for point-in-time joins
    revenue       numeric(12,2) NOT NULL CHECK (revenue >= 0)
);
```
Reference star-schema shape: `../../../../../dataeng/dbt_project/models/marts/dim_zones.sql:L7-L18` (denormalized dimension) and `../../../../../dataeng/dbt_project/models/marts/fct_trip_metrics.sql:L9-L23` (fact with declared grain).

**2. Seed `dim_date` and an initial customer row.**

```sql
INSERT INTO dim_date (date_sk, full_date, year, month, day) VALUES
  (20250101, DATE '2025-01-01', 2025, 1, 1),
  (20250201, DATE '2025-02-01', 2025, 2, 1),
  (20250301, DATE '2025-03-01', 2025, 3, 1);

INSERT INTO dim_customer (customer_id, customer_name, address, region, valid_from, valid_to, is_current)
VALUES (42, 'Ada Lovelace', '1 Babbage St, London', 'EMEA',
        TIMESTAMP '2025-01-01 00:00:00', NULL, true);
```

**3. Insert orders that reference the current SCD2 row.**

```sql
INSERT INTO fct_orders (order_id, customer_sk, order_date_sk, order_ts, revenue)
SELECT 1001, c.customer_sk, 20250101, TIMESTAMP '2025-01-15 10:00:00', 120.00
FROM dim_customer c WHERE c.customer_id = 42 AND c.is_current;

INSERT INTO fct_orders (order_id, customer_sk, order_date_sk, order_ts, revenue)
SELECT 1002, c.customer_sk, 20250201, TIMESTAMP '2025-02-10 14:30:00', 80.00
FROM dim_customer c WHERE c.customer_id = 42 AND c.is_current;
```

**4. Customer 42 moves. Apply an SCD2 update — close the old row and insert the new row in one transaction.**

```sql
BEGIN;

UPDATE dim_customer
SET valid_to   = TIMESTAMP '2025-02-15 00:00:00',
    is_current = false
WHERE customer_id = 42 AND is_current;

INSERT INTO dim_customer (customer_id, customer_name, address, region, valid_from, valid_to, is_current)
VALUES (42, 'Ada Lovelace', '10 Downing St, London', 'EMEA',
        TIMESTAMP '2025-02-15 00:00:00', NULL, true);

COMMIT;
```

SCD2 trade-offs and the `valid_from`/`valid_to`/`is_current` pattern: *Kimball DW Toolkit, Ch. 5*. dbt's `snapshot` with `strategy='timestamp'` does the same thing automatically — see `../../../../../dataeng/dbt_project/snapshots/snap_taxi_zones.sql:L1-L25`.

**5. Insert a post-move order. It must reference the new surrogate key.**

```sql
INSERT INTO fct_orders (order_id, customer_sk, order_date_sk, order_ts, revenue)
SELECT 1003, c.customer_sk, 20250301, TIMESTAMP '2025-03-05 09:15:00', 200.00
FROM dim_customer c WHERE c.customer_id = 42 AND c.is_current;
```

**6. Point-in-time query — "what was customer 42's revenue and address as of 2025-02-01?"**

```sql
SELECT c.customer_id, c.address, c.region, SUM(f.revenue) AS revenue
FROM fct_orders f
JOIN dim_customer c ON c.customer_sk = f.customer_sk
WHERE c.customer_id = 42
  AND f.order_ts <= TIMESTAMP '2025-02-01 23:59:59'
  AND c.valid_from <= TIMESTAMP '2025-02-01 23:59:59'
  AND (c.valid_to IS NULL OR c.valid_to > TIMESTAMP '2025-02-01 23:59:59')
GROUP BY c.customer_id, c.address, c.region;
```
Expected: address = `1 Babbage St, London`, revenue = `120.00`.

**7. Current-state query.**

```sql
SELECT c.customer_id, c.address, SUM(f.revenue) AS revenue_total
FROM fct_orders f
JOIN dim_customer c ON c.customer_sk = f.customer_sk
WHERE c.customer_id = 42 AND c.is_current
GROUP BY c.customer_id, c.address;
```
Expected: address = `10 Downing St, London`, revenue_total = `200.00` (only the order tied to the new surrogate key).

## Verify
- [ ] `SELECT count(*) FROM dim_customer WHERE customer_id = 42;` returns `2`.
- [ ] Exactly one row for customer 42 has `is_current = true` and `valid_to IS NULL`.
- [ ] The point-in-time query returns `1 Babbage St, London`.
- [ ] The current-state query returns `10 Downing St, London`.
- [ ] All `fct_orders.customer_sk` values exist in `dim_customer.customer_sk` (FK holds).

## Cleanup
```bash
docker rm -f pg-l2
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `ERROR: insert or update on table "fct_orders" violates foreign key` | The `SELECT … WHERE is_current` returned zero rows — you forgot to insert the new SCD2 row before the post-move order |
| Two rows with `is_current = true` for the same `customer_id` | The `UPDATE` in step 4 was skipped; re-run the transaction or assert `COUNT(*) FILTER (WHERE is_current) = 1` per business key |
| Point-in-time query returns duplicated rows | Missing upper-bound predicate on `valid_to`; add `(valid_to IS NULL OR valid_to > :as_of)` |
| `psql: connection refused` | Container still starting — wait 2–3 seconds and retry, or `docker logs pg-l2` |

## Stretch goals
- Add a Type 3 `prior_region` column to `dim_customer`. On each SCD2 update, copy the outgoing `region` into the new row's `prior_region`. Write a query that returns customers whose region changed. *Kimball DW Toolkit, Ch. 5*.
- Add a `dim_product` and extend `fct_orders` to line-item grain (`order_id`, `product_sk`). Re-declare the grain before writing the DDL.
- Simulate a late-arriving fact: insert an order with `order_ts = '2025-01-20'` *after* the SCD2 update in step 4, and verify your point-in-time join still picks the original address.

## References
See `../../references.md` (module-level).
