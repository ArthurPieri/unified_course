# Appendix B — Database Engine Taxonomy

## Why this appendix

Phase 2 teaches core storage, ETL, and distributed-system concepts hands-on. This appendix is the "someone said *we need a database*, what are the choices" reference — the engine comparison that V1 Finding #4 moved out of Phase 2 to keep that phase focused. Read it once when you need to place a new engine on the map; it is not required to finish the course.

Every non-trivial claim below cites a primary source. See [references.md](references.md) for the full list.

## The axes

### OLTP vs OLAP

Transactional systems optimize for many small, random, concurrent reads and writes with strict consistency. Analytical systems optimize for large sequential scans over wide rows with batch-style queries. Kleppmann's framing is in *Designing Data-Intensive Applications*, Ch. 3 (Transaction Processing vs Analytics).

### Row-oriented vs columnar storage

Row stores co-locate all fields of a record on disk and win for point lookups and single-record updates. Column stores co-locate all values of a column and win for scans that touch few columns and many rows — they enable aggressive compression and vectorized execution. Primary source: *Designing Data-Intensive Applications*, Kleppmann, Ch. 3 (Column-Oriented Storage). The Parquet file format encodes this idea on disk: [Apache Parquet — file format](https://parquet.apache.org/docs/file-format/).

### Shared-nothing MPP vs single-node

A shared-nothing massively parallel processing cluster partitions data across independent nodes and parallelizes query fragments. A single-node engine runs on one machine and stays there until it hits a resource wall. Kleppmann, Ch. 6 (Partitioning), is the concept anchor.

### Storage-compute coupled vs decoupled

Coupled systems (classical MPP, classical Postgres) tie storage and compute to the same nodes. Decoupled systems store data in a shared object store and spin compute up and down against it — the lakehouse pattern, as implemented by Snowflake virtual warehouses, BigQuery slots, Databricks SQL warehouses, and the open-source MinIO + Iceberg + Trino stack that Phase 3 builds. Primary sources: [Snowflake key concepts & architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts) (three-layer architecture: storage, virtual warehouses, cloud services), [Amazon Redshift RA3 node types](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html) (coupled→decoupled via managed storage).

### ACID vs BASE

Classical relational databases enforce atomicity, consistency, isolation, durability. Many "NoSQL" systems relax these for availability and partition tolerance — *Basically Available, Soft state, Eventual consistency*. Kleppmann, Ch. 7 (Transactions) and Ch. 9 (Consistency and Consensus) are the references.

## Representative engines

| Engine | Category | Storage model | Typical workload | Canonical doc |
|---|---|---|---|---|
| PostgreSQL | Row OLTP (with OLAP extensions) | Heap + B-tree/GIN/BRIN | General OLTP, small-mid analytics | [postgresql.org/docs](https://www.postgresql.org/docs/current/) |
| MySQL | Row OLTP | InnoDB B-tree | Web app OLTP | [dev.mysql.com/doc](https://dev.mysql.com/doc/) |
| ClickHouse | Columnar OLAP | MergeTree (columnar) | High-volume analytics, event logs | [clickhouse.com/docs](https://clickhouse.com/docs) |
| DuckDB | Columnar embedded OLAP | Single-file columnar | Local / in-process analytics | [duckdb.org/docs](https://duckdb.org/docs/) |
| Snowflake | MPP, storage-compute decoupled | Micro-partitions in S3-class storage | Cloud warehouse | [docs.snowflake.com](https://docs.snowflake.com/) |
| BigQuery | MPP, storage-compute decoupled | Capacitor columnar on Colossus | Cloud warehouse | [cloud.google.com/bigquery/docs](https://cloud.google.com/bigquery/docs) |
| Amazon Redshift | MPP (coupled; RA3 decouples via managed storage) | Columnar | Cloud warehouse | [docs.aws.amazon.com/redshift](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html) |
| Databricks SQL Warehouse | Lakehouse MPP | Delta Lake on object storage | Lakehouse analytics | [docs.databricks.com](https://docs.databricks.com/) |
| Trino | SQL engine, no storage | Connectors only | Federated SQL, lakehouse query | [trino.io/docs/current](https://trino.io/docs/current/) |
| Apache Spark SQL | Compute engine, no storage | DataFrame on any source | Large-scale batch + ML | [spark.apache.org/docs/latest](https://spark.apache.org/docs/latest/) |
| Apache Iceberg | Table format (not an engine) | Manifest + snapshot metadata over Parquet/ORC | Lakehouse table state | [iceberg.apache.org/spec](https://iceberg.apache.org/spec/) |
| MongoDB | Document | BSON, B-tree | App document store | [mongodb.com/docs](https://www.mongodb.com/docs/) |
| Cassandra | Wide-column (Dynamo-style) | LSM tree, partition keys | High-write, horizontally scaled | [cassandra.apache.org/doc](https://cassandra.apache.org/doc/latest/) |
| Redis | Key-value (in-memory) | Hash tables, data structures | Cache, session, queues | [redis.io/docs](https://redis.io/docs/latest/) |
| Elasticsearch | Inverted-index search | Lucene segments | Full-text, log search | [elastic.co/docs](https://www.elastic.co/docs) |

Iceberg is not an engine; it is the table-state layer that Trino, Spark, Snowflake, Athena, Dremio, and others read and write. The Phase 3 stack uses this exact split: MinIO (bytes) + Hive Metastore (catalog) + Iceberg (table state) + Trino or Spark (compute).

## Which course module covers what

| Engine / category | Taught in |
|---|---|
| PostgreSQL (OLTP) | [phase_1_foundations/05_sql_postgres](../phase_1_foundations/05_sql_postgres/) |
| DuckDB (embedded OLAP) | [phase_2_core_domain/06_lakehouse_bridge](../phase_2_core_domain/06_lakehouse_bridge/) |
| Trino (federated SQL + lakehouse query) | [phase_3_core_tools/02_trino](../phase_3_core_tools/02_trino/) |
| Apache Spark (compute on Iceberg) | [phase_3_core_tools/03_pyspark](../phase_3_core_tools/03_pyspark/) |
| Iceberg (table format, hands-on) | [phase_3_core_tools/01_minio_iceberg_hms](../phase_3_core_tools/01_minio_iceberg_hms/) |
| Kafka (log-based streaming system) | [phase_4_specializations/02_kafka_hands_on](../phase_4_specializations/02_kafka_hands_on/) |
| Redshift / Athena / EMR (AWS) | [vendors/aws/03_compute_emr_athena_redshift](../vendors/aws/03_compute_emr_athena_redshift/) |
| Synapse / Databricks / Fabric (Azure) | [vendors/azure/03_compute_synapse_databricks_fabric](../vendors/azure/03_compute_synapse_databricks_fabric/) |
| Snowflake (architecture, performance) | [vendors/snowflake/01_architecture](../vendors/snowflake/01_architecture/), [vendors/snowflake/05_performance](../vendors/snowflake/05_performance/) |

## Anti-patterns to remember

- Don't use Postgres for 10 TB analytic scans. The heap + B-tree layout pays the row-store scan cost on every query; a columnar engine or lakehouse table will be orders of magnitude cheaper. See Kleppmann, DDIA Ch. 3 for the underlying reason.
- Don't use Trino as a catalog of truth. Trino has no storage — restart the cluster and "the data" is gone unless it lives in a catalog Trino reads through a connector. See [Trino concepts: connector and catalog](https://trino.io/docs/current/overview/concepts.html).
- Don't use Iceberg/Parquet as an OLTP store. Both are designed for large immutable files; per-row random updates are not the intended workload. See [Iceberg spec](https://iceberg.apache.org/spec/) on snapshot-based writes.
- Don't use MongoDB as a replacement for a warehouse. Document stores optimize for application-owned aggregates, not cross-entity analytical joins.
- Don't use Redis as durable storage without understanding its persistence modes (RDB snapshots, AOF log). The default in-memory-only behavior means a crash loses everything since the last snapshot. See [Redis persistence docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/).
