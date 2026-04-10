# Phase 2 — Checkpoint Q2 (20 questions)

Pass = 16/20. Answer key cites the source module and primary reference per question.

---

**Q1.** In Kimball dimensional modeling, the **grain** of a fact table is:
A) The smallest dimension it joins to
B) One business event at the lowest level of detail the fact captures
C) The partition size on disk
D) A synonym for "primary key"

**Q2.** You need to preserve the history of a customer's address changes for reporting "what was the address when the order was placed". The correct SCD type is:
A) Type 0 — no change allowed
B) Type 1 — overwrite in place
C) Type 2 — new row per version with `valid_from` / `valid_to`
D) Type 3 — `current_` and `prior_` columns

**Q3.** Inmon's Corporate Information Factory differs from Kimball's bus architecture primarily in that it:
A) Uses Data Vault as the physical model
B) Builds a normalized enterprise warehouse first, then departmental data marts on top
C) Requires column-store engines
D) Skips the staging layer

**Q4.** "ELT won" over ELT because the warehouse/lakehouse:
A) Is always cheaper than an application server
B) Has the compute and SQL expressiveness to do the transforms, and keeping raw source data enables re-transformation without re-extraction
C) Requires denormalized schemas
D) Makes CDC unnecessary

**Q5.** Idempotency in a pipeline means:
A) The pipeline runs faster on retry
B) Re-running the same input produces the same output state without duplicating rows or side effects
C) All writes are wrapped in transactions
D) The DAG has no cycles

**Q6.** CDC is preferred over snapshot-diff when the source:
A) Has fewer than 10k rows
B) Is append-only
C) Is a high-volume OLTP database with a transaction log you can tail (e.g., Postgres WAL, MySQL binlog)
D) Does not support indexes

**Q7.** In the Medallion architecture, the Silver layer is characterized by:
A) Raw source files, untouched
B) Cleansed, de-duplicated, conformed data ready for modeling
C) Business-level metrics and aggregates
D) The landing zone for CDC events

**Q8.** The CAP theorem states that in the presence of a network partition, a distributed system must choose between:
A) Consistency and Availability
B) Latency and Throughput
C) Durability and Availability
D) Replication and Sharding

**Q9.** Rank these consistency models from strongest to weakest:
A) Eventual → Causal → Sequential → Linearizable
B) Linearizable → Sequential → Causal → Eventual
C) Causal → Linearizable → Sequential → Eventual
D) Sequential → Linearizable → Causal → Eventual

**Q10.** Single-leader replication's characteristic failure mode is:
A) Split-brain
B) Conflicting writes
C) Stale reads from followers (replica lag)
D) Read amplification

**Q11.** Hash partitioning vs range partitioning: hash is preferred when:
A) You frequently do range scans on the partition key
B) You want to spread writes evenly and avoid hotspots on monotonically increasing keys
C) The key is a timestamp
D) You need ordered output

**Q12.** A dbt **generic test** vs **singular test**:
A) Generic is a YAML-configured reusable test (e.g., `unique`, `not_null`); singular is a hand-written SQL file that returns failing rows
B) Generic runs on every model; singular runs only on marts
C) Generic is deprecated
D) Singular tests cannot be parameterized

**Q13.** dbt **unit tests** differ from dbt **data tests** in that unit tests:
A) Run against production data
B) Run on fixture (mock) inputs at CI-time to verify model logic, not data
C) Cannot be written in SQL
D) Require Great Expectations

**Q14.** A dbt **model contract** is a preventive control because it:
A) Blocks a build if the model's output columns/types drift from the declared schema
B) Encrypts the output
C) Triggers a retry
D) Is equivalent to a `not_null` test

**Q15.** Dagster's `FreshnessPolicy` attaches to an asset to:
A) Schedule recomputation
B) Alert or mark the asset as stale if it has not been updated within a declared SLA window
C) Enforce a retention window
D) Compress the asset on disk

**Q16.** Event-time vs processing-time matters because:
A) Processing-time is more accurate for late-arriving events
B) Event-time reflects when the event happened in the real world; processing-time reflects when the system saw it — they can differ by seconds, hours, or days
C) Only event-time works with Kafka
D) They are the same thing in a streaming system

**Q17.** A **watermark** in a streaming system is:
A) A copyright marker on output
B) A heuristic estimate of "event-time progress" used to decide when a window can be closed and emitted
C) A type of checkpoint
D) A DLQ entry

**Q18.** Exactly-once delivery in a producer → Kafka → consumer pipeline requires:
A) Nothing special — Kafka is exactly-once by default
B) Idempotent producer + transactions + consumer commit coupled to output write
C) Only the idempotent producer flag
D) A single-partition topic

**Q19.** The three ingredients of a lakehouse are:
A) Kubernetes + Helm + Terraform
B) Object storage + open file format + open table format
C) HDFS + Hive + Spark
D) Postgres + dbt + Metabase

**Q20.** You `COPY (SELECT …) TO 's3://bucket/out.parquet'` from DuckDB against MinIO. Which extension/setting is required?
A) `spatial`
B) `httpfs` loaded, with `s3_endpoint`, `s3_access_key_id`, `s3_secret_access_key`, and `s3_url_style='path'` configured for MinIO
C) `parquet` extension only
D) None — DuckDB supports S3 natively in the core

---

## Answers

| # | Ans | Source module | Primary citation |
|---|---|---|---|
| 1 | B | 01_data_modeling | *The Data Warehouse Toolkit*, Kimball, Ch. 1 — "Declare the grain" |
| 2 | C | 01_data_modeling | *Kimball*, Ch. 5 — SCD Type 2 |
| 3 | B | 01_data_modeling | *Building the Data Warehouse*, Inmon, Ch. 2 |
| 4 | B | 02_etl_elt_patterns | *Fundamentals of Data Engineering*, Reis & Housley, Ch. 8 |
| 5 | B | 02_etl_elt_patterns | [dbt docs — idempotency](https://docs.getdbt.com/terms/idempotent) |
| 6 | C | 02_etl_elt_patterns | [Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html) |
| 7 | B | 02_etl_elt_patterns | [Databricks Medallion](https://www.databricks.com/glossary/medallion-architecture) |
| 8 | A | 03_distributed_systems | *DDIA*, Kleppmann, Ch. 9 |
| 9 | B | 03_distributed_systems | *DDIA*, Kleppmann, Ch. 9 |
| 10 | C | 03_distributed_systems | *DDIA*, Ch. 5 — replication lag |
| 11 | B | 03_distributed_systems | *DDIA*, Ch. 6 — partitioning |
| 12 | A | 04_data_quality | [dbt tests](https://docs.getdbt.com/docs/build/data-tests) |
| 13 | B | 04_data_quality | [dbt unit tests](https://docs.getdbt.com/docs/build/unit-tests) |
| 14 | A | 04_data_quality | [dbt model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts) |
| 15 | B | 04_data_quality | [Dagster freshness](https://docs.dagster.io/concepts/assets/asset-checks/freshness-checks) |
| 16 | B | 05_streaming_concepts | *DDIA*, Kleppmann, Ch. 11 |
| 17 | B | 05_streaming_concepts | *DDIA*, Ch. 11 — windows and watermarks |
| 18 | B | 05_streaming_concepts | [Kafka EOS design](https://kafka.apache.org/documentation/#semantics) |
| 19 | B | 06_lakehouse_bridge | [Apache Iceberg — lakehouse](https://iceberg.apache.org/); [Parquet spec](https://parquet.apache.org/docs/) |
| 20 | B | 06_lakehouse_bridge | [DuckDB httpfs / S3](https://duckdb.org/docs/extensions/httpfs/s3api.html) |
