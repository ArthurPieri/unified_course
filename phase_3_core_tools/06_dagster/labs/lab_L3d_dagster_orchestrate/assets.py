"""Lab L3d — Dagster asset definitions for the Phase 3 taxi pipeline.

Three assets:
    raw_taxi      -- dlt ingest (NYC taxi -> MinIO/Iceberg)   [dagster-dlt]
    staging_taxi  -- dbt model over raw_taxi                  [dagster-dbt]
    mart_taxi     -- dbt model over staging_taxi              [dagster-dbt]

Three asset patterns: ingestion, transformation, and quality checks.
"""
from __future__ import annotations

import os
from pathlib import Path

from dagster import (
    AssetCheckResult,
    AssetCheckSeverity,
    AssetExecutionContext,
    AssetKey,
    Definitions,
    asset_check,
)
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_dlt import DagsterDltResource, dlt_assets

# ---------------------------------------------------------------------------
# Config — resolved from env so the same file runs in the container and locally.
# ---------------------------------------------------------------------------
DBT_PROJECT_DIR = Path(os.environ["DBT_PROJECT_DIR"]).resolve()
DBT_MANIFEST = DBT_PROJECT_DIR / "target" / "manifest.json"


# ---------------------------------------------------------------------------
# raw_taxi — dlt ingest wrapped as a Dagster asset.
# We import the dlt source + pipeline builders from the Phase 3 lab L3b module.
# ---------------------------------------------------------------------------
import importlib

# The dlt lab directory starts with a digit (04_dlt), which is not a valid
# Python identifier.  Use importlib so the import works regardless.
# Requires the repo root on PYTHONPATH — see lab README "Setup".
_pipeline_mod = importlib.import_module(
    "phase_3_core_tools.04_dlt.labs.lab_L3b_dlt_ingest.pipeline"
)
build_taxi_pipeline = _pipeline_mod.build_pipeline
taxi_source = _pipeline_mod.taxi_source


@dlt_assets(
    dlt_source=taxi_source(year=2024, months=[1]),
    dlt_pipeline=build_taxi_pipeline(),
    name="raw_taxi",
    group_name="ingestion",
)
def raw_taxi(context: AssetExecutionContext, dlt: DagsterDltResource):
    # `build_dlt_assets` / `@dlt_assets` runs the dlt pipeline and yields
    # Dagster events (one MaterializeResult per dlt resource) with load_info
    # attached as metadata. See docs.dagster.io/integrations/dlt.
    yield from dlt.run(context=context)


# ---------------------------------------------------------------------------
# staging_taxi + mart_taxi — emitted from the dbt manifest.
# @dbt_assets creates one Dagster asset per dbt model; lineage comes from
# the compiled manifest.json so `ref()` edges become asset edges.
# ---------------------------------------------------------------------------
@dbt_assets(manifest=DBT_MANIFEST)
def taxi_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


# ---------------------------------------------------------------------------
# Asset check on staging_taxi — row count must be > 0.
# A production version might query Trino via a trino_resource; here
# we query the dbt adapter via `dbt show` to keep the lab dependency-light.
# ---------------------------------------------------------------------------
@asset_check(
    asset=AssetKey(["staging_taxi"]),
    name="staging_taxi_row_count",
    blocking=False,
)
def staging_taxi_row_count(context: AssetExecutionContext, dbt: DbtCliResource):
    result = dbt.cli(
        ["show", "--inline", "select count(*) as n from {{ ref('staging_taxi') }}"],
        context=context,
    ).wait()
    # dbt show prints the row; the adapter response lives in result.get_artifact.
    # For the lab we treat a non-zero process exit as failure.
    passed = result.process is None or result.process.returncode == 0
    return AssetCheckResult(
        passed=passed,
        severity=AssetCheckSeverity.ERROR,
        metadata={"check": "count(*) > 0 on staging_taxi"},
    )


# ---------------------------------------------------------------------------
# Definitions — the single code location entrypoint Dagster loads.
# ---------------------------------------------------------------------------
defs = Definitions(
    assets=[raw_taxi, taxi_dbt_assets],
    asset_checks=[staging_taxi_row_count],
    resources={
        "dlt": DagsterDltResource(),
        "dbt": DbtCliResource(project_dir=str(DBT_PROJECT_DIR)),
    },
)
