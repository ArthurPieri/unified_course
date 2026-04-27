# Full-stack lakehouse compose

Complete Phase 3 reference stack: MinIO, Hive Metastore (with its Postgres backend), Trino, Spark, Dagster (webserver + daemon + Postgres), and Metabase. Based on the companion lakehouse project, with the monitoring services stripped out and Spark promoted to a first-class service for the PySpark labs.

## Requirements

- Docker 25+ / Docker Compose v2 ([install](https://docs.docker.com/compose/install/))
- ~16 GB total RAM; ~25 GB free disk
- CPU: 4+ cores recommended (Spark + Trino both benefit)

## Start

```bash
cp .env.example .env
# edit .env — at minimum change MINIO_ROOT_PASSWORD, HMS_DB_PASSWORD, DAGSTER_DB_PASSWORD
docker compose up -d
docker compose ps
```

First start takes 2-4 minutes: HMS schema init runs on first boot, and Spark downloads its Iceberg/hadoop-aws jars via `--packages`. The jars are cached in the `spark_ivy_cache` volume on subsequent runs.

Tear down (keeps volumes):

```bash
docker compose down
```

Tear down and wipe all data:

```bash
docker compose down -v
```

## Services and ports

| Service            | Port (host) | UI / endpoint                          | Purpose                          |
|--------------------|-------------|-----------------------------------------|----------------------------------|
| `minio`            | 9000 / 9001 | http://localhost:9001 (console)         | S3-compatible object store       |
| `metastore-db`     | internal    | -                                       | Postgres backend for HMS         |
| `hive-metastore`   | 9083        | Thrift `thrift://localhost:9083`        | Iceberg catalog service          |
| `trino`            | 8080        | http://localhost:8080                   | Distributed SQL query engine     |
| `spark`            | internal    | `docker exec -it lh_spark spark-shell`  | PySpark batch engine             |
| `dagster-db`       | internal    | -                                       | Dagster run + event storage      |
| `dagster-webserver`| 3000        | http://localhost:3000                   | Dagster UI                       |
| `dagster-daemon`   | internal    | -                                       | Schedules + sensors              |
| `metabase-db`      | internal    | -                                       | Metabase app DB                  |
| `metabase`         | 3001        | http://localhost:3001                   | BI dashboards                    |

Default credentials come from `.env`. MinIO defaults to `minioadmin` / `minioadmin` — change before exposing anything.

## RAM budget

Targets are compose `mem_limit` caps, not guarantees. Actual resident size is lower when services are idle.

| Service            | Cap      |
|--------------------|----------|
| MinIO              | 1.0 GB   |
| metastore-db       | 0.25 GB  |
| hive-metastore     | 1.0 GB   |
| Trino              | 5.0 GB   |
| Spark (when run)   | 5.0 GB   |
| dagster-db         | 0.25 GB  |
| dagster-webserver  | 1.0 GB   |
| dagster-daemon     | 0.5 GB   |
| metabase-db        | 0.25 GB  |
| Metabase           | 1.5 GB   |
| **Total cap**      | **~15.75 GB** |

Docker itself + the host OS pushes the floor higher. On a 16 GB laptop, expect steady-state usage ~11-13 GB with everything idle; running a Spark job adds 2-4 GB transient. If Spark OOMs, tune `SPARK_DRIVER_MEM` / `SPARK_EXECUTOR_MEM` in `.env` — see Spark tuning docs: https://spark.apache.org/docs/3.5.3/tuning.html.

On 8 GB machines use `../light-profile/` instead.

## Mounted config

This compose references config files under `./conf/` that are included with the scaffold:

- `./conf/metastore-site.xml` — HMS JDBC + S3A settings
- `./conf/trino/catalog/iceberg.properties` — Iceberg catalog pointing at `thrift://hive-metastore:9083`
- `./conf/trino/config.properties`, `./conf/trino/jvm.config` — Trino coordinator config
- `./notebooks/` — mounted read-write into the Spark container work-dir
- `./dagster_home/` — persisted Dagster instance home

Each config file is explained in its corresponding Phase 3 module (`01_minio_iceberg_hms`, `02_trino`, `03_pyspark`).

## Version pinning

All image tags are pinned to exact releases. See `../../00_stack_overview/README.md` for the rationale on each one and the upstream release pages. When bumping, update `../../../references/tools.md` in the same commit.

## References

- Docker Compose: https://docs.docker.com/compose/
- MinIO in Docker: https://min.io/docs/minio/container/index.html
- Hive Metastore image: https://hub.docker.com/r/apache/hive
- Trino on Docker: https://trino.io/docs/current/installation/containers.html
- Spark on Docker: https://spark.apache.org/docs/3.5.3/running-on-docker.html
- Dagster Postgres storage: https://docs.dagster.io/deployment/dagster-instance#postgres-storage
- Metabase running: https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker
