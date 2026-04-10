# Lab L3e: PySpark NYC Taxi → Iceberg → Trino

## Goal

Run a PySpark job via `spark-submit` against the Phase 3 full-stack compose that reads an NYC Yellow Taxi Parquet file from MinIO over `s3a://`, computes per-hour trip counts, writes the result to an Iceberg table registered in HMS, and confirms the write with a Trino `SELECT`.

## Prerequisites

- `../00_stack_overview/` and `../01_minio_iceberg_hms/` complete.
- Phase 3 full-stack compose running: `cd phase_3_core_tools/compose/full-stack && docker compose up -d` (wait until `docker compose ps` shows `minio`, `hive-metastore`, `trino`, and `spark` healthy).
- One NYC Yellow Taxi monthly Parquet file (e.g. `yellow_tripdata_2024-01.parquet`) from the NYC TLC Trip Record Data page ([nyc.gov/site/tlc/about/tlc-trip-record-data.page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)).

## Setup

```bash
# 1. Upload the taxi file to MinIO under s3://lakehouse/raw/.
docker compose exec minio mc alias set local http://localhost:9000 minioadmin minioadmin
docker compose exec minio mc mb -p local/lakehouse || true
docker cp ./yellow_tripdata_2024-01.parquet lh_minio:/tmp/
docker compose exec minio mc cp /tmp/yellow_tripdata_2024-01.parquet local/lakehouse/raw/

# 2. Create the target Iceberg namespace once, from the Spark container.
docker compose exec spark /opt/spark/bin/spark-sql \
  --conf spark.sql.catalog.lakehouse.type=hive \
  -e "CREATE SCHEMA IF NOT EXISTS lakehouse.nyc;"

# 3. Copy the job script into the Spark work-dir (mounted at ./notebooks).
cp taxi_job.py ../../../compose/full-stack/notebooks/taxi_job.py
```

## Steps

1. Submit the job. The compose's Spark service already has `--packages` cached in `spark_ivy_cache`, so the second run is fast.
   ```bash
   docker compose exec spark /opt/spark/bin/spark-submit \
     --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
     --conf spark.sql.catalog.lakehouse=org.apache.iceberg.spark.SparkCatalog \
     --conf spark.sql.catalog.lakehouse.type=hive \
     --conf spark.sql.catalog.lakehouse.uri=thrift://hive-metastore:9083 \
     --conf spark.sql.catalog.lakehouse.warehouse=s3a://lakehouse/ \
     /opt/spark/work-dir/taxi_job.py
   ```
   Expected tail:
   ```
   Rows read    : 2964624
   Rows written : 744
   Wrote lakehouse.nyc.trips_hourly
   ```

2. Verify the write from Trino.
   ```bash
   docker compose exec trino trino --catalog iceberg --schema nyc \
     --execute "SELECT pickup_hour, trip_count FROM trips_hourly ORDER BY pickup_hour LIMIT 5;"
   ```
   Expected output:
   ```
   "2024-01-01 00:00:00","1432"
   "2024-01-01 01:00:00","980"
   ...
   ```

## Verify

- [ ] `spark-submit` exits 0 and prints a non-zero `Rows written`.
- [ ] Trino returns at least one row from `iceberg.nyc.trips_hourly`.
- [ ] `mc ls local/lakehouse/nyc/trips_hourly/` shows `data/` and `metadata/` directories.

## Cleanup

```bash
docker compose exec spark /opt/spark/bin/spark-sql \
  -e "DROP TABLE IF EXISTS lakehouse.nyc.trips_hourly PURGE;"
docker compose exec minio mc rm --recursive --force local/lakehouse/raw/yellow_tripdata_2024-01.parquet
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `NoClassDefFoundError` from `IcebergSparkSessionExtensions` | Scala mismatch — confirm the compose still uses `iceberg-spark-runtime-3.5_2.12:1.5.2`. |
| `NoSuchMethodError` in `S3AFileSystem.initialize` | `hadoop-aws` version drift — pin `hadoop-aws:3.3.4` with Spark 3.5.3. |
| DNS error like `bucket.minio not found` | Missing `spark.hadoop.fs.s3a.path.style.access=true` (compose sets it; check for overrides). |
| Trino `Table 'iceberg.nyc.trips_hourly' does not exist` | Confirm the Trino `iceberg` catalog points at `thrift://hive-metastore:9083` and the `nyc` schema was created. |
| OOM in executor | Bump `SPARK_DRIVER_MEM` / `SPARK_EXECUTOR_MEM` in `.env`, re-up the `spark` service. |

## Stretch goals

- Add `.partitionBy("pickup_date")` to the write and re-query from Trino to see per-day files.
- Swap `createOrReplace` for append-mode and re-run over a second month's file.

## References

See `../../references.md` (module-level).
