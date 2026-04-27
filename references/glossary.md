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

**RBAC (Role-Based Access Control)** — access control model where permissions are assigned to roles, and users assume roles. Simplifies management by grouping permissions into logical job functions.
Ref: Sandhu, R. et al. (1996). "Role-Based Access Control Models." *IEEE Computer* 29(2), pp. 38–47. · [NIST RBAC](https://csrc.nist.gov/projects/role-based-access-control)

**ABAC (Attribute-Based Access Control)** — access control model where authorization decisions use attributes of the subject, resource, action, and environment (e.g., IP range, time of day). More flexible than RBAC but harder to audit.
Ref: [NIST SP 800-162: Guide to ABAC](https://csrc.nist.gov/pubs/sp/800/162/final)

## Data engineering concepts

**ETL / ELT** — ETL (Extract–Transform–Load) transforms data before loading into the target; ELT (Extract–Load–Transform) loads raw data first, then transforms in the target warehouse. ELT dominates cloud warehouses because storage is cheap and compute is elastic.
Ref: *Fundamentals of Data Engineering*, Reis & Housley, Ch. 8

**Backfill** — retroactively loading or reprocessing historical data through a pipeline that normally handles only new increments. Common after schema changes, bug fixes, or new source onboarding.
Ref: *Fundamentals of Data Engineering*, Reis & Housley, Ch. 8

**Idempotency** — property of an operation where running it multiple times produces the same result as running it once. Critical for pipeline retries — if a task fails and restarts, idempotent writes prevent duplicates.
Ref: *Designing Data-Intensive Applications*, Kleppmann, Ch. 11

**Schema-on-read vs. schema-on-write** — schema-on-write enforces structure at write time (RDBMS, Iceberg); schema-on-read defers interpretation to query time (raw data lakes, JSON blobs). Lakehouse formats bring schema-on-write to the data lake.
Ref: *Designing Data-Intensive Applications*, Kleppmann, Ch. 4

**Materialized view** — a precomputed query result stored as a table and refreshed on demand or on a schedule. Trades storage and freshness for query speed.
Ref: [PostgreSQL: materialized views](https://www.postgresql.org/docs/current/rules-materializedviews.html)

**Compaction** — background process that merges many small files into fewer, larger files. In Iceberg, compaction rewrites data files and updates metadata without changing table contents.
Ref: [Iceberg maintenance — compaction](https://iceberg.apache.org/docs/latest/maintenance/#compact-data-files)

**DLQ (Dead Letter Queue)** — a queue where messages that cannot be processed after a configured number of retries are diverted. Prevents poison messages from blocking the main pipeline.
Ref: [AWS SQS DLQ docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html) · [Kafka error handling patterns](https://kafka.apache.org/documentation/#connect_errantrecordreporter)

**SLO / SLI** — an SLI (Service Level Indicator) is a quantitative measure of a service aspect (e.g., latency p99, freshness lag). An SLO (Service Level Objective) is a target value for an SLI (e.g., "freshness lag < 15 min, 99.5% of the time"). SLAs are contractual commitments built on SLOs.
Ref: Beyer, B. et al. (2016). *Site Reliability Engineering*, O'Reilly, Ch. 4. · [Google SRE Book — Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)

**ADR (Architecture Decision Record)** — a short document capturing one architecture decision: context, decision, and consequences. Accumulated ADRs form a decision log that explains *why* the system looks the way it does.
Ref: Nygard, M. (2011). "Documenting Architecture Decisions." · [adr.github.io](https://adr.github.io/)
