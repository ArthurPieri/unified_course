# Phase 3 — Core Tools, Workflows, and Applied Practice (54h)

The hands-on phase. You stand up a local lakehouse on Docker Compose — MinIO + Iceberg + Hive Metastore + Trino + Spark + dlt + dbt + Dagster + Metabase — and drive it end-to-end from raw file to dashboard. Every module ends in a lab you run against the same stack; the exit criterion is a 2-hour integration exercise where you walk the full flow in front of an imaginary reviewer and explain each hop.

## Prerequisites

- [Phase 2 complete](../phase_2_core_domain/) — data modeling, ETL/ELT patterns, distributed-systems literacy, quality engineering, streaming concepts, lakehouse bridge.
- 16 GB RAM for the full stack; 8 GB works on the light profile (no PySpark — see [`compose/light-profile/`](compose/light-profile/)).
- Docker + Docker Compose v2 installed.

## Compose stacks

Start here. Every module below assumes one of these stacks is running.

- [`compose/full-stack/`](compose/full-stack/) — MinIO + HMS + Trino + Spark + Dagster + Metabase (~16 GB)
- [`compose/light-profile/`](compose/light-profile/) — MinIO + Trino (JDBC Iceberg catalog) + Dagster + Metabase (~6 GB)

## Module order

| #  | Module                                          | Hours | Type                                    | Link                                      |
|----|-------------------------------------------------|-------|-----------------------------------------|-------------------------------------------|
| 00 | Stack Overview — topology, jar gotchas          | 2     | primary — spark.apache.org + iceberg    | [00_stack_overview/](00_stack_overview/)  |
| 01 | MinIO + Iceberg + Hive Metastore                | 6     | primary — iceberg spec + MinIO docs     | [01_minio_iceberg_hms/](01_minio_iceberg_hms/) |
| 02 | Trino — SQL, connectors, federation             | 6     | primary — trino.io                      | [02_trino/](02_trino/)                    |
| 03 | PySpark on the Lakehouse                        | 8     | **GAP** — primary docs only             | [03_pyspark/](03_pyspark/)                |
| 04 | dlt — Python-native ingestion                   | 6     | partial-reuse — `../dataeng/dlt_pipelines/` | [04_dlt/](04_dlt/)                    |
| 05 | dbt — modelling and tests                       | 10    | partial-reuse — `../dataeng/dbt_project/` | [05_dbt/](05_dbt/)                      |
| 06 | Dagster — orchestration                         | 8     | partial-reuse — `../dataeng/dagster/`   | [06_dagster/](06_dagster/)                |
| 07 | Metabase — BI frontend                          | 4     | primary — metabase.com/docs             | [07_metabase/](07_metabase/)              |

Total: 54h. Each module has `README.md` → labs → `quiz.md` → `references.md`.

## Labs in this phase

| Lab | Module | Goal |
|---|---|---|
| `lab_L3a_stack_up` | 01 | Bring up MinIO + HMS + Trino, create a warehouse bucket, CREATE/INSERT/SELECT an Iceberg table, inspect the metadata tree |
| `lab_L3b_dlt_ingest` | 04 | Ingest NYC taxi Parquet into MinIO as an Iceberg table with an incremental cursor, verify via Trino |
| `lab_L3c_dbt_trino` | 05 | Build bronze/silver/gold Iceberg models with dbt-trino; run `dbt test`; wire an SCD Type 2 snapshot |
| `lab_L3d_dagster` | 06 | Wrap the dlt + dbt + Spark steps as Dagster assets; schedule a daily run; watch the UI |
| `lab_L3e_pyspark_nyc_taxi` | 03 | `spark-submit` a PySpark job that reads Parquet from MinIO, writes a per-hour Iceberg table, and SELECTs it from Trino |

Labs live under [`labs/`](labs/) and are wired to the module that introduces them.

## Phase exit criteria — Checkpoint Q3

Before leaving Phase 3, you should be able to:

- [ ] Draw the full-stack topology from memory — services, ports, and which depends on which.
- [ ] Explain, per service, what it stores and what it only routes: HMS stores pointers, MinIO stores bytes, Trino stores nothing, Iceberg metadata lives in the bucket.
- [ ] Recite the Spark 3.5 / Iceberg 1.5.2 / hadoop-aws 3.3.4 / aws-java-sdk-bundle 1.12.262 / Scala 2.12 matrix and the failure mode each pin guards against.
- [ ] Configure S3A to talk to MinIO without re-reading the docs (endpoint override + path-style access + credentials).
- [ ] Write and read an Iceberg table from both Spark and Trino against the same HMS and see the same rows.
- [ ] Run a time-travel query and a snapshot expiry, and say which files the expiry deletes.
- [ ] Write a dlt `@dlt.resource` with an `incremental("cursor_col")` and explain where the cursor state lives.
- [ ] Build dbt bronze/silver/gold models on dbt-trino, use `ref()` across layers, and write one generic and one singular test.
- [ ] Wrap dlt + dbt + Spark as Dagster assets and explain how assets differ from Airflow tasks.
- [ ] Point Metabase at Trino, build a dashboard on a gold table, and explain which layer cached a stale result.
- [ ] State the one-line rule for Trino vs Spark and for Metabase vs direct SQL.

Take [checkpoint_Q3.md](checkpoint_Q3.md) — 20 questions, pass = 16/20. Below that, re-read the module cited in the answer key.

## References

Each module has its own `references.md` citing the primary doc pages used. The phase-level aggregator is [references.md](references.md); the course-wide index is [`../references/docs.md`](../references/docs.md) and the sibling reuse map is [`../references/sibling_sources.md`](../references/sibling_sources.md) (grep "Phase 3").

## Next

[Phase 4 — Specializations](../phase_4_specializations/) (CDC, Kafka hands-on, semi-structured data, security/governance, performance tuning, observability).
