# Phase 3: Core Tools, Workflows, and Applied Practice

> The hands-on phase. You stand up a local lakehouse and use every piece of it. Scope, hours, and exit criteria are defined in `../UNIFIED_COURSE_PLAN.md:L245-L352`.

## Prerequisites

- Phase 2 exit criteria met (`../phase_2_core_domain/`)
- 16 GB RAM machine for the full stack; 8 GB works on the light profile (no PySpark — see `compose/light-profile/README.md`)
- Docker + Docker Compose v2 installed

## Compose stacks

Start here. Every module below assumes one of these stacks is running.

- [`compose/full-stack/`](compose/full-stack/) — MinIO + HMS + Trino + Spark + Dagster + Metabase (~16 GB)
- [`compose/light-profile/`](compose/light-profile/) — MinIO + Trino (JDBC Iceberg catalog) + Dagster + Metabase (~6 GB)

## Modules

| #  | Module                                        | Status  | Hours | Link                                 |
|----|-----------------------------------------------|---------|-------|--------------------------------------|
| 00 | Stack overview (topology, jar gotchas)        | scaffolded | 2  | [00_stack_overview/](00_stack_overview/) |
| 01 | MinIO + Iceberg + Hive Metastore              | pending | 8     | `01_minio_iceberg_hms/`              |
| 02 | Trino (SQL, connectors, federation)           | pending | 8     | `02_trino/`                          |
| 03 | PySpark batch processing                      | pending | 12    | `03_pyspark/`                        |
| 04 | dlt — declarative ingestion                   | pending | 6     | `04_dlt/`                            |
| 05 | dbt — modelling and tests                     | pending | 10    | `05_dbt/`                            |
| 06 | Dagster — orchestration                       | pending | 8     | `06_dagster/`                        |
| 07 | Metabase — BI frontend                        | pending | 4     | `07_metabase/`                       |

"pending" modules exist as empty directories scaffolded in Stage 3. They will be filled in later stages using the reuse map in `../references/sibling_sources.md` (grep "Phase 3").

## Labs

Labs live under `labs/` and are wired to specific modules. See `labs/` for the current index.

## Phase exit criteria

From `../UNIFIED_COURSE_PLAN.md:L352`: a 2-hour integration exercise — from a fresh Docker Compose stack, end-to-end flow (start services → create Iceberg table → dbt transform → Trino query → verify). All dbt tests pass. PySpark notebook demonstrates DataFrame transforms with Spark UI analysis. Can explain the data flow at every step.

## References

See [references.md](./references.md).
