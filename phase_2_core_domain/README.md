# Phase 2 — Core Domain (50–65h)

Tool-agnostic fundamentals every data engineer must own before touching a specific stack. Data modeling, ETL/ELT patterns, distributed-systems literacy, quality engineering, streaming concepts, and a hands-on bridge from abstract lakehouse concepts to a running MinIO + DuckDB sandbox.

## Prerequisites
- [Phase 1 complete](../phase_1_foundations/) — shell, Docker, SQL fluency, Python basics.

## Module order

| # | Module | Hours | Type |
|---|---|---|---|
| 01 | [Data Modeling](01_data_modeling/) | 14 | **GAP** — Kimball, Inmon, Data Vault |
| 02 | [ETL / ELT Patterns](02_etl_elt_patterns/) | 10 | primary docs + `../dataeng/` dlt pipeline |
| 03 | [Distributed Systems](03_distributed_systems/) | 8 | **GAP** — *DDIA, Kleppmann* Ch. 5–11 |
| 04 | [Data Quality — Tests, Contracts, Checks](04_data_quality/) | 8 | partial-reuse — `../dataeng/` dbt + Dagster |
| 05 | [Streaming Concepts](05_streaming_concepts/) | 6 | **GAP** — *DDIA* Ch. 11 + Kafka/Debezium docs |
| 06 | [Lakehouse Bridge — MinIO + DuckDB + Parquet](06_lakehouse_bridge/) | 6 | primary — MinIO, DuckDB, Parquet spec |

Module hours: 52h. With buffer for data modeling exercises and lakehouse bridge setup: **50–65h** (5–6 weeks at 10–12h/week).

## Labs in this phase
| Lab | Module | Goal |
|---|---|---|
| lab_L2_star_schema | 01 | Build a star schema in Postgres with an SCD Type 2 dimension |
| lab_L2b_minio_duckdb | 06 | Write Parquet to MinIO via S3 API, query it with DuckDB `httpfs` |

## Exit criteria — Checkpoint Q2
Before leaving Phase 2, you should be able to:
- [ ] Design a star schema from a business process (grain, facts, conformed dimensions)
- [ ] Pick an SCD type per attribute and defend the choice
- [ ] Contrast ETL vs ELT and pick the right incremental strategy for a source
- [ ] State the CAP theorem precisely and name one failure mode of each replication topology
- [ ] Write a dbt generic test and a Dagster `@asset_check`; decide error vs warn
- [ ] Explain event-time vs processing-time, tumbling vs sliding windows, at-least-once vs exactly-once
- [ ] Write Parquet to S3-compatible storage and query it in place without a metastore

Take [checkpoint_Q2.md](checkpoint_Q2.md) — 20 questions, pass = 16/20.

## References
Each module has its own `references.md` citing primary sources. Canonical books for this phase are tracked in [references/books.md](../references/books.md): *The Data Warehouse Toolkit* (Kimball), *Building the Data Warehouse* (Inmon), *Designing Data-Intensive Applications* (Kleppmann), *Fundamentals of Data Engineering* (Reis & Housley).

## Next
[Phase 3 — Core Tools](../phase_3_core_tools/) (the full lakehouse stack: MinIO + Iceberg + HMS + Trino + Spark + dlt + dbt + Dagster + Metabase).
