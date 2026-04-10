
# Module 05: dbt — SQL-first transformation (8h)

> The **T** in ELT. You write `SELECT` statements; dbt compiles them into a DAG, runs them in order against your warehouse/query engine, and runs tests against the results. No Python, no orchestration — just SQL plus a YAML config.

## Learning goals
- Explain dbt's thesis (version-controlled, tested, documented SQL) and lay out a project directory without looking it up.
- Distinguish `source()` from `ref()` and explain why `ref()` builds the DAG automatically.
- Pick the right materialization (`view`, `table`, `incremental`, `ephemeral`) for a given model.
- Write a staging → intermediate → mart layer with generic (`unique`, `not_null`) and singular tests.
- Configure the `dbt-trino` adapter against the Phase 3 full-stack compose and materialize models as Iceberg tables.
- Debug `dbt build` failures: missing `ref`, circular deps, schema mismatch, wrong target, adapter-version drift.

## Prerequisites
- `phase_3_core_tools/00_stack_overview/`
- `phase_3_core_tools/01_minio_iceberg_hms/`
- `phase_3_core_tools/02_trino/` (dbt will talk to this Trino)
- `phase_3_core_tools/04_dlt/` (source tables the lab reads from)

## Reading order
1. This README
2. `labs/lab_L3c_dbt_models/README.md`
3. `quiz.md`

## Concepts

### Thesis: SQL, but version-controlled
dbt's proposition is that the transformation layer of an ELT pipeline should be plain SQL in git, with the same review, test, and CI discipline as application code. Every model is a `SELECT`; dbt wraps it in `CREATE TABLE AS` / `CREATE VIEW AS` and runs it against your target adapter. Tests are also SQL — a query that returns rows is a test failure. The runtime is a CLI (`dbt run`, `dbt test`, `dbt build`), so it drops into any scheduler (cron, Airflow, Dagster) without its own server.
Ref: [dbt — About dbt projects](https://docs.getdbt.com/docs/build/projects)

### Project layout
A dbt project is a directory with `dbt_project.yml` at the root and a handful of subdirectories whose names are wired in that YAML:
- `models/` — one `.sql` file per model, organised by layer (`staging/`, `intermediate/`, `marts/`). Each `.sql` is a single `SELECT`.
- `tests/` — singular tests: one `.sql` file per assertion, any query returning rows is a failure.
- `seeds/` — small CSVs loaded via `dbt seed` as reference tables.
- `snapshots/` — SCD Type 2 captures via `dbt snapshot` (Phase 2 owns the modelling; dbt owns the mechanism).
- `macros/` — Jinja helpers reused across models.
- `dbt_project.yml` — declares `name`, `profile`, path overrides, and per-path model defaults.
- `profiles.yml` — connection config. Lives outside the project by default (`~/.dbt/profiles.yml`) so secrets stay out of git.

The canonical reuse reference is `../dataeng/dbt_project/dbt_project.yml:L1-L27`, which wires `staging → silver`, `intermediate → silver`, `marts → gold` with layer-specific materializations.
Refs: [dbt — dbt_project.yml](https://docs.getdbt.com/reference/dbt_project.yml) · [dbt — profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml)

### `source()` vs `ref()` and the DAG
`{{ source('raw_taxi', 'yellow_taxi_trips') }}` points at a table that dbt did **not** create — it's the edge of your world, usually a raw landing table from dlt or Fivetran. You declare it in a `sources.yml` with its catalog/schema/table. `{{ ref('stg_taxi_trips') }}` points at a model this project builds. dbt parses every `ref()` call, turns the edges into a graph, and executes models in topological order. You never hand-write run order — it falls out of `ref`. Circular refs fail at parse time. See `../dataeng/dbt_project/models/sources.yml:L1-L27` for the source declaration pattern and `../dataeng/dbt_project/models/marts/fct_trip_metrics.sql:L1-L5` for `ref` in action.
Ref: [dbt — ref function](https://docs.getdbt.com/reference/dbt-jinja-functions/ref) · [dbt — Sources](https://docs.getdbt.com/docs/build/sources)

### Materializations
A materialization is *how* dbt persists a model. Set it via `{{ config(materialized='...') }}` at the top of the `.sql` file or as a default in `dbt_project.yml`.
- `view` — a `CREATE OR REPLACE VIEW`. Cheap to build, slow to query, always fresh. Default for staging when compute is free.
- `table` — a `CREATE TABLE AS`. Full rebuild every run. Default for marts.
- `incremental` — first run builds the full table; later runs insert/merge only new rows matched by `{% if is_incremental() %}` + a `unique_key`. Used for large append-only sources. `../dataeng/dbt_project/models/staging/stg_taxi_trips.sql:L1-L20` is the canonical pattern: `config(materialized='incremental', unique_key='trip_id')` plus a `where pickup_datetime > (select max(pickup_datetime) from {{ this }})` guard.
- `ephemeral` — dbt inlines the model as a CTE into whatever refs it; no object in the warehouse. Use sparingly — it complicates debugging because the SQL only exists at compile time.
Ref: [dbt — Materializations](https://docs.getdbt.com/docs/build/materializations)

### Staging → intermediate → marts
The layering convention (sometimes called the "Fishtown layout") is:
- **Staging** — one model per source table. Renames, casts, light cleanup. One-to-one with `sources.yml`. Usually `view` or `incremental`.
- **Intermediate** — joins and enrichment that are useful to multiple marts but not consumed directly by BI. `table` materialization. See `../dataeng/dbt_project/models/intermediate/int_trips_enriched.sql:L1-L52`.
- **Marts** — business-grain facts and dimensions. `table`, often partitioned. Consumed by Metabase / notebooks. See `../dataeng/dbt_project/models/marts/fct_trip_metrics.sql:L1-L31`.

The convention is worth following because it gives reviewers a predictable place to look and keeps `ref` chains shallow. The lab for this module builds one file per layer end-to-end.
Ref: [dbt — How we structure our dbt projects](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)

### Tests: generic and singular
dbt has two kinds of data tests.
- **Generic tests** are parameterised and attached to columns in a `schema.yml`. The four built-ins are `unique`, `not_null`, `accepted_values`, and `relationships` (foreign-key style). See `../dataeng/dbt_project/models/marts/_marts__models.yml:L8-L18` for `not_null` + `accepted_values`, and `L67-L73` for `unique` + `not_null` on a dimension surrogate key.
- **Singular tests** are one-off SQL files under `tests/`. Any query that returns rows counts as a failure. `../dataeng/dbt_project/tests/assert_positive_revenue.sql:L1-L9` is the canonical example: it selects rows from `fct_daily_revenue` where `total_revenue < 0`.

Phase 2, Module 04 (`phase_2_core_domain/04_data_quality/`) owns the broader data-quality theory and also introduces **unit tests** (YAML-declared, run against mocked inputs) which dbt added in 1.8 — see `../dataeng/dbt_project/unit_tests/test_revenue_calculation.yml:L1-L80`. In this phase we stay tool-focused: you need to know when to reach for each.
Ref: [dbt — Data tests](https://docs.getdbt.com/docs/build/data-tests) · [dbt — Unit tests](https://docs.getdbt.com/docs/build/unit-tests)

### Sources and freshness
A `sources.yml` entry can declare a `freshness` SLA: `warn_after: {count: 48, period: hour}` plus a `loaded_at_field`. `dbt source freshness` then issues a `max(loaded_at_field)` query and compares it to wall-clock. Failing freshness is a lightweight **input SLA** — it tells you "dlt stopped landing data" before a downstream mart goes stale. `../dataeng/dbt_project/models/sources.yml:L10-L17` uses `_dlt_load_id` as the freshness field, bridging directly to the dlt module.
Ref: [dbt — Source freshness](https://docs.getdbt.com/docs/build/sources#snapshotting-source-data-freshness)

### `dbt build` = run + test in DAG order
`dbt run` builds models. `dbt test` runs tests. `dbt build` does both, interleaved: it runs a model, then runs its tests, and if the tests fail it short-circuits the downstream DAG. For any pipeline that will be orchestrated from Dagster or Airflow, `dbt build` is the default command because it guarantees you never publish a mart whose upstream tests failed. `dbt run --select state:modified+` is the Slim-CI pattern — only rebuild what changed plus its descendants.
Ref: [dbt — dbt build](https://docs.getdbt.com/reference/commands/build)

### dbt-trino specifics
The `dbt-trino` adapter connects to Trino over HTTP. A minimal `profiles.yml` target needs `type: trino`, `method`, `host`, `port`, `user`, `database` (the Trino *catalog*), and `schema`. See `../dataeng/dbt_project/profiles.yml:L1-L12`: `method: none` is the no-auth local path against the compose stack's Trino at `localhost:8080`, catalog `iceberg`, schema `silver`.

Against the Iceberg catalog, a `table` materialization issues `CREATE TABLE ... WITH (...)`; you can pass Trino-Iceberg table properties via the model config, for example `{{ config(materialized='table', properties={'format': "'PARQUET'"}) }}` to force Parquet file format. Because the underlying storage is Iceberg on MinIO (Phase 3 compose, `docker-compose.yml:L105-L125` for the Trino service), `dbt run` effectively writes Parquet data files into `s3://lakehouse/` and registers snapshots through the Hive Metastore. Adapter version must match dbt-core major: dbt-core 1.8.x needs dbt-trino 1.8.x — mismatches usually surface as `AttributeError` on `adapter.get_relation`.
Refs: [dbt — Trino setup](https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup) · [Trino — Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L3c_dbt_models` | Scaffold a dbt project against the Phase 3 Trino, build staging → intermediate → mart with generic + singular tests, `dbt build` to green | 90m | [labs/lab_L3c_dbt_models/](labs/lab_L3c_dbt_models/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `Compilation Error ... depends on a node named 'X' which was not found` | Model SQL hard-codes a table name instead of using `ref()` | Replace the literal with `{{ ref('X') }}`; dbt cannot graph raw identifiers | [dbt — ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref) |
| `Found a cycle in the graph` | Two models `ref` each other | Break the cycle by moving shared logic into an intermediate model | [dbt — Projects](https://docs.getdbt.com/docs/build/projects) |
| `Column X not found` on 2nd incremental run | Upstream schema drifted; `on_schema_change` default is `ignore` | Set `on_schema_change='append_new_columns'` as in `../dataeng/dbt_project/models/staging/stg_taxi_trips.sql:L1-L7` | [dbt — Incremental models](https://docs.getdbt.com/docs/build/incremental-models) |
| `dbt run` writes to the wrong schema | Wrong `--target`; default target is whatever `profiles.yml` says | Pass `--target prod` explicitly in CI; keep `dev` as the default | [dbt — profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml) |
| `AttributeError` from the adapter on first run | dbt-core and dbt-trino minor versions drifted | Pin both in `requirements.txt` to the same minor (e.g. `dbt-core==1.8.*`, `dbt-trino==1.8.*`) | [dbt-trino releases](https://github.com/starburstdata/dbt-trino/releases) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Sketch the four required directories of a dbt project and name the file that wires them.
- [ ] Explain in one sentence why `ref()` exists instead of writing the schema-qualified table name.
- [ ] Pick the right materialization for (a) a small lookup, (b) a 2B-row event feed, (c) a daily revenue mart.
- [ ] Write a singular test that fails when `fct_taxi_hourly.trip_count < 0`.
- [ ] Run `dbt build` against the Phase 3 compose and see a non-zero row count from Trino on `iceberg.gold.fct_taxi_hourly`.
- [ ] Diagnose a "wrong target" failure by reading `dbt --debug run` output.
