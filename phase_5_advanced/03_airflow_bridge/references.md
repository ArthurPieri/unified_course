# References — 03_airflow_bridge

## Primary docs (airflow.apache.org)
- [Airflow — Architecture overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html) — scheduler, executor, workers, metadata DB
- [Airflow — Core Concepts / DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) — DAG object, scheduling, parsing
- [Airflow — Operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html) — classic operator model, built-ins
- [Airflow — TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html) — `@task`, implicit XComs, dependency inference
- [Airflow — XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html) — cross-task communication, size limits, custom backends
- [Airflow — Connections](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html) — credential storage, secrets backends, `conn_id`
- [Airflow — Datasets and data-aware scheduling](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html) — the closest Airflow equivalent to Dagster assets
- [Airflow — Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html) — top-level-code trap, idempotency, DAG design
- [Airflow — Templates reference](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html) — `{{ ds }}`, `{{ data_interval_start }}`, Jinja context
- [Airflow — Running Airflow in Docker / standalone](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) — local-dev compose reference
- [Airflow — Release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html) — Airflow 2 vs 3 compatibility
- [Airflow providers index](https://airflow.apache.org/docs/apache-airflow-providers/) — 1500+ community operators/hooks

## Primary docs (docs.dagster.io) — for contrast
- [Dagster — Software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets) — asset model, lineage, materializations
- [Dagster — Asset checks](https://docs.dagster.io/concepts/assets/asset-checks) — data-quality tied to assets (no direct Airflow equivalent)
- [Dagster — Partitions](https://docs.dagster.io/concepts/partitions-schedules-sensors/partitions) — partition-keyed asset materialization

## Primary docs (managed Airflow)
- [AWS MWAA — What is Amazon MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html) — managed Airflow on AWS
- [Google Cloud Composer overview](https://cloud.google.com/composer/docs/concepts/overview) — managed Airflow on GCP

## Internal course references
- Phase 3 Dagster module (`../../phase_3_core_tools/06_dagster/`) — covers the Dagster asset graph (ingestion, transformation, quality) that Lab L5b ports to Airflow
- [Dagster — Software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets) — dlt ingestion and dbt build as Dagster assets
- [Dagster — Asset checks](https://docs.dagster.io/concepts/assets/asset-checks) — Dagster quality checks; the thing Airflow has no direct equivalent for

## Books
- *Fundamentals of Data Engineering*, Reis & Housley, Ch. 8 — orchestration chapter contrasts DAG-of-tasks vs asset-oriented systems
