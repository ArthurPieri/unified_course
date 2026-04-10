# Module 00: Stack Overview (2h)

> Orientation for the Phase 3 lakehouse. Read this before touching any compose file. The topology here is mirrored in `../compose/full-stack/docker-compose.yml` and simplified in `../compose/light-profile/docker-compose.yml`.

## Learning goals

- Draw the Phase 3 stack from memory: which services talk to which, over which ports and protocols.
- Explain the role each service plays in a raw-file → dashboard flow.
- Match Spark 3.5.x with a compatible Iceberg runtime, `hadoop-aws`, and `aws-java-sdk-bundle` — and explain why the versions must be matched.
- Configure S3A to talk to MinIO (path-style access, endpoint override, credentials).
- State the minimum Spark memory configs and where to tune them.

## Prerequisites

- `../../phase_2_core_domain/06_lakehouse_bridge/` (DuckDB + Iceberg concepts)
- Docker + Docker Compose v2 installed

## Reading order

1. This README
2. `../compose/full-stack/README.md`
3. `../compose/light-profile/README.md`
4. `references.md`

## Topology

```
                              +-------------------+
                              |     Metabase      |  :3001  (BI / dashboards)
                              +---------+---------+
                                        |
                                        v (JDBC)
 +-----------+      +----------+    +-------+    +-----------+
 |   dbt     +----->|  Trino   |<---+  HMS  +--->|   MinIO   |  :9000/:9001
 | (trino)   |      |  :8080   |    | :9083 |    |  (S3 API) |
 +-----------+      +----+-----+    +---+---+    +-----+-----+
                         ^              ^              ^
                         |              | Thrift       | S3A
                         |              |              |
                         |          +---+---+          |
                         |          | pg 16 |          |
                         |          | (HMS) |          |
                         |          +-------+          |
                         |                             |
                    +----+-----+                       |
                    |  Spark   +-----------------------+
                    | 3.5.3    |  writes Iceberg via HMS catalog + S3A
                    +----------+
                         ^
                         |
                    +----+------------------+
                    |      Dagster          |  :3000
                    |  (webserver + daemon) |  orchestrates dlt + dbt + Spark
                    +-----------------------+
```

Data flow: raw file → MinIO → Iceberg table registered in HMS → Trino query (or Spark write) → dbt model → Metabase dashboard. Dagster schedules each step.

## Service responsibility

| Service            | Role                                    | Port (host) | Depends on                       |
|--------------------|-----------------------------------------|-------------|----------------------------------|
| `minio`            | S3-compatible object store              | 9000 / 9001 | —                                |
| `metastore-db`     | Postgres backend for HMS                | internal    | —                                |
| `hive-metastore`   | Iceberg HMS catalog (Thrift)            | 9083        | `metastore-db`, `minio`          |
| `trino`            | Distributed SQL engine                  | 8080        | `hive-metastore`                 |
| `spark`            | PySpark batch engine                    | internal    | `minio`, `hive-metastore`        |
| `dagster-db`       | Dagster run + event storage (Postgres)  | internal    | —                                |
| `dagster-webserver`| Dagster UI                              | 3000        | `dagster-db`                     |
| `dagster-daemon`   | Schedules + sensors                     | internal    | `dagster-db`                     |
| `metabase-db`      | Metabase app DB (Postgres)              | internal    | —                                |
| `metabase`         | BI frontend                             | 3001        | `metabase-db`, `trino`           |

The full compose with all healthchecks and mounts lives at `../compose/full-stack/docker-compose.yml`. The sibling reference implementation is `../../../../dataeng/docker-compose.yml:L1-L243` — our version drops the Prometheus/Grafana monitoring block (that moves to Phase 4 · 06_observability) and promotes Spark from "notebook attached on demand" to a first-class compose service.

## Data flow walkthrough

1. **Land raw files in MinIO.** A dlt pipeline (`04_dlt`) or a manual upload drops Parquet/JSON/CSV into `s3://lakehouse/raw/<source>/...`. MinIO exposes the S3 API on port 9000 and a web console on 9001. Ref: [MinIO S3 compatibility](https://min.io/docs/minio/linux/reference/minio-server/minio-server.html).
2. **Register an Iceberg table.** Either Trino (`CREATE TABLE ... WITH (type='ICEBERG', location='s3a://lakehouse/bronze/...')`) or Spark (`spark.sql("CREATE TABLE lakehouse.bronze.trips ...")`) writes metadata to HMS and data files to MinIO. HMS stores table pointers in Postgres; it does not hold data. Ref: [Iceberg Hive catalog](https://iceberg.apache.org/docs/latest/hive/).
3. **Transform with dbt.** `dbt-trino` runs `bronze → silver → gold` models against the Trino coordinator on :8080. Trino pushes reads/writes back through HMS + S3A to MinIO. Ref: [dbt-trino](https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup).
4. **Serve via Metabase.** Metabase's Trino driver queries gold tables; dashboards render in the browser at :3001. Ref: [Metabase Trino driver](https://www.metabase.com/data_sources/starburst).
5. **Orchestrate with Dagster.** Dagster assets wrap each dlt/dbt/Spark step; schedules and sensors trigger them. Ref: [Dagster asset model](https://docs.dagster.io/concepts/assets/software-defined-assets).

## Spark-Iceberg jar gotchas

This is where learners most often lose a day. The Spark service in `../compose/full-stack/docker-compose.yml` pulls all three jars via `--packages`; the block below explains *why* each version is what it is.

### Scala 2.12 vs 2.13

Spark 3.5 is published in two Scala variants: 2.12 (the default distribution) and 2.13. The Iceberg runtime artifact name ends in `_2.12` or `_2.13`, and **it must match the Scala version of your Spark build**. The `apache/spark:3.5.3` image is the 2.12 build, so we use `iceberg-spark-runtime-3.5_2.12:1.5.2`. Mixing them raises `NoSuchMethodError` or `NoClassDefFoundError` at the first catalog call. Refs: [Spark 3.5 downloads page](https://spark.apache.org/downloads.html) (Scala version dropdown), [Iceberg Spark configuration](https://iceberg.apache.org/docs/latest/spark-configuration/).

### hadoop-aws must match Spark's bundled Hadoop exactly

Spark ships with a specific Hadoop version baked in. Spark 3.5.x is built against Hadoop 3.3.4, so **`hadoop-aws` must also be 3.3.4**. Mismatches (e.g. Spark 3.5.x with `hadoop-aws:3.3.6`) cause `NoSuchMethodError` deep in the `S3AFileSystem` init path because internal Hadoop APIs shifted between minor versions. Verify the bundled Hadoop by reading the release notes at [spark.apache.org/releases](https://spark.apache.org/releases/). The `hadoop-aws` module docs: [hadoop-aws 3.3.4](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html). Maven coords: [hadoop-aws on Maven Central](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws/3.3.4).

### aws-java-sdk-bundle must match hadoop-aws

Each `hadoop-aws` release is tested against a specific `aws-java-sdk-bundle` version. For `hadoop-aws:3.3.4` the paired bundle is `com.amazonaws:aws-java-sdk-bundle:1.12.262`, as documented in the [hadoop-aws 3.3.4 dependencies](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws/3.3.4). Upgrading only the SDK without upgrading `hadoop-aws` tends to produce `NoSuchMethodError: com.amazonaws.services.s3.model...`.

### S3A configuration for MinIO

MinIO requires path-style access (`bucket` as a URL segment, not a DNS prefix) and a custom endpoint. Set these on the Spark session (all four are in `docker-compose.yml`):

```
spark.hadoop.fs.s3a.endpoint=http://minio:9000
spark.hadoop.fs.s3a.path.style.access=true
spark.hadoop.fs.s3a.access.key=<MINIO_ROOT_USER>
spark.hadoop.fs.s3a.secret.key=<MINIO_ROOT_PASSWORD>
```

Without `path.style.access=true`, S3A tries `http://lakehouse.minio:9000/...` and the DNS lookup fails. Ref: [Hadoop S3A configuration](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html#S3A).

### Driver / executor memory tuning

The compose sets `spark.driver.memory=2g` and `spark.executor.memory=2g` by default via `.env`. This is the floor that can read a ~500 MB NYC Taxi Parquet partition without spilling aggressively. If a lab OOMs:

1. Bump both to `3g`, then `4g`.
2. Reduce partition count on the write side: `.coalesce(N)` before `.write`.
3. Inspect the Spark UI stage view for skewed tasks.

Ref: [Spark memory tuning](https://spark.apache.org/docs/3.5.3/tuning.html#memory-tuning), [Spark configuration](https://spark.apache.org/docs/3.5.3/configuration.html#application-properties).

## Common failures

| Symptom                                                       | Cause                                             | Fix                                                                   | Source                                                                 |
|---------------------------------------------------------------|---------------------------------------------------|-----------------------------------------------------------------------|------------------------------------------------------------------------|
| `NoSuchMethodError` from `S3AFileSystem.initialize`           | `hadoop-aws` version ≠ Spark's bundled Hadoop     | Pin `hadoop-aws:3.3.4` with Spark 3.5.3                               | [hadoop-aws 3.3.4](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/)  |
| `NoClassDefFoundError` from Iceberg extensions                | Scala variant mismatch (2.12 vs 2.13)             | Use `iceberg-spark-runtime-3.5_2.12` with the 2.12 Spark image        | [Iceberg Spark config](https://iceberg.apache.org/docs/latest/spark-configuration/) |
| S3A tries `http://bucket.minio:9000/...` and DNS fails        | `path.style.access` not set                        | `spark.hadoop.fs.s3a.path.style.access=true`                          | [Hadoop S3A](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html) |
| HMS container crashes on first boot, loops `schematool`       | Postgres not ready when HMS starts                 | `depends_on: metastore-db: condition: service_healthy`                | `../compose/full-stack/docker-compose.yml:L63-L90`                     |
| Trino `iceberg` catalog throws `Failed to connect to HMS`     | HMS health check not yet passing                   | Wait for `docker compose ps` to show HMS healthy; check its logs      | [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) |
| Spark OOM on NYC Taxi job                                     | Default 2g driver/executor too small               | Bump `SPARK_DRIVER_MEM` / `SPARK_EXECUTOR_MEM` in `.env`              | [Spark tuning](https://spark.apache.org/docs/3.5.3/tuning.html)        |

## References

See [references.md](./references.md).

## Checkpoint

Before moving on, you can:

- [ ] Draw the topology diagram from memory, including ports.
- [ ] Explain why `iceberg-spark-runtime-3.5_2.12:1.5.2`, `hadoop-aws:3.3.4`, and `aws-java-sdk-bundle:1.12.262` are pinned together.
- [ ] Name the two S3A configs MinIO needs that a real AWS S3 endpoint does not.
- [ ] Identify which compose service HMS depends on and why the order matters.
- [ ] State which services you lose on the light profile and which Phase 3 objectives are affected.
