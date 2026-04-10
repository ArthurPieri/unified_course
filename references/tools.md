# Tool Version Index

Tool versions used across the course. These are pinned in the Phase 3 Docker Compose files for reproducibility.

**Pinning policy:** Stage 4 (Phase 3 stack scaffolding) verifies every version against the upstream release page before committing. This file is updated by Stage 4, not before.

Last verified: *pending Stage 4*

## Core stack (Phase 3)

| Tool | Version | Source of truth | Notes |
|---|---|---|---|
| MinIO | *pending* | [MinIO release tags](https://github.com/minio/minio/releases) | Object storage |
| Hive Metastore | 4.0.1 (target) | [Hive releases](https://hive.apache.org/general/downloads/) | Iceberg catalog |
| Apache Iceberg | 1.5.x (target) | [Iceberg releases](https://github.com/apache/iceberg/releases) | Table format |
| Trino | 470 (target) | [Trino releases](https://github.com/trinodb/trino/releases) | Query engine |
| Apache Spark | 3.5.x (target) | [Spark releases](https://spark.apache.org/releases/) | Batch engine |
| Scala runtime | 2.12 | n/a | Must match iceberg-spark-runtime-3.5_2.12 |
| hadoop-aws | 3.3.4 | [Maven Central](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws) | S3A filesystem |
| aws-java-sdk-bundle | 1.12.x | [Maven Central](https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-bundle) | S3 client |
| dbt-core | 1.8.x (target) | [dbt-core releases](https://github.com/dbt-labs/dbt-core/releases) | Transformations |
| dbt-trino | *pending* | [dbt-trino releases](https://github.com/starburstdata/dbt-trino/releases) | Trino adapter |
| Dagster | 1.9.x (target) | [Dagster releases](https://github.com/dagster-io/dagster/releases) | Orchestrator |
| Metabase | *pending* | [Metabase releases](https://github.com/metabase/metabase/releases) | BI frontend |
| DuckDB | *pending* | [DuckDB releases](https://github.com/duckdb/duckdb/releases) | In-process OLAP |
| PostgreSQL | 16 (stable) | [PostgreSQL versioning](https://www.postgresql.org/support/versioning/) | OLTP + HMS backend |

## Phase 4 additions

| Tool | Version | Source | Notes |
|---|---|---|---|
| Debezium | *pending* | [Debezium releases](https://github.com/debezium/debezium/releases) | CDC |
| Apache Kafka | *pending* | [Kafka releases](https://kafka.apache.org/downloads) | Streaming |
| kafka-python | *pending* | [PyPI kafka-python](https://pypi.org/project/kafka-python/) | Python client |

## Phase 5 additions

| Tool | Version | Source | Notes |
|---|---|---|---|
| Apache Airflow | *pending* | [Airflow releases](https://airflow.apache.org/announcements/) | Orchestrator bridge |
| LocalStack | *pending* | [LocalStack releases](https://github.com/localstack/localstack/releases) | IAM primer sandbox |
| Prometheus | *pending* | [Prometheus releases](https://github.com/prometheus/prometheus/releases) | Metrics |
| Grafana | *pending* | [Grafana releases](https://github.com/grafana/grafana/releases) | Dashboards |

## Python

- Python 3.12+ required (per dbt, Dagster, dlt current compatibility; re-verify in Stage 4)
