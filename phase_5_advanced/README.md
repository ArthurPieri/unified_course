# Phase 5 — Advanced Architecture, Operations, and Strategy (50–65h)

Phase 5 elevates individual pipeline competence to system-level thinking: shipping via CI/CD, running on Kubernetes, orchestrating with Airflow, reasoning about cloud and identity, controlling cost, and serving data to applications and models.

## Modules
| # | Name | Hours | Link |
|---|---|---|---|
| 01 | CI/CD for Data — GitHub Actions, dbt deployment | 8h | [01_cicd/](01_cicd/) |
| 02 | Kubernetes Fundamentals — pods, services, Helm, Trino on kind | 8h | [02_kubernetes_basics/](02_kubernetes_basics/) |
| 03 | Airflow Bridge — DAGs, operators, Dagster comparison | 6h | [03_airflow_bridge/](03_airflow_bridge/) |
| 04 | Cloud Concepts — IaaS/PaaS/SaaS, multi-cloud mapping, lifecycle | 6h | [04_cloud_concepts/](04_cloud_concepts/) |
| 05 | Cloud IAM Primer — principals, policies, least privilege, LocalStack | 5h | [05_iam_primer/](05_iam_primer/) |
| 06 | FinOps & Cost Optimization — TCO, right-sizing, query cost | 6h | [06_finops/](06_finops/) |
| 07 | Data Serving — APIs, feature stores, reverse ETL | 6h | [07_data_serving/](07_data_serving/) |

## Exit criteria
- CI/CD pipeline for the lakehouse project runs green on GitHub Actions.
- Trino deployed on a local Kubernetes cluster via Helm and reachable from the host.
- Cost estimation produced for 3 scale scenarios of the lakehouse stack.
- FastAPI endpoint serving a Gold-layer query with a Pydantic response model.
- Airflow DAG replicating the dbt pipeline, with a written comparison to the Dagster equivalent.
- Architecture decision record (ADR) written for one non-trivial technology choice.
- Exit quiz passed — [checkpoint_Q5.md](checkpoint_Q5.md) (16/20 to pass).

## Reference
- Course hub: [../README.md](../README.md)
- Curriculum plan: [../UNIFIED_COURSE_PLAN.md](../UNIFIED_COURSE_PLAN.md) §Phase 5
- Glossary: [../references/glossary.md](../references/glossary.md)
- Reuse & citation policy: [../docs/REUSE_POLICY.md](../docs/REUSE_POLICY.md)
