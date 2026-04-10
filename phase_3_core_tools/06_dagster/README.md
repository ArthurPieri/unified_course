# Module 06: Dagster — Asset-centric orchestration (8h)

> Dagster's thesis: declare the **assets** that exist in your platform (a table, a file, an ML model) and Dagster works out how to compute, schedule, monitor, and validate them. You do not write tasks; you write asset definitions, and the task graph falls out of the dependencies.

## Learning goals
- Define a software-defined asset with `@asset` and wire upstream dependencies via function argument names.
- Distinguish the **asset graph** from a task graph and say when each one is the right model.
- Use **resources** and **IO managers** to keep assets free of connection and persistence code.
- Wrap a dlt pipeline with `dagster-dlt` and a dbt project with `@dbt_assets` so that lineage crosses tools automatically.
- Write an `@asset_check` and reason about freshness checks as the quality layer over the asset graph.
- Run the webserver + daemon from the Phase 3 compose stack and materialize assets from both the UI and the CLI.

## Prerequisites
- `phase_3_core_tools/04_dlt/` (the dlt pipeline this module wraps)
- `phase_3_core_tools/05_dbt/` (the dbt project this module wraps)
- `phase_3_core_tools/compose/full-stack/` up and healthy (Dagster service at `:3000`)

## Reading order
1. This README
2. `labs/lab_L3d_dagster_orchestrate/README.md`
3. `quiz.md`

## Concepts

### Asset-centric orchestration
A Dagster **asset** is a named, persistent artefact your platform owns — a table, a file, a dashboard. You declare the asset with `@asset` and a function that produces it; Dagster stores the definition, tracks its lineage, computes a run plan when you ask for materialization, and records the result. The contrast with task-centric schedulers is the object the scheduler keeps track of: Airflow tracks task runs and leaves the data as a side effect; Dagster tracks asset versions and derives the tasks from them. For a compact counterpoint see Phase 5 `03_airflow_bridge` — same pipeline, task-graph lens.
Ref: [Dagster — Software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets)

### `@asset` and the asset graph
```python
@asset
def raw_taxi() -> None: ...

@asset
def staging_taxi(raw_taxi) -> None: ...
```
The function name is the asset key. Upstream dependencies are inferred from parameter names — `staging_taxi(raw_taxi)` declares an edge `raw_taxi → staging_taxi`. Dagster composes every asset in a code location into a single **asset graph** that you can browse in the UI. The run plan for "materialize `mart_taxi`" is "materialize its upstream ancestors in topological order, then `mart_taxi`". See the ingestion pattern in `../dataeng/dagster/lakehouse/assets/ingestion.py:L1-L58`.
Ref: [Dagster — Asset definitions](https://docs.dagster.io/concepts/assets/asset-definitions) · [Asset graph](https://docs.dagster.io/concepts/webserver/ui#asset-graph)

### Resources
Resources are the reusable, configurable dependencies assets need at runtime — a dbt CLI handle, a dlt pipeline factory, a Trino connection, an S3 client. They are declared once at the `Definitions(...)` level and injected into assets by name, which keeps connection strings and credentials out of the asset body and makes the asset easy to test with a stub. The sibling project defines one resource per tool under `../dataeng/dagster/lakehouse/resources/` (`dlt_resource.py`, `dbt_resource.py`, `trino_resource.py`) — each wraps a single external system.
Ref: [Dagster — Resources](https://docs.dagster.io/concepts/resources)

### IO managers
An **IO manager** owns the "how do I store and load the output of this asset?" decision. The default IO manager pickles to the local filesystem under `$DAGSTER_HOME/storage/`, which is fine for in-memory Python objects but wrong for a multi-million-row table. For lakehouse assets you either (a) write the data yourself inside the asset (dlt/dbt do this — the asset body is a side-effecting call, the IO manager stores only metadata) or (b) attach a table-aware IO manager that writes to Iceberg. The `@dbt_assets` and `build_dlt_assets` integrations take approach (a): the dbt model materializes the table; Dagster records the metadata.
Ref: [Dagster — IO managers](https://docs.dagster.io/concepts/io-management/io-managers)

### Jobs, schedules, sensors
A **job** is a named selection of assets to materialize together; the default job `__ASSET_JOB` covers every asset, and you can define narrower ones with `define_asset_job("daily_taxi", selection=["raw_taxi", "staging_taxi", "mart_taxi"])`. A **schedule** fires a job on a cron. A **sensor** fires a job in response to an external event — a new object in MinIO, an upstream freshness violation, a webhook. Schedules and sensors are evaluated by the **daemon** process; the **webserver** serves the UI and GraphQL API. Both processes run out of the Dagster service block in `phase_3_core_tools/compose/full-stack/docker-compose.yml:L189-L222`.
Ref: [Dagster — Schedules](https://docs.dagster.io/concepts/automation/schedules) · [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors)

### Partitions (one-line intro)
A partitioned asset has one materialization per partition key; the overwhelmingly common case is a `DailyPartitionsDefinition(start_date="2024-01-01")` so each day's data is tracked, backfilled, and retried independently.
Ref: [Dagster — Partitions](https://docs.dagster.io/concepts/partitions-schedules-sensors/partitions)

### Asset checks
An `@asset_check` is a named assertion that runs after (or alongside) an asset materialization and reports `passed`/`failed` against that specific asset version. It is the natural home for the row-count, null-rate, and referential checks from Phase 2 `04_data_quality`: the check lives next to the asset, is visible in the UI, and blocks downstream materializations when wired with `blocking=True`. A **freshness check** is a specialised asset check that fails when an asset has not been materialized within a declared window — the Phase 4 observability forward-reference. The sibling project's quality checks pattern lives in `../dataeng/dagster/lakehouse/assets/quality.py:L11-L71`.
Ref: [Dagster — Asset checks](https://docs.dagster.io/concepts/assets/asset-checks) · [Freshness checks](https://docs.dagster.io/concepts/assets/asset-checks#freshness-checks)

### `dagster-dlt`: wrapping a dlt pipeline
The `dagster-dlt` integration turns a dlt pipeline into a set of Dagster assets: one asset per dlt resource, dependencies following the dlt source graph, and the dlt `load_info` surfaced as asset metadata. The entry point is `build_dlt_assets(dlt_source=..., dlt_pipeline=...)` (or the `@dlt_assets` decorator on the translator pattern). This is how you avoid re-implementing the taxi pipeline as a hand-written `@asset` — you declare it once in dlt and let the integration lift it. See the concrete pattern in `../dataeng/dagster/lakehouse/assets/ingestion.py:L1-L58`.
Ref: [Dagster — dagster-dlt](https://docs.dagster.io/integrations/dlt)

### `dagster-dbt`: wrapping a dbt project
`@dbt_assets(manifest=Path(".../manifest.json"))` reads the compiled dbt manifest and emits one Dagster asset per dbt model, with the model-to-model lineage exactly as dbt sees it. Calling `dbt.cli(["build"], context=context).stream()` inside the asset body runs the selected models and streams results back as Dagster events. Because both dlt and dbt assets live in the same code location, Dagster stitches the lineage across tools — `raw_taxi` (dlt) flows into `staging_taxi` and `mart_taxi` (dbt) in one graph. See `../dataeng/dagster/lakehouse/assets/transformation.py:L1-L42` for the manifest-driven pattern and `../dataeng/dagster/lakehouse/resources/dbt_resource.py` for the resource wiring.
Ref: [Dagster — dagster-dbt](https://docs.dagster.io/integrations/dbt)

### Webserver, daemon, CLI
Three entry points matter in the Phase 3 compose:
- `dagster-webserver -h 0.0.0.0 -p 3000 -w workspace.yaml` — the UI on `:3000` and the GraphQL API.
- `dagster-daemon run` — evaluates schedules, sensors, and run queues. The UI will not auto-trigger anything without it.
- `dagster asset materialize --select <asset_key> -m <module>` — the CLI equivalent of clicking "Materialize" in the UI. Used in the lab.
All three are pinned on the 1.9.x line in the compose and share `$DAGSTER_HOME=/opt/dagster/dagster_home`.
Ref: [Dagster — Webserver](https://docs.dagster.io/deployment/dagster-webserver) · [Daemon](https://docs.dagster.io/deployment/dagster-daemon) · [CLI reference](https://docs.dagster.io/_apidocs/cli)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L3d_dagster_orchestrate` | Wrap the Phase 3 dlt + dbt pipeline as three Dagster assets, materialize from UI and CLI, add an `@asset_check` | 75m | [labs/lab_L3d_dagster_orchestrate/](labs/lab_L3d_dagster_orchestrate/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Code location fails to load with `ModuleNotFoundError` in the UI | `workspace.yaml` points at a module the image cannot import | Match the `python_module` value to the package name installed in the image; verify with `dagster definitions validate` | [Dagster — Workspace files](https://docs.dagster.io/concepts/code-locations/workspace-files) |
| `Resource 'dbt' required by asset not found` | Asset uses `dbt: DbtCliResource` but `Definitions(resources=...)` is missing the key | Add `resources={"dbt": DbtCliResource(project_dir=...)}` to the `Definitions` call | `../dataeng/dagster/lakehouse/resources/dbt_resource.py` |
| dbt assets show but "Materialize" does nothing | dbt project path inside the container differs from host path | Mount the dbt project into the Dagster image and point `project_dir` at the container path | [Dagster — dbt project config](https://docs.dagster.io/integrations/dbt/reference) |
| Schedules never fire | Daemon not running | `docker compose ps dagster-daemon`; restart the service | [Daemon](https://docs.dagster.io/deployment/dagster-daemon) |
| Asset check appears but never runs | Check is defined but not attached to the asset (`asset=` missing) or not selected in the run | Pass `asset=<asset_key>` to `@asset_check` and use "Materialize with checks" | [Asset checks](https://docs.dagster.io/concepts/assets/asset-checks) |
| `dagster asset materialize` errors with "no definitions found" | `-m` module path wrong | Use the fully qualified module that defines `defs = Definitions(...)` | [CLI — asset](https://docs.dagster.io/_apidocs/cli#dagster-asset) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Explain in two sentences why Dagster tracks assets instead of tasks and what that buys you.
- [ ] Point at the three assets in `labs/lab_L3d_dagster_orchestrate/assets.py` and name their upstream/downstream edges.
- [ ] Materialize `mart_taxi` from the UI and from `dagster asset materialize`, and find the run in the Runs tab.
- [ ] Write an `@asset_check` that fails when `staging_taxi` has zero rows, and see it surface in the asset's right-hand panel.
- [ ] State what the webserver does, what the daemon does, and which one you need for a cron schedule to fire.
