# Lab L3d: Orchestrate the Phase 3 pipeline as Dagster assets

## Goal
Wrap the Phase 3 dlt + dbt taxi pipeline as three Dagster software-defined assets (`raw_taxi`, `staging_taxi`, `mart_taxi`), materialize them from both the UI and the CLI, browse the asset graph, and add a row-count `@asset_check` on the staging asset.

## Prerequisites
- Phase 3 full-stack compose running: `phase_3_core_tools/compose/full-stack/` (MinIO, HMS, Trino, Dagster webserver + daemon all healthy).
- Lab L3b (`04_dlt`) completed — the dlt pipeline module is importable.
- Lab L3c (`05_dbt`) completed — `dbt_project/` has a compiled `target/manifest.json`.
- Python 3.11+ with `dagster==1.9.*`, `dagster-webserver`, `dagster-dlt`, `dagster-dbt` installed in the lab venv.

## Setup
```bash
cd phase_3_core_tools/compose/full-stack
docker compose up -d dagster-db dagster-webserver dagster-daemon
docker compose ps | grep dagster

# Local venv for CLI runs (matches the image's dagster line)
cd ../../06_dagster/labs/lab_L3d_dagster_orchestrate
uv venv && source .venv/bin/activate
uv pip install 'dagster==1.9.*' dagster-webserver dagster-dlt dagster-dbt 'dbt-trino>=1.8'

# Point at the sibling dlt pipeline and dbt project
export DLT_PIPELINE_MODULE=phase_3_core_tools.04_dlt.labs.lab_L3b_dlt_ingest.pipeline
export DBT_PROJECT_DIR=$(pwd)/../../../05_dbt/labs/lab_L3c_dbt_models/dbt_project
export DBT_PROFILES_DIR=$DBT_PROJECT_DIR
export DAGSTER_HOME=$(pwd)/.dagster_home && mkdir -p "$DAGSTER_HOME"

# Compile dbt so @dbt_assets has a manifest to read
(cd "$DBT_PROJECT_DIR" && dbt parse)
```

## Steps
1. Validate the code location loads.
   ```bash
   dagster definitions validate -m assets
   ```
   Expected: `Validation successful for code location assets.`

2. Open the UI on `http://localhost:3000`, open **Assets → Asset graph**, and confirm three nodes with edges `raw_taxi → staging_taxi → mart_taxi`.

3. Materialize `mart_taxi` from the UI. Click the node, press **Materialize**, and watch the run surface `raw_taxi` and `staging_taxi` first. Open the run page and confirm all three assets are green.

4. Materialize from the CLI as an alternative entry point:
   ```bash
   dagster asset materialize --select mart_taxi -m assets
   ```
   Expected tail:
   ```
   RUN_SUCCESS - Finished execution of run ...
   ```

5. Trigger the asset check. In the UI, open `staging_taxi`, click the **Checks** tab, and run `staging_taxi_row_count`. Expected: `PASSED` with `num_rows > 0` in the metadata. Then, to see a failure, truncate the staging table in Trino and re-run the check.

## Verify
- [ ] `dagster definitions validate -m assets` succeeds.
- [ ] The asset graph in the UI shows all three assets with the correct lineage.
- [ ] `mart_taxi` materializes both from the UI and from `dagster asset materialize`.
- [ ] The `staging_taxi_row_count` check is visible on the staging asset and can be executed.
- [ ] The daemon process shows "Schedules: 0, Sensors: 0" but is `RUNNING` in the UI's **Deployment → Daemons** page.

## Cleanup
```bash
rm -rf "$DAGSTER_HOME"
cd phase_3_core_tools/compose/full-stack
docker compose stop dagster-webserver dagster-daemon
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: assets` | Run the `dagster` commands from the lab directory so `assets.py` is on `sys.path`. |
| `DagsterInvalidDefinitionError: resource 'dbt' required` | Confirm `Definitions(resources=...)` in `assets.py` includes both `dlt` and `dbt` keys. |
| `@dbt_assets` shows 0 assets | Re-run `dbt parse` in `$DBT_PROJECT_DIR`; the manifest was stale or missing. |
| UI shows `raw_taxi` but no edge to `staging_taxi` | dbt model does not `{{ ref('raw_taxi') }}` — add the ref or use a source. |
| `dagster asset materialize` says "no definitions found" | `-m` must be the module that exports `defs = Definitions(...)` — here, `assets`. |

## Stretch goals
- Add a `DailyPartitionsDefinition` to `raw_taxi` and backfill three days.
- Add a schedule with `define_asset_job("daily_taxi", selection="*mart_taxi")` and a `@schedule` cron.
- Wire the check with `blocking=True` and observe that a failed check stops `mart_taxi` from materializing.

## References
See `../../references.md` (module-level).
