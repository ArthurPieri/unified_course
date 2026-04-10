# Glossary

Short, cited definitions of recurring terms. Each entry links to the primary source.

## Storage / File formats

**Parquet** — columnar binary file format for analytics workloads. Stores data by column, enabling selective column reads and compression.
Ref: [Apache Parquet format specification](https://parquet.apache.org/docs/file-format/)

**Avro** — row-oriented binary serialization format with JSON-defined schemas. Common for message-broker payloads.
Ref: [Apache Avro specification](https://avro.apache.org/docs/)

**ORC** — columnar file format optimized for Hive workloads. Stripes of columns with embedded indexes.
Ref: [Apache ORC specification](https://orc.apache.org/specification/)

**Apache Iceberg** — open table format for huge analytic datasets. Provides schema evolution, hidden partitioning, time travel, and atomic commits over files in object storage.
Ref: [Iceberg table spec v2/v3](https://iceberg.apache.org/spec/)

## Lakehouse / Architecture

**Medallion architecture** — data lake refinement pattern with Bronze (raw), Silver (cleaned/conformed), and Gold (business-aggregated) layers.
Ref: [Databricks Medallion architecture docs](https://docs.databricks.com/aws/en/lakehouse/medallion)

**Lakehouse** — architectural pattern combining data lake storage (object store + open formats) with warehouse-like features (ACID, schema enforcement, indexing).

**Data Mesh** — decentralized sociotechnical approach treating data as a product owned by domain teams, supported by self-serve data infrastructure.

## Modeling

**SCD (Slowly Changing Dimension)** — technique for tracking changes to dimension attributes over time. Common types: Type 1 (overwrite), Type 2 (new row per change, valid-from/valid-to), Type 3 (prior value column).
Ref: *The Data Warehouse Toolkit*, Kimball, Ch. 5

**Star schema** — dimensional model with a central fact table linked to denormalized dimension tables.
Ref: *The Data Warehouse Toolkit*, Kimball, Ch. 1

**Data Vault** — modeling methodology using hubs, links, and satellites to provide auditable, historized, source-agnostic storage.

## Processing / Compute

**Trino** — distributed SQL query engine for running interactive analytic queries against heterogeneous sources.
Ref: [Trino overview](https://trino.io/docs/current/overview.html)

**Apache Spark** — unified engine for large-scale data processing, providing DataFrame, SQL, streaming, and ML APIs.
Ref: [Spark overview](https://spark.apache.org/docs/latest/)

**DuckDB** — in-process OLAP database. Embeds in a Python/C++/etc. process; executes columnar analytic queries on Parquet/CSV/Arrow without a server.
Ref: [DuckDB docs](https://duckdb.org/docs/)

**Shuffle** — Spark operation that redistributes data across partitions; required by groupBy, join, and repartition. Expensive because it writes to disk and moves data over the network.
Ref: [Spark performance tuning](https://spark.apache.org/docs/latest/tuning.html)

## Ingestion / Streaming

**CDC (Change Data Capture)** — technique for tracking and propagating row-level changes from source databases to downstream systems, typically by reading transaction logs.
Ref: [Debezium CDC overview](https://debezium.io/documentation/reference/stable/architecture.html)

**Apache Kafka** — distributed event streaming platform. Topics partitioned across brokers; producers append, consumers read offsets.
Ref: [Kafka overview](https://kafka.apache.org/documentation/#introduction)

**dlt (data load tool)** — Python library for declarative E+L pipelines with automatic schema inference, normalization, and incremental loading.
Ref: [dlt docs](https://dlthub.com/docs/intro)

## Transformation / Orchestration

**dbt (data build tool)** — SQL-first transformation framework. Models are SELECT statements; dbt handles dependency graphs, tests, and docs.
Ref: [dbt docs](https://docs.getdbt.com/)

**Dagster** — data orchestrator built around Software-Defined Assets (declare what data should exist; the scheduler figures out how).
Ref: [Dagster concepts](https://docs.dagster.io/concepts)

**Apache Airflow** — task-centric workflow orchestration platform. DAGs composed of operators run on a schedule.
Ref: [Airflow concepts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html)

## Quality / Governance

**Data contract** — schema + constraint agreement between a data producer and its consumers, enforced at pipeline boundaries.
Ref: [dbt contracts docs](https://docs.getdbt.com/docs/collaborate/govern/model-contracts)

**Schema evolution** — adding, removing, or modifying columns in a table over time while preserving query compatibility.
Ref: [Iceberg schema evolution](https://iceberg.apache.org/docs/latest/evolution/)

**PII (Personally Identifiable Information)** — data that can identify a specific individual; subject to regulatory handling (GDPR, CCPA).

## Distributed systems

**CAP theorem** — in a distributed system, consistency, availability, and partition-tolerance cannot all be simultaneously maximized; partition-tolerance is generally required, so the trade-off is CP vs. AP.
Ref: *Designing Data-Intensive Applications*, Kleppmann, Ch. 9

**Eventual consistency** — replicas converge to the same state if no new updates are made; reads may return stale data until convergence.
Ref: *Designing Data-Intensive Applications*, Kleppmann, Ch. 5

## Ops

**FinOps** — discipline of managing cloud cost as an ongoing, cross-functional practice.
Ref: [FinOps Framework](https://www.finops.org/framework/)

**IAM (Identity and Access Management)** — cloud service model defining principals (users, roles), actions, resources, and conditions that together determine who can do what.
Ref: [AWS IAM user guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
