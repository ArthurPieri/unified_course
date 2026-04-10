# Lab L2b: MinIO + DuckDB + Parquet

## Goal
Run a local S3-compatible object store (MinIO), generate 10,000 synthetic rows with DuckDB, write them to MinIO as a Parquet object, and query them back over an `s3://` URL — all without a metastore or query server.

## Prerequisites
- Docker Engine running
- `duckdb` CLI ≥ 1.1 on PATH ([install](https://duckdb.org/docs/installation/))
- `mc` (MinIO client) on PATH ([install](https://min.io/docs/minio/linux/reference/minio-mc.html)) — or use the MinIO console at `http://localhost:9001`
- Completed module reading (`../../README.md`)

## Setup
```bash
cd phase_2_core_domain/06_lakehouse_bridge/labs/lab_L2b_minio_duckdb
export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin
docker compose up -d
docker compose ps              # minio should be (healthy)
```

Create the bucket (pick one):
```bash
# Option A: mc CLI
mc alias set local http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
mc mb local/lakehouse

# Option B: MinIO console
open http://localhost:9001     # log in with the env vars above, then create "lakehouse"
```

## Steps
1. Launch DuckDB and run the provided SQL script:
   ```bash
   duckdb -c ".read generate.sql"
   ```
   Expected tail of output:
   ```
   ┌───────────┬───────────────────┐
   │ row_count │    avg_amount     │
   │   int64   │      double       │
   ├───────────┼───────────────────┤
   │     10000 │ ~500.0            │
   └───────────┴───────────────────┘
   ```
2. List the object from the host to confirm it landed in MinIO:
   ```bash
   mc ls local/lakehouse/events/
   # data.parquet
   ```
3. Open the console at `http://localhost:9001`, browse to the `lakehouse` bucket, and confirm `events/data.parquet` is listed with a non-zero size.
4. (Stretch) The script also writes a partitioned layout under `s3://lakehouse/events_partitioned/region_id=*/...parquet` via `PARTITION_BY`. Inspect it:
   ```bash
   mc ls --recursive local/lakehouse/events_partitioned/
   ```

## Verify
- [ ] `docker compose ps` shows MinIO as `healthy`
- [ ] `mc ls local/lakehouse/events/` shows `data.parquet`
- [ ] The DuckDB `SELECT count(*)` query returns exactly `10000`
- [ ] MinIO console shows the object with a non-zero byte size
- [ ] (Stretch) The partitioned layout has 7 subdirectories (`region_id=0` … `region_id=6`)

## Cleanup
```bash
docker compose down -v
unset MINIO_ROOT_USER MINIO_ROOT_PASSWORD
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `IO Error: Connection refused` on COPY | Confirm `s3_endpoint='localhost:9000'` (no scheme) and `s3_use_ssl=false` |
| `HTTP 400 InvalidRequest` / signature errors | `SET s3_url_style='path';` — MinIO requires path-style |
| `NoSuchBucket` | Create `lakehouse` via `mc mb local/lakehouse` before running the COPY |
| Port 9000 already in use | Stop conflicting container or edit `ports:` in `docker-compose.yml` |
| `httpfs` not available | Run both `INSTALL httpfs;` and `LOAD httpfs;` — the script does this |

## Stretch goals
- Replace `PARTITION_BY (region_id)` with a two-column partition and compare file counts.
- Query the Parquet file from Python via `duckdb.connect()` and the same `SET s3_*` pragmas.
- Point `DuckDB` at the partitioned glob and verify partition pruning with `EXPLAIN ANALYZE`.

## References
See `../../references.md` (module-level).
