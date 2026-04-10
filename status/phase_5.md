# Phase 5 — Build Status

Last updated: 2026-04-10

## Modules
- [x] 01_cicd — drafted 2026-04-10 (GH Actions, OIDC, dbt PR pattern, preview envs; reuses `../dataeng/.github/workflows/`)
- [x] 02_kubernetes_basics — drafted 2026-04-10 (reconciliation model, core resources, kind, Helm, when-K8s-vs-managed)
- [x] 03_airflow_bridge — drafted 2026-04-10 (TaskFlow vs classic, Dagster contrast, MWAA/Composer, top-level-code pitfall)
- [x] 04_cloud_concepts — drafted 2026-04-10 (cloud-neutral; AWS/Azure/GCP citations; shared responsibility, AZs, VPC, egress)
- [x] 05_iam_primer — drafted 2026-04-10 (principal/action/resource/condition, STS AssumeRole, LocalStack hands-on)
- [x] 06_finops — drafted 2026-04-10 (FinOps Framework phases, unit economics, spot, egress as silent killer)
- [x] 07_data_serving — drafted 2026-04-10 (BI/API/feature-store/reverse-ETL patterns, FastAPI, gRPC, Feast)

## Labs
- [x] lab_L5a_cicd_k8s — drafted (uv + ruff + pytest on PR; kind + Helm Trino smoke test on main)
- [x] lab_L5b_airflow_dag — drafted (TaskFlow DAG: dlt → dbt build → quality check; + dag_example.py)
- [x] lab_iam_localstack — drafted (LocalStack IAM + S3 + STS AssumeRole, 4 test cases)

## Artifacts
- [x] phase_5_advanced/README.md (phase hub)
- [x] phase_5_advanced/checkpoint_Q5.md (20-Q checkpoint)

## Decisions recorded
- IAM primer is hands-on via LocalStack (V2 Finding #8) — offline-friendly, no AWS account needed
- Airflow is taught as a "bridge" from Dagster: concept parity + MWAA/Composer reality, not a deep Airflow course
- Cloud concepts module is vendor-neutral — cites all three hyperscalers per topic
- CI/CD lab uses kind (not a managed EKS/AKS/GKE) so it runs on the learner's laptop

## Blockers
none

## Next action
Stage 8 — Phase 6 capstone (complete, pending commit)
