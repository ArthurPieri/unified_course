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
- [ ] 01_minio_iceberg_hms — pending (Stage 5 batch A)
- [ ] 02_trino — pending (Stage 5 batch A)
- [ ] 03_pyspark — pending (Stage 5 batch A, GAP)
- [ ] 04_dlt — pending (Stage 5 batch A)
- [ ] 05_dbt — pending (Stage 5 batch B)
- [ ] 06_dagster — pending (Stage 5 batch B)
- [ ] 07_metabase — pending (Stage 5 batch B)

## Labs
- [ ] lab_L3a_stack_up — pending
- [ ] lab_L3b_dlt_ingest — pending
- [ ] lab_L3c_dbt_models — pending
- [ ] lab_L3d_dagster_orchestrate — pending
- [ ] lab_L3e_pyspark_nyc_taxi — pending

## Decisions recorded
- Full-stack compose mirrors `../dataeng/docker-compose.yml:L1-L243` minus Prometheus/Grafana (moved to Phase 4 · 06_observability)
- Spark service uses `--packages` to pull Iceberg 1.5.2 + hadoop-aws 3.3.4 + aws-java-sdk-bundle 1.12.262 (Scala 2.12, Hadoop 3.3.4 alignment)
- Light profile uses Trino JDBC Iceberg catalog against a dedicated small Postgres (no HMS, no Spark)
- Metabase pinned v0.51.10 (flagged for re-verify); MinIO RELEASE.2025-02-07 (flagged)
- dbt not pinned in compose; lives in Dagster image or dev venv

## Blockers
none

## Next action
Stage 5: launch parallel agents for modules 01-07 + labs L3a-L3e
