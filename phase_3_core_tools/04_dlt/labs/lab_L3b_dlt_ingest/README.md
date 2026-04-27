# Lab L3b: Ingest NYC Taxi Parquet with dlt

## Goal
Use a dlt pipeline to ingest NYC Yellow Taxi Parquet files from the public TLC HTTP source into MinIO as an Iceberg table, using an incremental cursor on `tpep_pickup_datetime`, and verify the load with a Trino `SELECT count(*)`.

## Prerequisites
- Phase 3 full-stack compose running: `phase_3_core_tools/compose/full-stack/`
- `uv` or `pip` with Python 3.11+
- `dlt[filesystem]>=1.4` installed in the local venv
- Trino CLI or any JDBC client on `localhost:8080`

## Setup
```bash
cd phase_3_core_tools/compose/full-stack
cp .env.example .env
docker compose up -d minio hive-metastore trino
# Wait for health
docker compose ps

# Create the target bucket
docker compose exec minio \
  mc alias set local http://localhost:9000 minioadmin minioadmin
docker compose exec minio mc mb -p local/lakehouse || true

# Python env for the pipeline
cd ../../04_dlt/labs/lab_L3b_dlt_ingest
uv venv && source .venv/bin/activate
uv pip install 'dlt[filesystem]>=1.4' pyarrow

# MinIO credentials for dlt's filesystem destination
export DESTINATION__FILESYSTEM__BUCKET_URL=s3://lakehouse
export DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID=minioadmin
export DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY=minioadmin
export DESTINATION__FILESYSTEM__CREDENTIALS__ENDPOINT_URL=http://localhost:9000
```

## Steps
1. Run the pipeline for January 2024.
   ```bash
   python pipeline.py --year 2024 --months 1
   ```
   Expected tail:
   ```
   Load package 17... is LOADED and contains no failed jobs
   ```

2. Register an Iceberg table in Trino over the Parquet that dlt wrote.
   ```bash
   docker compose exec -T trino trino --execute "
   CREATE SCHEMA IF NOT EXISTS iceberg.yellow_taxi
     WITH (location = 's3://lakehouse/yellow_taxi');
   CREATE TABLE IF NOT EXISTS iceberg.yellow_taxi.trips
   WITH (format = 'PARQUET', location = 's3://lakehouse/yellow_taxi/yellow_taxi_trips')
   AS SELECT * FROM hive.yellow_taxi.yellow_taxi_trips;
   "
   ```

3. Verify the row count.
   ```bash
   docker compose exec -T trino trino --execute \
     "SELECT count(*) FROM iceberg.yellow_taxi.trips;"
   ```
   Expected: a count in the ~3M range for a single month.

4. Re-run the pipeline to prove incrementality.
   ```bash
   python pipeline.py --year 2024 --months 1
   ```
   Expected: `load_info` shows 0 new rows — the incremental cursor filtered them.

5. Extend the cursor. Load February:
   ```bash
   python pipeline.py --year 2024 --months 2
   ```
   The row count in Trino should now reflect Jan + Feb.

## Verify
- [ ] `mc ls local/lakehouse/yellow_taxi/yellow_taxi_trips/` shows Parquet files.
- [ ] Trino `SELECT count(*)` returns > 0 and increases after step 5.
- [ ] A second identical run (step 4) prints no new load packages with data.
- [ ] `~/.dlt/pipelines/nyc_taxi_lab/state.json` exists and references `tpep_pickup_datetime`.

## Cleanup
```bash
rm -rf ~/.dlt/pipelines/nyc_taxi_lab
docker compose exec minio mc rb --force local/lakehouse || true
docker compose down
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `InvalidAccessKeyId` on load | Re-export the `DESTINATION__FILESYSTEM__CREDENTIALS__*` env vars in the same shell. |
| `Could not connect to endpoint` | `ENDPOINT_URL` must be `http://localhost:9000` from the host; `http://minio:9000` only inside the compose network. |
| Trino count stays at 0 after re-run | Cursor is working as intended; bump `--months` to load new data. |
| `SchemaCorruptedException` | Upstream column added; the resource already sets `schema_contract="evolve"` — confirm you are on dlt ≥ 1.4. |

## Stretch goals
- Swap the filesystem destination for `destination="iceberg"` and configure a PyIceberg catalog against the lab HMS at `thrift://localhost:9083`. See [dlt — Iceberg destination](https://dlthub.com/docs/dlt-ecosystem/destinations/iceberg).
- Add a second resource for a taxi zones lookup and group both under one `@dlt.source`. See [dlt — Sources](https://dlthub.com/docs/general-usage/source).
- Wire the pipeline as a Dagster asset (forward reference to Module 06) using the `dagster-dlt` integration. See [Dagster — dagster-dlt](https://docs.dagster.io/integrations/dlt).

## References
See `../../references.md` (module-level).
