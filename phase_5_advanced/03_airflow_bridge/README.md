# Module 03: Airflow Bridge — Crossing Over From Dagster (6h)

> You already orchestrate with Dagster in Phase 3, but most existing data platforms — especially at large shops, on AWS MWAA, or on Astronomer — still run Apache Airflow. This module is a fast bridge: Airflow's mental model, how it differs from Dagster's asset-first paradigm, and the concrete porting exercise (Lab L5b) that forces you to translate a working Dagster asset graph into an Airflow DAG.

## Learning goals
- Describe Airflow's core runtime: DAGs, tasks, operators, scheduler, executor, metadata DB
- Explain why Airflow is process-centric (tasks) while Dagster is data-centric (assets), and what that means for lineage and freshness
- Write a simple DAG using the TaskFlow API, including dependencies and XComs
- Use Connections to hold credentials instead of hard-coding them
- Identify the top-level-code pitfall and task-level state pitfall, and fix both
- Decide when Airflow is still the right answer (MWAA, Astronomer, existing Airflow at a large shop)

## Prerequisites
- [../../phase_3_core_tools/05_dagster/](../../phase_3_core_tools/05_dagster/) — asset-based orchestration with Dagster (the "before" side of Lab L5b)
- [../../phase_1_foundations/04_docker/](../../phase_1_foundations/04_docker/) — Compose, for the standalone Airflow container
- [../../phase_3_core_tools/03_dbt/](../../phase_3_core_tools/03_dbt/) — dbt CLI invocation (the `transform` task calls it)

## Reading order
1. This README
2. [labs/lab_L5b_airflow_dag/README.md](labs/lab_L5b_airflow_dag/README.md)
3. [quiz.md](quiz.md)

## Concepts

### Airflow's mental model: DAG + tasks + operators + scheduler + executor
An Airflow **DAG** is a Python object that declares a directed acyclic graph of **tasks**. Each task is an instance of an **operator** — `PythonOperator`, `BashOperator`, `KubernetesPodOperator`, etc. — or a `@task`-decorated function under the TaskFlow API. The **scheduler** parses DAG files, computes the next run, and sends tasks to the **executor** (Local, Celery, Kubernetes) which actually runs them on workers. A **metadata database** (usually Postgres) stores DAG runs, task instances, XComs, connections, and variables. Every UI view and every CLI command reads from that same metadata DB.
Ref: [Airflow — Core Concepts / DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) · [Airflow — Architecture overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)

### TaskFlow API vs classic operators
The **TaskFlow API** (added in Airflow 2.0) lets you write tasks as plain Python functions decorated with `@task`, and dependencies as normal function calls: `transform(ingest())`. Return values become XCom pushes and function arguments become XCom pulls — no `ti.xcom_push` boilerplate. The **classic operator** style instantiates operator objects and chains them with `>>` / `set_downstream()`; it is what most older DAGs still use, and it is still the only option for some third-party operators. The two styles interoperate inside a single DAG.
Ref: [Airflow — TaskFlow](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html) · [Airflow — Operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html)

### Dagster vs Airflow: assets versus tasks
Dagster's primary noun is the **asset** — a named, versioned artifact (a table, a file, an ML model) that a function produces and that the system tracks in a catalog with lineage, freshness, and code versions baked in. Airflow's primary noun is the **task** — a unit of work with no first-class notion of what it produces. Airflow added **Datasets** (Airflow 2.4) to give a task-to-data dependency, but the catalog, checks, and partitioned asset graph are still Dagster-native concepts. Practically: in Dagster you declare "this asset exists and here's how to compute it"; in Airflow you declare "run this task on this schedule and here's what it depends on." That shift matters most when you care about lineage, backfills keyed on data partitions, and data-quality checks tied to the asset itself.
Ref: [Dagster — Assets](https://docs.dagster.io/concepts/assets/software-defined-assets) · [Airflow — Datasets and data-aware scheduling](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html)

### When Airflow is still the right answer
Airflow's gravity is huge: managed offerings (**AWS MWAA**, **Google Cloud Composer**, **Astronomer**), a 10+ year operator ecosystem (1500+ community providers), and an installed base that means "the team already runs Airflow" is the default at most large employers. If you are joining a shop that already runs Airflow, you port to Airflow — you do not pitch replacing it. Greenfield projects and data-centric teams lean Dagster; process orchestration across heterogeneous systems leans Airflow.
Ref: [AWS MWAA — What is MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html) · [Airflow providers index](https://airflow.apache.org/docs/apache-airflow-providers/)

### Connections and XComs
A **Connection** is a named credential/endpoint record stored in the metadata DB (optionally backed by a secrets backend like AWS Secrets Manager). Operators reference them by `conn_id` — `PostgresOperator(conn_id="warehouse_pg", ...)` — so credentials never live in DAG files. **XCom** ("cross-communication") is the mechanism tasks use to pass small values between each other; under TaskFlow, it's automatic. XCom is not a data-transport layer — push a pointer (a path, a key, a row count), not a dataframe. The default XCom backend stores JSON in the metadata DB and is limited to small values; for larger payloads you configure a custom XCom backend backed by S3/GCS.
Ref: [Airflow — Connections](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html) · [Airflow — XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)

### Common pitfall: top-level code in DAG files
The scheduler re-parses every DAG file on a loop (default every 30 seconds). Any code at the top level of a DAG file — an API call, a DB query, a `pandas.read_csv` — runs on every parse, hammering whatever it touches and slowing scheduler throughput. The fix is to move anything expensive **inside** a task function so it runs only when the task runs. Airflow's own "best practices" page calls this out as the #1 mistake.
Ref: [Airflow — Best Practices: top-level code](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#top-level-python-code)

### Common pitfall: task-level state and non-idempotent tasks
Tasks can retry, and backfills replay historical runs. If a task mutates external state without an idempotency key (e.g., `INSERT` without `ON CONFLICT`, or appending to a file keyed only on current time), you get duplicates on every retry. Airflow's design assumes tasks are idempotent when keyed on the **logical date** (`{{ ds }}` / `{{ data_interval_start }}`); use that macro as the partition key in your writes, and design inserts as upserts.
Ref: [Airflow — Best Practices: deterministic + idempotent tasks](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#deterministic-and-idempotent) · [Airflow — Templates reference](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)

### Airflow 2 vs 3 — a note, not a deep dive
Airflow 3 (released 2025) changes the task execution model to a task-server API (tasks run in isolated workers over HTTP instead of sharing the metadata DB connection), adds a new React-based UI, and makes DAG versioning and backfills first-class. Most DAG code written for Airflow 2.x still runs on 3. Do not pin to 3 in production until your provider packages catch up; the Airflow release-notes page tracks the compatibility matrix.
Ref: [Airflow release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L5b_airflow_dag` | Port the Dagster lakehouse asset graph (dlt → dbt → check) to an Airflow TaskFlow DAG; write a 1-page comparison | 120m | [labs/lab_L5b_airflow_dag/](labs/lab_L5b_airflow_dag/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Scheduler CPU pegged, parse times >30s | Expensive top-level code in DAG files | Move work into task bodies; keep module-level imports cheap | [Best Practices — top-level code](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#top-level-python-code) |
| Duplicate rows after a retry | Task is non-idempotent | Key writes on `{{ data_interval_start }}`; use upserts | [Best Practices — idempotent](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#deterministic-and-idempotent) |
| `XCom value exceeds max size` | Pushing a dataframe through XCom | Push a pointer (S3 URI, row count) and read the data in the next task | [XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html) |
| DAG does not appear in UI | File not under `$AIRFLOW_HOME/dags/`, or import error | Check `airflow dags list-import-errors` | [DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) |
| Credentials hard-coded in DAG file | No Connection configured | Create a Connection via UI or `airflow connections add`, reference by `conn_id` | [Connections](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Draw Airflow's runtime: scheduler → executor → workers, with the metadata DB in the middle
- [ ] Explain to a teammate the one-sentence difference between a Dagster asset and an Airflow task
- [ ] Write a TaskFlow DAG with three dependent tasks and a `schedule='@daily'`
- [ ] Point at a line of DAG code and say "that will run on every scheduler parse — move it"
- [ ] Name two scenarios where you would recommend Airflow over Dagster
