"""Lab L5b — Airflow port of the Dagster lakehouse asset graph.

Ports the Dagster assets in
    ../../../../../dataeng/dagster/lakehouse/assets/ingestion.py       (dlt taxi ingest)
    ../../../../../dataeng/dagster/lakehouse/assets/transformation.py  (dbt build)
    ../../../../../dataeng/dagster/lakehouse/assets/quality.py         (asset checks)
to an Airflow TaskFlow DAG with three tasks: ingest -> transform -> quality_check.

Docs:
    TaskFlow API:  https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html
    Best practices: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html

Drop this file into $AIRFLOW_HOME/dags/ (or the ./dags/ bind mount of the compose setup).
"""

from __future__ import annotations

from datetime import datetime

from airflow.decorators import dag, task

# NOTE: keep module-level code cheap. Heavy imports (dlt, dbt) go inside tasks,
# so the scheduler does not pay the cost on every DAG-file parse.
# See: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#top-level-python-code

DEFAULT_ARGS = {
    "owner": "data-eng",
    "retries": 2,
}


@dag(
    dag_id="lakehouse_taxi_daily",
    description="Port of the Dagster lakehouse asset graph: dlt -> dbt -> quality check.",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["lab", "l5b", "lakehouse"],
)
def lakehouse_taxi_daily():
    @task
    def ingest(data_interval_start=None) -> dict:
        """Run the dlt taxi pipeline. Mirrors ingestion.py::taxi_ingestion_assets."""
        import dlt  # local import — keeps DAG parse fast

        from taxi_pipeline import taxi_trips_source  # type: ignore[import-not-found]

        pipeline = dlt.pipeline(
            pipeline_name="taxi_ingestion",
            destination="filesystem",
            dataset_name="raw_taxi",
        )
        info = pipeline.run(taxi_trips_source())
        # Return a small pointer payload — NOT the data itself. XComs are for small values.
        # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html
        return {
            "dataset": "raw_taxi",
            "logical_date": str(data_interval_start),
            "rows_loaded": sum(
                p.metrics.get("job_metrics", {}).get("rows_count", 0)
                for p in info.load_packages
            ),
        }

    @task
    def transform(ingest_info: dict) -> dict:
        """Run `dbt build`. Mirrors transformation.py::dbt_lakehouse_assets."""
        import subprocess

        result = subprocess.run(
            ["dbt", "build", "--profiles-dir", "/opt/airflow/dbt", "--project-dir", "/opt/airflow/dbt"],
            check=True,
            capture_output=True,
            text=True,
        )
        return {
            "source_rows": ingest_info["rows_loaded"],
            "dbt_stdout_tail": result.stdout.strip().splitlines()[-5:],
        }

    @task
    def quality_check(transform_info: dict) -> None:
        """Final gate. In Dagster this would be an asset check; Airflow has no direct
        equivalent, so we assert inline and fail the task on bad data."""
        if transform_info["source_rows"] <= 0:
            raise ValueError(
                f"No rows landed by the ingest task: {transform_info}. "
                "Failing the DAG so downstream consumers do not see an empty partition."
            )

    # Dependencies are declared by calling tasks as functions — TaskFlow infers the DAG edges.
    quality_check(transform(ingest()))


dag = lakehouse_taxi_daily()
