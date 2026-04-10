
# Lab L3c: dbt models against Trino + Iceberg

## Goal
Scaffold a dbt project with the `dbt-trino` adapter, build a staging → intermediate → mart DAG on top of the `raw_taxi.yellow_taxi_trips` source landed by the dlt lab, add generic and singular tests, and green `dbt build` end-to-end — with verification via a Trino SQL query.

## Prerequisites
- Phase 3 full-stack compose running: `phase_3_core_tools/compose/full-stack/docker-compose.yml` (MinIO + HMS + Trino).
- Lab `L3b_dlt_ingest` completed so that `iceberg.bronze.yellow_taxi_trips` exists.
- Python 3.11+ and `pip`.

## Setup
```bash
cd phase_3_core_tools/05_dbt/labs/lab_L3c_dbt_models

python -m venv .venv && source .venv/bin/activate
pip install 'dbt-core==1.8.*' 'dbt-trino==1.8.*'

# Profile: copy the example and keep secrets out of the project dir.
mkdir -p ~/.dbt
cp profiles.yml.example ~/.dbt/profiles.yml

# Sanity check: does the adapter find Trino?
dbt debug --project-dir . --profiles-dir ~/.dbt
```
Expected tail:
```
All checks passed!
```

## Steps
1. Inspect the project layout.
   ```bash
   tree -L 3 .
   ```
   You should see `dbt_project.yml`, `models/staging/stg_taxi_trips.sql`, `models/intermediate/int_taxi_hourly.sql`, `models/marts/fct_taxi_hourly.sql`, `models/schema.yml`, and `tests/assert_nonneg_trip_count.sql`.

2. Parse + compile (no SQL executes yet):
   ```bash
   dbt parse --project-dir . --profiles-dir ~/.dbt
   dbt compile --project-dir . --profiles-dir ~/.dbt --select stg_taxi_trips
   cat target/compiled/lakehouse_l3c/models/staging/stg_taxi_trips.sql
   ```
   Confirm the compiled SQL references `iceberg.bronze.yellow_taxi_trips`.

3. Build the DAG:
   ```bash
   dbt build --project-dir . --profiles-dir ~/.dbt
   ```
   Expected tail (numbers will differ):
   ```
   Completed successfully
   Done. PASS=6 WARN=0 ERROR=0 SKIP=0 TOTAL=6
   ```
   The six nodes are three models plus three tests (`unique` and `not_null` on the mart key, plus the singular test).

4. Verify via Trino:
   ```bash
   docker exec -it lh_trino trino --catalog iceberg --schema gold \
     --execute "select pickup_hour, trip_count from fct_taxi_hourly order by trip_count desc limit 5;"
   ```
   You should see five rows with non-zero `trip_count`.

5. Prove the singular test can fail. Temporarily break it:
   ```bash
   dbt test --select assert_nonneg_trip_count --project-dir . --profiles-dir ~/.dbt --vars '{force_fail: true}'
   ```
   (Only works if you add the `{% if var('force_fail', false) %}` branch — stretch goal.) Otherwise, inject a bad row via Trino, rerun `dbt test`, see the failure, then clean it up.

## Verify
- [ ] `dbt debug` returns "All checks passed".
- [ ] `dbt build` ends with `PASS=6 WARN=0 ERROR=0 SKIP=0`.
- [ ] `iceberg.silver.stg_taxi_trips`, `iceberg.silver.int_taxi_hourly`, `iceberg.gold.fct_taxi_hourly` are queryable from Trino.
- [ ] The `unique` test on `fct_taxi_hourly.pickup_hour` passes.
- [ ] The singular test `assert_nonneg_trip_count` runs and passes.

## Cleanup
```bash
docker exec -it lh_trino trino --catalog iceberg --execute "drop schema if exists silver cascade; drop schema if exists gold cascade;"
deactivate && rm -rf .venv target dbt_packages logs
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `dbt debug` fails with `Connection refused` | Trino not up — `docker compose ps` in `compose/full-stack/`, then retry. |
| `Relation 'iceberg.bronze.yellow_taxi_trips' does not exist` | Run lab `L3b_dlt_ingest` first to land the source. |
| `AttributeError` on adapter first call | `dbt-core` and `dbt-trino` minor versions drifted; re-pin to the same minor. |
| `unique` test fails on `pickup_hour` | Aggregation lost a `group by` key; check `int_taxi_hourly`. |

## Stretch goals
- Add `{{ config(properties={'format': "'PARQUET'"}) }}` to `fct_taxi_hourly` and inspect the resulting files in MinIO.
- Add a `relationships` test from `int_taxi_hourly.vendor_id` to a seed vendor table.
- Wire `dbt source freshness` against `raw_taxi.yellow_taxi_trips` using `_dlt_load_id` (pattern: `../dataeng/dbt_project/models/sources.yml:L10-L17`).

## References
See `../../references.md` (module-level).
