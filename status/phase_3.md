# Phase 3 — Build Status

Last updated: 2026-04-10

## Stack scaffolding
- [x] compose/full-stack/docker-compose.yml (pinned: MinIO RELEASE.2025-02-07, HMS 4.0.1, Trino 470, Spark 3.5.3 + Iceberg 1.5.2, Dagster 1.9, Metabase v0.51.10, Postgres 16-alpine)
- [x] compose/full-stack/.env.example
- [x] compose/full-stack/README.md
- [x] compose/light-profile/docker-compose.yml (JDBC catalog, no HMS/Spark, ~6 GB target)
- [x] compose/light-profile/README.md
- [x] 00_stack_overview/README.md (ASCII topology + Spark-Iceberg jar gotchas)
- [x] 00_stack_overview/references.md
- [x] phase_3_core_tools/README.md (phase hub)
- [x] phase_3_core_tools/references.md

## Modules
- [x] 00_stack_overview — drafted 2026-04-10
- [x] 01_minio_iceberg_hms — drafted 2026-04-10 (three-layer lakehouse, metadata tree, ACID via catalog CAS, time travel)
- [x] 02_trino — drafted 2026-04-10 (coordinator/worker/plugin, catalogs, Iceberg connector native S3, EXPLAIN, federation)
- [x] 03_pyspark — drafted 2026-04-10 (GAP module; SparkSession + Iceberg catalog config, jar version trap, writeTo API)
- [x] 04_dlt — drafted 2026-04-10 (resources, incremental cursor, write dispositions, pipeline state)
- [x] 05_dbt — drafted 2026-04-10 (dbt-trino 1.8.*, bronze/silver/gold, generic + singular tests, snapshots)
- [x] 06_dagster — drafted 2026-04-10 (software-defined assets, resources, IO managers, schedules)
- [x] 07_metabase — drafted 2026-04-10 (Trino driver, models, dashboards, caching, permissions)

## Labs
- [x] lab_L3a_stack_up — drafted 2026-04-10
- [x] lab_L3b_dlt_ingest — drafted 2026-04-10
- [x] lab_L3c_dbt_models — drafted 2026-04-10 (dbt_project.yml + profiles.yml.example + 3 models + schema.yml + singular test)
- [x] lab_L3d_dagster_orchestrate — drafted 2026-04-10 (3 assets: raw via dlt, staging + mart via dbt)
- [x] lab_L3e_pyspark_nyc_taxi — drafted 2026-04-10 (taxi_job.py using writeTo...createOrReplace)

## Phase artifacts
- [x] checkpoint_Q3.md — 20 MCQ, 2-3 per module, primary-doc citations

## Decisions recorded
- Full-stack compose mirrors `../dataeng/docker-compose.yml:L1-L243` minus Prometheus/Grafana (moved to Phase 4 · 06_observability)
- Spark service uses `--packages` to pull Iceberg 1.5.2 + hadoop-aws 3.3.4 + aws-java-sdk-bundle 1.12.262 (Scala 2.12, Hadoop 3.3.4 alignment)
- Light profile uses Trino JDBC Iceberg catalog against a dedicated small Postgres (no HMS, no Spark)
- Metabase pinned v0.51.10 (flagged for re-verify); MinIO RELEASE.2025-02-07 (flagged)
- dbt pinned at dbt-core + dbt-trino 1.8.* (installed in Dagster image or dev venv, not in a dedicated compose service)
- `04_dlt` directory name starts with a digit → invalid Python package name. Dagster `assets.py` uses `_04_dlt` alias via sys.path shim
- Lab L3c (dbt) assumes the `iceberg` Trino catalog is wired by lab L3a's compose bring-up — cross-lab coupling is intentional to keep configs DRY
- Phase 3 README "Next" link corrected post-serializer: `phase_4_specializations` (not `phase_4_infrastructure_cloud`)
- checkpoint_Q3 Q14-Q17 (dbt + Dagster) written from primary docs during serializer race; verified conceptually aligned with on-disk modules

## Blockers
none

## Next action
Stage 10 — Appendices + master references merge + final push
