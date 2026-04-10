# Lab L4c: Diagnose and Fix a Slow Trino/Iceberg Query

## Goal
Start with a slow `SELECT` against an Iceberg table backed by 10 000 tiny Parquet files, diagnose it with `EXPLAIN ANALYZE`, compact with `rewrite_data_files`, and measure a 10–100× wall-time improvement.

## Prerequisites
- Phase 3 full-stack compose up and healthy: MinIO, Trino, Spark, Iceberg, HMS (`phase_3_core_tools/compose/full-stack/docker-compose.yml`).
- `uv` on PATH ([uv install](https://docs.astral.sh/uv/getting-started/installation/)).
- `mc` (MinIO client) or the MinIO console to inspect bucket contents.
- Trino CLI or any Trino client (DBeaver, `trino` CLI, `trino-python-client`).

## Setup
Bring the stack up and create the bucket + MinIO alias. All following commands assume the stack's default credentials — adjust if yours differ.

```bash
cd phase_3_core_tools/compose/full-stack
docker compose up -d
docker compose ps  # confirm trino, spark, minio, hms, postgres are (healthy)

mc alias set local http://localhost:9000 minio minio123
mc mb --ignore-existing local/lakehouse
```

Generate the pathological dataset — 10 000 000 rows across 10 000 tiny Parquet files:

```bash
cd phase_4_specializations/05_performance_tuning/labs/lab_L4c_perf_tuning
uv run python generate_data.py
```

When the generator finishes it prints the bucket path, total file count, and average file size. Expect ~10 000 files, each around a few hundred KB.

## Steps

**1. Inspect the raw files.** Confirm the deliberately bad layout before touching Trino.

```bash
mc ls --recursive local/lakehouse/perf_lab/raw_events/ | wc -l
mc du local/lakehouse/perf_lab/raw_events/
```
Expected: `10000` (or close to it), and a human-readable total size under 1 GB.

**2. Register an Iceberg table over the files.** In the Trino CLI:

```sql
CREATE SCHEMA IF NOT EXISTS iceberg.perf_lab WITH (location = 's3a://lakehouse/perf_lab/');

CREATE TABLE iceberg.perf_lab.events (
    event_id   BIGINT,
    event_date DATE,
    user_id    BIGINT,
    amount     DOUBLE
)
WITH (
    format = 'PARQUET',
    location = 's3a://lakehouse/perf_lab/events/'
);
```
Then load the generated Parquet into the Iceberg table with an `INSERT ... SELECT` from the Hive external pointer, *or* register them directly using `system.register_table` / `migrate` (engine-dependent). A portable approach: use Spark (`spark-sql` shell in the stack) to bulk-append the generated Parquet into the Iceberg table.

```sql
-- In spark-sql:
CREATE TEMP VIEW raw USING parquet OPTIONS (path 's3a://lakehouse/perf_lab/raw_events/');
INSERT INTO iceberg.perf_lab.events SELECT event_id, event_date, user_id, amount FROM raw;
```

**3. Time the slow query.** In the Trino CLI, enable timing and run a filter that *should* be cheap:

```sql
-- Trino: \timing on
SELECT count(*), avg(amount)
FROM iceberg.perf_lab.events
WHERE event_date = DATE '2024-06-15';
```
Record the wall time. On a laptop with 10 000 tiny files and no partitioning, expect tens of seconds.

**4. Read the plan with EXPLAIN ANALYZE.**

```sql
EXPLAIN ANALYZE
SELECT count(*), avg(amount)
FROM iceberg.perf_lab.events
WHERE event_date = DATE '2024-06-15';
```
You should see a `ScanFilterProject` (or Iceberg table scan) stage reporting an input close to all 10 million rows and thousands of splits. That is the symptom: no pruning, many small files, per-file overhead dominates. Reference: [Trino EXPLAIN ANALYZE](https://trino.io/docs/current/sql/explain-analyze.html).

**5. Compact with Iceberg `rewrite_data_files`.** In Trino's Iceberg connector the equivalent is `ALTER TABLE ... EXECUTE optimize` ([Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)):

```sql
ALTER TABLE iceberg.perf_lab.events EXECUTE optimize(file_size_threshold => '256MB');
```
Or via Spark ([Iceberg Spark procedures](https://iceberg.apache.org/docs/latest/spark-procedures/#rewrite_data_files)):

```sql
-- spark-sql:
CALL iceberg.system.rewrite_data_files(table => 'perf_lab.events');
```

**6. Re-time the same query.**

```sql
SELECT count(*), avg(amount)
FROM iceberg.perf_lab.events
WHERE event_date = DATE '2024-06-15';
```
Record the new wall time. Expect a 10–100× improvement driven by far fewer splits and better IO batching.

**7. Re-run EXPLAIN ANALYZE.** Confirm the split / input-file count dropped from thousands to tens, and CPU time dropped accordingly.

**8. Expire snapshots to reclaim storage.** The old tiny files are still referenced by the pre-compaction snapshot and therefore still on disk ([Iceberg — Expire Snapshots](https://iceberg.apache.org/docs/latest/maintenance/#expire-snapshots)). Retain only the most recent snapshot:

```sql
-- spark-sql:
CALL iceberg.system.expire_snapshots(
  table => 'perf_lab.events',
  older_than => TIMESTAMP '9999-12-31 00:00:00',
  retain_last => 1
);
```
Re-run `mc du local/lakehouse/perf_lab/` and confirm the footprint dropped.

## Verify
- [ ] Wall time of the filter query drops at least 10× between step 3 and step 6.
- [ ] `EXPLAIN ANALYZE` input-split count drops from ~10 000 to a small number (tens).
- [ ] `mc ls --recursive local/lakehouse/perf_lab/events/data/ | wc -l` returns fewer files after compaction + expire than before.
- [ ] You can describe, in one sentence each, *why* each of the four things you changed (compaction, snapshot expiry, partitioning in the stretch goal) mattered.

## Cleanup
```bash
# Drop the table and schema
# trino:
DROP TABLE iceberg.perf_lab.events;
DROP SCHEMA iceberg.perf_lab;

# Then clear the bucket
mc rm --recursive --force local/lakehouse/perf_lab/

# Optional: bring the stack down
cd phase_3_core_tools/compose/full-stack && docker compose down
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `uv run` fails with missing `pyarrow` | The script declares inline dependencies via `# /// script`; upgrade `uv` to the latest and retry |
| `CreateBucketFailed` | Create the bucket first with `mc mb local/lakehouse` |
| Trino cannot see the table after the Spark insert | Refresh the catalog: `CALL iceberg.system.register_table(...)` or reconnect the CLI |
| `rewrite_data_files` returns quickly with no change | Files already above the threshold; lower `file_size_threshold` or rewrite all |
| Storage unchanged after compaction | You did not expire snapshots yet — old snapshot still references the old files |

## Stretch goals
- **Add partitioning.** Recreate the table with `PARTITIONED BY (days(event_date))`, regenerate the data into the partitioned layout (modify `generate_data.py` to write one file per date), and re-time the filter query. Compare to the compacted-but-unpartitioned result. The partition-pruned plan should touch a single file.
- **Skew probe.** Re-run the query with a `GROUP BY user_id` where 1% of `user_id`s hold 90% of rows (the generator has a `--skew` flag). Observe skew in the Trino query UI or Spark stage view. Try Spark with AQE off vs. on (`spark.sql.adaptive.enabled`) and measure the difference. Reference: [Spark — Optimizing Skew Join](https://spark.apache.org/docs/latest/sql-performance-tuning.html#optimizing-skew-join).
- **Broadcast join.** Create a 1000-row `dim_user` table, join it against `events`, and use `EXPLAIN ANALYZE` to confirm the dimension is broadcast not shuffled.

## References
See `../../references.md` (module-level).
