# Lab L3a: Stack up — MinIO + HMS + Trino + Iceberg

## Goal
Bring up the object store + catalog + query engine slice of the full-stack compose, create a warehouse bucket, register a namespace in Hive Metastore, create an Iceberg table from Trino, write and read rows, inspect the metadata tree in MinIO, then tear down.

## Prerequisites
- Docker 25+, Docker Compose v2. Ref: [Docker Compose install](https://docs.docker.com/compose/install/).
- `mc` CLI installed on the host, or willingness to run it via `docker run minio/mc`. Ref: [mc CLI reference](https://min.io/docs/minio/linux/reference/minio-mc.html).
- Trino CLI jar on the host, or run it via `docker exec -it lh_trino trino`. Ref: [Trino CLI](https://trino.io/docs/current/client/cli.html).
- Module read: `../../README.md`.

## Setup

The compose file at `../../../compose/full-stack/docker-compose.yml` mounts HMS + Trino config from `./conf/`. Create the minimum set before starting anything:

```bash
cd phase_3_core_tools/compose/full-stack
cp .env.example .env
# ensure the warehouse bucket name matches the lab
grep -q '^LAKEHOUSE_BUCKET=' .env || echo 'LAKEHOUSE_BUCKET=warehouse' >> .env

mkdir -p conf/trino/catalog
cat > conf/trino/catalog/iceberg.properties <<'EOF'
connector.name=iceberg
iceberg.catalog.type=hive_metastore
hive.metastore.uri=thrift://hive-metastore:9083
hive.s3.endpoint=http://minio:9000
hive.s3.path-style-access=true
hive.s3.aws-access-key=minioadmin
hive.s3.aws-secret-key=minioadmin
fs.native-s3.enabled=true
EOF
```

Ref: [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html). The `metastore-site.xml` and remaining Trino configs come from module `../00_stack_overview/` in your own branch; if `./conf/metastore-site.xml` is missing, copy the reference from `../../compose/full-stack/conf/metastore-site.xml` before proceeding.

## Steps

1. **Start the MinIO + HMS + Trino slice.**
   ```bash
   docker compose up -d minio metastore-db hive-metastore trino
   docker compose ps
   ```
   Wait for all four to show `healthy` (HMS takes ~60s on first boot for `schematool`). Ref: `../../../compose/full-stack/docker-compose.yml:L71-L98`.

2. **Create the `warehouse` bucket in MinIO with `mc`.**
   ```bash
   docker run --rm --network lakehouse_net minio/mc \
     alias set lh http://minio:9000 minioadmin minioadmin
   docker run --rm --network lakehouse_net minio/mc \
     mb lh/warehouse
   docker run --rm --network lakehouse_net minio/mc ls lh/
   ```
   Expected:
   ```
   [ ... ]  warehouse/
   ```
   Ref: [`mc alias`](https://min.io/docs/minio/linux/reference/minio-mc/mc-alias.html), [`mc mb`](https://min.io/docs/minio/linux/reference/minio-mc/mc-mb.html).

3. **Open the Trino CLI and create a namespace in HMS.**
   ```bash
   docker exec -it lh_trino trino --catalog iceberg
   ```
   ```sql
   CREATE SCHEMA IF NOT EXISTS iceberg.demo
     WITH (location = 's3a://warehouse/demo/');
   SHOW SCHEMAS FROM iceberg;
   ```
   `demo` must appear. Ref: [Trino Iceberg connector — schema location](https://trino.io/docs/current/connector/iceberg.html).

4. **Create an Iceberg table and write a few rows.**
   ```sql
   CREATE TABLE iceberg.demo.trips (
     id       BIGINT,
     pickup   TIMESTAMP(6),
     fare_usd DOUBLE
   );
   INSERT INTO iceberg.demo.trips VALUES
     (1, TIMESTAMP '2025-01-01 08:00:00', 12.50),
     (2, TIMESTAMP '2025-01-01 08:05:00',  7.25),
     (3, TIMESTAMP '2025-01-01 08:11:00', 23.00);
   SELECT count(*), sum(fare_usd) FROM iceberg.demo.trips;
   ```

5. **Inspect the Iceberg metadata tree in MinIO.**
   ```bash
   docker run --rm --network lakehouse_net minio/mc \
     ls --recursive lh/warehouse/demo/trips/
   ```
   You should see a `metadata/` prefix containing a `metadata.json`, a snapshot Avro (manifest list), and one or more manifest Avro files, plus a `data/` prefix with Parquet files. Ref: [Iceberg table spec — Overview](https://iceberg.apache.org/spec/#overview).

6. **Query table history from Trino.**
   ```sql
   SELECT snapshot_id, committed_at FROM iceberg.demo."trips$snapshots";
   ```
   Ref: [Trino Iceberg — metadata tables](https://trino.io/docs/current/connector/iceberg.html#metadata-tables).

## Verify
- [ ] `mc ls lh/warehouse/demo/trips/metadata/` lists at least one `*.metadata.json`, one `snap-*.avro`, and one `*-m0.avro`.
- [ ] `SELECT count(*) FROM iceberg.demo.trips` returns `3`.
- [ ] `SHOW CREATE TABLE iceberg.demo.trips` shows `location = 's3a://warehouse/demo/trips'` (or similar).
- [ ] The `trips$snapshots` metadata table has at least one row.

## Cleanup
```bash
# still in phase_3_core_tools/compose/full-stack
docker compose down           # keep volumes for the next lab
# OR wipe everything including the bucket:
docker compose down -v
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| Trino: `Failed to connect to Hive metastore` | Wait until `docker compose ps` shows `hive-metastore` `healthy`; first boot is slow. |
| `CREATE TABLE` error `Bucket warehouse does not exist` | Re-run step 2; the bucket is not auto-created. |
| S3A path error mentioning `warehouse.minio` | `path-style-access` missing in `iceberg.properties`; re-check setup step. |
| HMS loops `schematool` | `docker compose down -v` to drop the Postgres volume, then `up -d` again. |

## Stretch goals
- Run `ALTER TABLE iceberg.demo.trips EXECUTE expire_snapshots(retention_threshold => '0s')` and re-list the metadata prefix. Ref: [Trino Iceberg — expire_snapshots](https://trino.io/docs/current/connector/iceberg.html#expire-snapshots).
- Insert a second batch and use `SELECT * FROM iceberg.demo.trips FOR VERSION AS OF <snapshot_id>` to travel back.

## References
See `../../references.md`.
