# Lab L5b: Port a Dagster Asset Graph to an Airflow DAG

## Goal
Take the working Dagster lakehouse asset graph (dlt → dbt → quality) from `../../../../../dataeng/dagster/lakehouse/assets/`, port it to an Airflow TaskFlow DAG (`dag_example.py` in this directory), run it on a local Airflow, and write a 1-page comparison of the two paradigms.

## Prerequisites
- Docker + Compose v2
- Completed [../../../phase_3_core_tools/06_dagster/](../../../phase_3_core_tools/06_dagster/) (you know the "before" asset graph)
- The Dagster source files, read for reference: `../../../../../dataeng/dagster/lakehouse/assets/ingestion.py:L1-L58`, `transformation.py:L1-L42`, and `quality.py`

## Setup

Option A — **Airflow standalone** (fastest, single process):

```bash
mkdir -p ~/airflow-lab && cd ~/airflow-lab
python -m venv .venv && source .venv/bin/activate
pip install "apache-airflow==2.10.*" --constraint \
  "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.11.txt"
export AIRFLOW_HOME="$PWD/airflow_home"
airflow standalone   # prints an admin password; leave it running
```

Option B — **docker-compose** (closer to production), following [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html):

```bash
mkdir -p ~/airflow-lab && cd ~/airflow-lab
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up -d
```

## Steps

1. Copy `dag_example.py` from this lab into the Airflow DAGs folder.
   ```bash
   cp /path/to/unified_course/phase_5_advanced/03_airflow_bridge/labs/lab_L5b_airflow_dag/dag_example.py \
      "$AIRFLOW_HOME/dags/"       # standalone
   # or, for compose:
   cp .../dag_example.py ./dags/
   ```

2. Confirm there are no import errors.
   ```bash
   airflow dags list-import-errors
   ```
   Expected output: empty.

3. Open the UI at `http://localhost:8080`, find the `lakehouse_taxi_daily` DAG, and unpause it with the toggle.

4. Trigger a manual run.
   ```bash
   airflow dags trigger lakehouse_taxi_daily
   ```

5. Watch the grid view until all three tasks (`ingest`, `transform`, `quality_check`) are green.

## Verify
- [ ] `airflow dags list-import-errors` reports no errors on `dag_example.py`
- [ ] A manual run finishes with all 3 tasks `success` in the UI grid view
- [ ] The `transform` task's log shows `dbt build` output
- [ ] Pausing and re-triggering the DAG does not produce duplicate rows in the warehouse (idempotency check)

## Cleanup
```bash
# standalone
pkill -f "airflow standalone"
# compose
docker compose down -v
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `airflow: command not found` | Activate the venv: `source .venv/bin/activate` |
| DAG missing from UI | Check `airflow dags list-import-errors`; common cause: `taxi_pipeline` not on `PYTHONPATH` — add via `AIRFLOW__CORE__DAGBAG_IMPORT_ERROR_TRACEBACKS=True` and inspect the log |
| `dbt: command not found` in the `transform` task | `pip install dbt-core dbt-trino` into the Airflow environment (or bake it into a custom image) |
| Scheduler pegged at 100% CPU | Search the DAG file for top-level code — move heavy imports/queries inside task bodies ([Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#top-level-python-code)) |

## Stretch goals
- Add a `BranchPythonOperator` (classic style) after `ingest` that routes to `transform` only when `rows_loaded > 0`, and to a `skip_transform` EmptyOperator otherwise. Confirm the two styles interoperate in one DAG.
- Replace the inline assertion in `quality_check` with an `SQLCheckOperator` against the Trino gold table, using an Airflow Connection with `conn_id=trino_gold`. Configure the connection via `airflow connections add`.
- Swap the `schedule='@daily'` for a data-aware schedule using Datasets, so that `transform` only runs when `ingest` has produced a new dataset version. Note what this gets you that stock Airflow scheduling does not.

## Comparison writeup (deliverable — commit as `COMPARISON.md` next to this README)

Write 5–10 bullets covering these diffs, citing `../../../../../dataeng/dagster/lakehouse/assets/` line ranges for "before" and Airflow docs for "after":

- **Primary noun.** Dagster names the *asset* produced; Airflow names the *task* that runs.
- **Data-quality checks.** Dagster has first-class asset checks (`../../../../../dataeng/dagster/lakehouse/assets/quality.py`) — Airflow has no direct equivalent; use inline asserts or `SQLCheckOperator`.
- **Freshness SLAs.** Per-asset in Dagster; closest Airflow analog is per-task SLAs + [Datasets](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html).
- **Partitioning.** Dagster partitions are asset-keyed; Airflow partitions are implicit in `{{ data_interval_start }}`.
- **Lineage.** Dagster infers it from code; Airflow relies on Datasets or OpenLineage.
- **Local dev loop.** `dagster dev` hot-reloads; `airflow standalone` restarts slower.
- **Operator ecosystem.** Airflow wins — 1500+ providers.
- **When to pick Airflow.** Existing Airflow shops, MWAA/Composer/Astronomer mandates, heterogeneous process orchestration.

## References
See `../../references.md` (module-level).
