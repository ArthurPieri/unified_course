# Tool Version Index

Tool versions used across the course. These are pinned in the Phase 3 Docker Compose files for reproducibility.

**Pinning policy:** Stage 4 (Phase 3 stack scaffolding) verifies every version against the upstream release page before committing. This file is updated by Stage 4, not before.

Last verified: 2026-04-27

## Core stack (Phase 3)

| Tool | Version | Source of truth | Notes |
|---|---|---|---|
| MinIO | RELEASE.2025-02-07T23-21-09Z | [MinIO release tags](https://github.com/minio/minio/releases) | Object storage |
| Hive Metastore | 4.0.1 | [Hive releases](https://hive.apache.org/general/downloads/) | Iceberg catalog |
| Apache Iceberg | 1.5.2 | [Iceberg releases](https://github.com/apache/iceberg/releases) | Table format (via Spark runtime jar) |
| Trino | 470 | [Trino releases](https://github.com/trinodb/trino/releases) | Query engine |
| Apache Spark | 3.5.3 | [Spark releases](https://spark.apache.org/releases/) | Batch engine |
| Scala runtime | 2.12 | n/a | Must match iceberg-spark-runtime-3.5_2.12 |
| hadoop-aws | 3.3.4 | [Maven Central](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws) | S3A filesystem |
| aws-java-sdk-bundle | 1.12.262 | [Maven Central](https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-bundle) | S3 client |
| dbt-core | 1.8.x | [dbt-core releases](https://github.com/dbt-labs/dbt-core/releases) | Transformations |
| dbt-trino | 1.8.x | [dbt-trino releases](https://github.com/starburstdata/dbt-trino/releases) | Trino adapter |
| Dagster | 1.9.x | [Dagster releases](https://github.com/dagster-io/dagster/releases) | Orchestrator |
| Metabase | v0.51.10 | [Metabase releases](https://github.com/metabase/metabase/releases) | BI frontend |
| DuckDB | 1.1+ | [DuckDB releases](https://github.com/duckdb/duckdb/releases) | In-process OLAP (host-installed for Lab L2b) |
| PostgreSQL | 16-alpine | [PostgreSQL versioning](https://www.postgresql.org/support/versioning/) | OLTP + HMS backend |

## Phase 4 additions

| Tool | Version | Source | Notes |
|---|---|---|---|
| Debezium | 2.7 | [Debezium releases](https://github.com/debezium/debezium/releases) | CDC |
| Apache Kafka | 3.8.0 | [Kafka releases](https://kafka.apache.org/downloads) | Streaming |
| kafka-python | 2.0.2 | [PyPI kafka-python](https://pypi.org/project/kafka-python/) | Python client |

## Phase 5 additions

| Tool | Version | Source | Notes |
|---|---|---|---|
| Apache Airflow | 2.x | [Airflow releases](https://airflow.apache.org/announcements/) | Orchestrator bridge |
| LocalStack | 3.8 | [LocalStack releases](https://github.com/localstack/localstack/releases) | IAM primer sandbox |
| Prometheus | latest stable | [Prometheus releases](https://github.com/prometheus/prometheus/releases) | Metrics (conceptual module) |
| Grafana | latest stable | [Grafana releases](https://github.com/grafana/grafana/releases) | Dashboards (conceptual module) |

## Python

- Python 3.11+ required (per dbt, Dagster, dlt current compatibility)
