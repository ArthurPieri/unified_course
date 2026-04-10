# Quiz — 03_airflow_bridge

Ten multiple-choice questions. Answers at the bottom.

---

**1.** In Airflow, which component is responsible for parsing DAG files and deciding which task instances are ready to run?

A. The executor
B. The worker
C. The scheduler
D. The webserver

**2.** A new teammate writes this at the top of a DAG file: `rows = pd.read_sql("SELECT * FROM events", conn)`. Why is this a problem?

A. Pandas is not allowed in Airflow
B. The scheduler re-parses DAG files on a loop, so this query runs on every parse
C. It will only run once, which is too rare
D. Top-level code is not allowed in Airflow 2

**3.** Which statement about the TaskFlow API is correct?

A. It replaces the scheduler with a reactive task queue
B. It lets you write tasks as `@task`-decorated Python functions with XComs handled implicitly
C. It is only available on Airflow 3
D. It eliminates the need for a metadata database

**4.** You need credentials for a Postgres warehouse inside a task. What is the recommended approach?

A. Hard-code them in the DAG file
B. Put them in a `.env` file committed to the repo
C. Create an Airflow Connection with a `conn_id` and reference it from the operator or hook
D. Pass them through an XCom from a startup task

**5.** A teammate pushes a 200 MB dataframe through XCom and the task fails with `XCom value exceeds max size`. What is the right fix?

A. Increase the XCom size limit
B. Switch to classic operators
C. Write the dataframe to object storage and push only the URI through XCom
D. Serialize the dataframe with pickle

**6.** Which is the *primary* semantic difference between a Dagster asset and an Airflow task?

A. Assets are written in YAML, tasks are written in Python
B. Assets are data-centric (name the artifact produced, with lineage), tasks are process-centric (a unit of work)
C. Assets cannot be scheduled
D. Tasks cannot have dependencies

**7.** A task writes rows to Postgres and is retried after a transient error. Duplicates appear. What is the Airflow-idiomatic fix?

A. Disable retries
B. Make the write idempotent — key on `{{ data_interval_start }}` and use an upsert
C. Move the write to the scheduler
D. Use a `BranchPythonOperator`

**8.** Which scenario is the *strongest* argument for choosing Airflow over Dagster on a new project?

A. You want first-class data lineage and asset checks built into the orchestrator
B. You are joining a team that already runs Airflow at scale on MWAA and has 200+ existing DAGs
C. You want the smallest-footprint local dev loop
D. You primarily care about partition-keyed backfills of tables

**9.** Which Airflow feature most closely resembles (but does not equal) Dagster's asset concept?

A. XComs
B. Connections
C. Datasets and data-aware scheduling
D. SubDAGs

**10.** You are porting a Dagster asset graph with `ingest → transform → check` to Airflow using the TaskFlow API. Which snippet best expresses the dependency?

A. `ingest >> transform >> check`
B. `check(transform(ingest()))`
C. `dag.add_task(ingest); dag.add_task(transform); dag.add_task(check)`
D. `with TaskGroup(): ingest; transform; check`

---

## Answer key

1. **C** — The scheduler parses DAG files and queues runnable tasks; the executor dispatches them to workers. [Architecture overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
2. **B** — Top-level code runs on every DAG-file parse (default every 30s), hammering whatever it touches. Move it inside a task body. [Best Practices — top-level code](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#top-level-python-code)
3. **B** — TaskFlow lets you decorate functions with `@task`; return values become XComs, arguments become XCom pulls. [TaskFlow](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html)
4. **C** — Connections are the canonical credential store, optionally backed by a secrets backend. [Connections](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html)
5. **C** — XComs are for small control values; large payloads go to object storage and XComs carry the pointer. [XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)
6. **B** — Dagster names the artifact (asset) and tracks lineage; Airflow names the work (task). [Dagster assets](https://docs.dagster.io/concepts/assets/software-defined-assets) · [Airflow DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
7. **B** — Idempotency keyed on the logical data interval is the documented Airflow design principle. [Best Practices — idempotent](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#deterministic-and-idempotent)
8. **B** — Airflow's strongest case is the installed base and managed offerings; greenfield data-centric projects lean Dagster. [AWS MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html)
9. **C** — Airflow Datasets enable data-aware scheduling; they are close but lack the catalog/checks model of Dagster assets. [Datasets](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html)
10. **B** — Under TaskFlow, calling a `@task` function returns an XCom reference, and passing it as an argument to the next task creates the dependency implicitly. [TaskFlow](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html)
