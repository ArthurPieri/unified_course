# Capstone Project Brief

Source spec: `../UNIFIED_COURSE_PLAN.md` §Phase 6 (L523–L572). This document turns that spec into a standalone brief you can hand to a reviewer. Nothing here is new curriculum — if something conflicts with the plan, the plan wins.

## Problem statement

Build a production-grade lakehouse end-to-end for a realistic public dataset of your choice. The goal is not to build something novel; it is to integrate every tool from Phases 3–5 into a single system that a stranger could onboard onto in one afternoon using only your README.

"Production-grade" here means: it runs unattended on a schedule, it tells you when it is broken, it resists unauthorized reads of sensitive data, it can be redeployed from source control, and every non-obvious decision is documented in an ADR. It does not mean high-availability or multi-region — you are proving integration competence on a single machine or a small Kind cluster, not running a real SaaS.

## Dataset — pick one

Pick the dataset you find most interesting. All three are large enough to stress partitioning and file sizing, and all three contain fields that plausibly need masking.

| Dataset | Why it works | PII / sensitivity angle |
|---|---|---|
| **NYC Taxi (TLC) trip records** | Canonical. Clean schema, large volume, natural time partitioning. Already used in Phase 3 labs (`../phase_3_core_tools/05_dbt/`), so you can lift the dbt models. | Pickup/dropoff coordinates → quasi-identifier; license numbers → direct identifier |
| **GitHub Archive (gharchive.org)** | JSON event stream, nested schemas, natural for CDC-style append. Good stress test for schema evolution. | Actor logins + emails in some event types |
| **Wikipedia pageviews** | Hourly batch dumps, massive cardinality, strong aggregation story. | Low PII — use it only if you plan to synthesize a "user profile" table on the side to exercise masking |

Choose one. Do not mix datasets. If you picked NYC Taxi because it reuses Phase 3 code, that is fine — the integration work is still non-trivial.

## Required components

All twelve of these are called out in `../UNIFIED_COURSE_PLAN.md` L537–L548. Dropping any component means the capstone is not complete.

1. **Source ingestion — dlt.** At least two ingestion modes: a batch API pull and an append-only stream (simulated producer is acceptable). CDC from a PostgreSQL source via Debezium is required if you took Phase 4 (`../UNIFIED_COURSE_PLAN.md` L537–L538).
2. **Raw / Bronze / Silver / Gold zones on Iceberg.** Medallion architecture on MinIO-backed Iceberg tables with a Hive Metastore catalog. Bronze = immutable raw landing, Silver = cleaned and conformed, Gold = business-ready marts.
3. **dbt models with contracts and tests.** Staging → intermediate → marts. Every mart must have a dbt contract (`docs.getdbt.com/docs/collaborate/govern/model-contracts`). Every source must have at least one freshness check and one not-null/unique test. At least one dbt unit test.
4. **Dagster orchestration with schedules and sensors.** The full pipeline expressed as software-defined assets. At least one schedule (daily or hourly) and at least one sensor (e.g., MinIO object-landing → dlt run). Retry policies on every asset that touches the network.
5. **PII masking + RBAC.** For whichever dataset you chose, identify the PII columns, document the masking/redaction decision per column, and enforce role-based access via Trino (or Spark views) such that an unprivileged role cannot read the unmasked version. Keep an audit trail of access attempts.
6. **Prometheus + Grafana monitoring.** Scrape Dagster, dbt run metrics, and at least one pipeline-health metric (rows-per-run, freshness lag, or DAG success rate). One Grafana dashboard tied to those metrics. At least one alert rule wired to a fake receiver (webhook, file, or email).
7. **GitHub Actions CI/CD.** On every PR: lint (ruff/pre-commit), `dbt compile`, `dbt test` against a CI profile, and at least one integration test. Merge to main is blocked on green CI. Optional but encouraged: a deploy job that re-applies the compose stack to a remote host.
8. **Architecture diagram.** One page, readable, labeled. ASCII in the README is acceptable; a PNG rendered from diagrams.net is better. It must match reality.
9. **ADR folder.** At least three ADRs using a minimal template (context / decision / consequences). Suggested topics: why Iceberg over Delta, why dbt over Spark SQL scripts, why Dagster over Airflow for this project.
10. **README sufficient for onboarding.** Someone who has never seen your repo must be able to clone, run, and query in under 30 minutes following only the README. Prerequisites, `docker compose up`, bootstrap commands, where to click in Dagster and Metabase, how to rerun a failed asset.

## Time budget

50–70 hours, ideally spread over 4–6 weeks (`../UNIFIED_COURSE_PLAN.md` L558). A realistic breakdown:

| Week | Focus | Hours |
|---|---|---|
| 1 | Compose stack up, Bronze ingestion working, dataset loaded | 10–14h |
| 2 | Silver + Gold dbt models, contracts, tests | 10–14h |
| 3 | Dagster DAG + schedules + sensors + retry policies | 8–12h |
| 4 | Security (PII + RBAC), observability (Prometheus + alert) | 10–14h |
| 5 | CI/CD, ADRs, README, architecture diagram | 8–12h |
| 6 | Polish, acceptance-criteria dry run from a fresh clone | 4–8h |

If you are tracking significantly over 70h, stop adding features and start cutting scope. The rubric rewards completeness over cleverness.

## Acceptance criteria

Copied verbatim in spirit from `../UNIFIED_COURSE_PLAN.md` L550–L556. You are done when all five pass from a fresh clone of your repository:

1. **Pipeline runs end-to-end without manual intervention.** `docker compose up -d`, wait for health, trigger the Dagster schedule (or let it fire), and the full Bronze → Silver → Gold → dashboard flow completes without human steps. No "run this SQL by hand first" caveats.
2. **All dbt tests pass.** `dbt build` exits 0. Freshness checks pass on live sources. Unit tests pass.
3. **Monitoring detects an injected failure within 5 minutes.** Break something deliberately (kill the metastore container, point a dbt model at a missing column, drop a source file). Prometheus + Grafana + your alert rule must fire within 5 minutes. Document the injection procedure in the README.
4. **PII masking prevents unauthorized reads.** A query run as the unprivileged role against the PII column returns masked/redacted values. The same query run as the privileged role returns the raw value. An audit log entry exists for both queries.
5. **Documentation is sufficient for a stranger to onboard.** Give the README to someone outside the course. They should get to a running pipeline in under 30 minutes without asking you questions. If they get stuck, the README is wrong — fix it, not them.

Additional quality bar from the plan (L556): pre-commit hooks pass, type hints where they make sense, test coverage on any non-trivial Python.

## What you hand in

A public Git repository containing the code, the ADRs, the architecture diagram, the README, and a `rubric_self_review.md` scoring yourself against [`12_dimension_rubric.md`](12_dimension_rubric.md). The self-review is the honest version — dimensions you know you are weak on are the dimensions a vendor-branch interviewer will push on.

## What this capstone does NOT cover

Streaming exactly-once semantics, multi-region replication, schema-registry integration beyond the basics, sub-second serving latency, and anything that requires a managed cloud service. Those belong in the vendor branches (`../UNIFIED_COURSE_PLAN.md` §VI). The capstone is deliberately open-source and local — the vendor branches then port the same architecture onto AWS / Azure / Snowflake (`../UNIFIED_COURSE_PLAN.md` L638, L729, L824).
