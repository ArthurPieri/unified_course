# Phase 6 References

Citation list for the capstone scaffolding in this directory. Follows `../docs/REUSE_POLICY.md` citation rules: primary docs and specs, canonical books, sibling-directory files with line ranges, no blog posts.

## Course internal

- `../UNIFIED_COURSE_PLAN.md` L523–L572 — Phase 6 capstone specification (project scope, assessment criteria, fast-track alternative, exit criteria). Source of truth for [`project_brief.md`](project_brief.md) and [`12_dimension_rubric.md`](12_dimension_rubric.md).
- `../UNIFIED_COURSE_PLAN.md` L577 — vendor-branch entry condition: "After Phase 5 completion with Phase 6 capstone complete OR fast-track rubric met."
- `../UNIFIED_COURSE_PLAN.md` L926 — phase priority: capstone is P1 and recommended.
- `../UNIFIED_COURSE_PLAN.md` L537–L548 — enumeration of the 12 required components, source for the 12-dimension rubric mapping.
- `../UNIFIED_COURSE_PLAN.md` L550–L556 — five acceptance criteria used verbatim in [`project_brief.md`](project_brief.md).
- `../UNIFIED_COURSE_PLAN_adversarial_analysis_v2.md` L97–L118 — Finding #3: the v1 rubric was cosmetic; Option A (convert to concrete self-diagnostic deliverables) is the basis for [`fast_track_rubric.md`](fast_track_rubric.md).
- `../UNIFIED_COURSE_PLAN_adversarial_analysis_v2.md` L296 — severity table entry for the fast-track mechanism.
- `../docs/REUSE_POLICY.md` — citation format and reuse-first rule applied to all Phase 6 writing.
- `../docs/TEMPLATE_module.md` — module structure template (not a strict fit for Phase 6 since this phase has no labs, but followed in spirit).
- `../phase_0_orientation/README.md` — tone reference for all phase README files.

## Sibling reference implementations

All of these are in `../dataeng/` (the working lakehouse stack that seeds Phase 3 and the capstone). Index: `../references/sibling_sources.md`.

- `../dataeng/docker-compose.yml` — reference compose stack; starting point for the capstone
- `../dataeng/dagster/lakehouse/assets/ingestion.py` — Dagster ingestion asset pattern
- `../dataeng/dagster/lakehouse/assets/transformation.py` — dbt-to-asset bridge
- `../dataeng/dagster/lakehouse/assets/quality.py` — quality-check asset pattern
- `../dataeng/dagster/lakehouse/assets/maintenance.py` — Iceberg compaction pattern
- `../dataeng/dagster/lakehouse/schedules/daily_pipeline.py` — schedule pattern
- `../dataeng/dagster/lakehouse/sensors/minio_sensor.py` — object-landing sensor pattern
- `../dataeng/dbt_project/models/staging/` — staging model layout
- `../dataeng/dbt_project/models/marts/fct_trip_metrics.sql` — fact table pattern
- `../dataeng/dbt_project/tests/assert_positive_revenue.sql` — singular test pattern
- `../dataeng/dbt_project/unit_tests/test_revenue_calculation.yml` — unit test pattern (for fast-track Deliverable 1)
- `../dataeng/dlt_pipelines/taxi_pipeline.py` — end-to-end dlt pipeline
- `../dataeng/prometheus/prometheus.yml` — Prometheus scrape config (for fast-track Deliverable 5)
- `../dataeng/grafana/provisioning/` — Grafana datasource + dashboard provisioning
- `../dataeng/.github/workflows/dbt-ci.yml` — dbt CI workflow (for fast-track Deliverable 6)
- `../dataeng/.github/workflows/pipeline-validation.yml` — full pipeline CI
- `../phase_3_core_tools/compose/full-stack/docker-compose.yml` — unified course variant of the compose stack

## Primary tool documentation

Per `../docs/REUSE_POLICY.md` priority 1. These are the canonical sources the capstone components are built against.

- Apache Iceberg spec: https://iceberg.apache.org/spec/
- Apache Iceberg Spark getting started: https://iceberg.apache.org/docs/latest/spark-getting-started/
- Trino documentation: https://trino.io/docs/current/
- Apache Spark documentation: https://spark.apache.org/docs/latest/
- dbt documentation: https://docs.getdbt.com/
- dbt model contracts: https://docs.getdbt.com/docs/collaborate/govern/model-contracts
- dbt unit tests: https://docs.getdbt.com/docs/build/unit-tests
- Dagster documentation: https://docs.dagster.io/
- Dagster asset checks + freshness: https://docs.dagster.io/concepts/assets/asset-checks
- dlt documentation: https://dlthub.com/docs
- MinIO documentation: https://min.io/docs/minio/linux/index.html
- Hive Metastore (via Apache Hive): https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+Administration
- Debezium documentation: https://debezium.io/documentation/
- Prometheus alerting rules: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
- Grafana documentation: https://grafana.com/docs/grafana/latest/
- GitHub Actions documentation: https://docs.github.com/en/actions
- Docker Compose reference: https://docs.docker.com/compose/

## Table format comparison (fast-track Deliverable 3)

- Iceberg spec: https://iceberg.apache.org/spec/
- Delta Lake protocol: https://github.com/delta-io/delta/blob/master/PROTOCOL.md
- Delta Lake documentation: https://docs.delta.io/

## Canonical books

Cited per `../docs/REUSE_POLICY.md` priority 3.

- *Designing Data-Intensive Applications*, Kleppmann — Ch. 5 (Replication), Ch. 6 (Partitioning), Ch. 9 (Consistency and Consensus) for CDC + partitioning + idempotency reasoning
- *The Data Warehouse Toolkit*, Kimball — Ch. 1–3 for dimensional modeling of the Gold layer
- *Fundamentals of Data Engineering*, Reis & Housley — Ch. 5 (Data Generation), Ch. 6 (Storage), Ch. 8 (Queries, Modeling, Transformation) for lifecycle framing

## Sibling vendor references (for post-capstone context)

- `../aws_certified/labs/week-11-lab-capstone.md` — AWS capstone lab, used as the AWS-branch port target referenced in `../UNIFIED_COURSE_PLAN.md` L638
- `../azure_certified/labs/04-batch-and-pipeline-patterns.md` — Azure port reference, `../UNIFIED_COURSE_PLAN.md` L729
- `../snowflake_eng/STUDY_PLAN.md` — Snowflake port reference, `../UNIFIED_COURSE_PLAN.md` L824
