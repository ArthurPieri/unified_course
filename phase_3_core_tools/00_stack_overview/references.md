# References — 00_stack_overview

## Compose reference

- `../../compose/full-stack/docker-compose.yml` — the self-contained full lakehouse stack for this course. Based on the companion lakehouse project.

## Upstream release pages (version pinning)

- MinIO releases: https://github.com/minio/minio/releases
- Apache Hive downloads: https://hive.apache.org/general/downloads/
- Apache Hive Docker image: https://hub.docker.com/r/apache/hive
- Trino releases: https://github.com/trinodb/trino/releases
- Apache Spark releases: https://spark.apache.org/releases/
- Apache Spark 3.5 downloads (Scala version selector): https://spark.apache.org/downloads.html
- Apache Iceberg releases: https://github.com/apache/iceberg/releases
- iceberg-spark-runtime 1.5.2: https://github.com/apache/iceberg/releases/tag/apache-iceberg-1.5.2
- hadoop-aws 3.3.4 on Maven Central: https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws/3.3.4
- aws-java-sdk-bundle 1.12.262 on Maven Central: https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-bundle/1.12.262
- Dagster releases: https://github.com/dagster-io/dagster/releases
- Metabase releases: https://github.com/metabase/metabase/releases
- PostgreSQL versioning policy: https://www.postgresql.org/support/versioning/

## Configuration docs

- Iceberg Spark configuration: https://iceberg.apache.org/docs/latest/spark-configuration/
- Iceberg Hive catalog: https://iceberg.apache.org/docs/latest/hive/
- Hadoop S3A (3.3.4): https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html
- Spark 3.5.3 configuration: https://spark.apache.org/docs/3.5.3/configuration.html
- Spark 3.5.3 memory tuning: https://spark.apache.org/docs/3.5.3/tuning.html#memory-tuning
- Trino Iceberg connector: https://trino.io/docs/current/connector/iceberg.html
- Trino Iceberg JDBC catalog: https://trino.io/docs/current/connector/iceberg.html#jdbc-catalog
- MinIO health probe: https://min.io/docs/minio/linux/operations/monitoring/healthcheck-probe.html
- MinIO S3 compatibility: https://min.io/docs/minio/linux/reference/minio-server/minio-server.html
- Dagster instance / Postgres storage: https://docs.dagster.io/deployment/dagster-instance#postgres-storage
- Dagster software-defined assets: https://docs.dagster.io/concepts/assets/software-defined-assets
- Metabase Docker install: https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker
- Metabase app DB guidance: https://www.metabase.com/docs/latest/installation-and-operation/configuring-application-database
- Metabase Trino driver: https://www.metabase.com/data_sources/starburst
- Docker Compose install: https://docs.docker.com/compose/install/
- dbt-trino setup: https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup

## Course-internal

- `../../UNIFIED_COURSE_PLAN.md:L245-L303` — Phase 3 scope + PySpark block
- `../../references/tools.md` — canonical version index (updated by Stage 4)
- `../../references/sibling_sources.md` — Phase 3 reuse mapping
