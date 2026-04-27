
# Module 05: dbt — References

## Patterns (based on the companion lakehouse project)
- Canonical project wiring: layer-to-schema mapping (`staging → silver`, `marts → gold`), layer-specific materializations in `dbt_project.yml`. Ref: [dbt — dbt_project.yml](https://docs.getdbt.com/reference/dbt_project.yml).
- `dbt-trino` profile targeting the local compose Trino (`type: trino`, `method: none`, catalog `iceberg`). See the lab's `profiles.yml.example`. Ref: [dbt — Trino setup](https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup).
- `sources:` declaration with freshness SLA on the `_dlt_load_id` load marker. Ref: [dbt — Source freshness](https://docs.getdbt.com/docs/build/sources#snapshotting-source-data-freshness).
- Incremental staging pattern: `config(materialized='incremental', unique_key='trip_id', on_schema_change='append_new_columns')` + `is_incremental()` guard. Ref: [dbt — Incremental models](https://docs.getdbt.com/docs/build/incremental-models).
- Rename/cast-only staging body. See the lab's `models/staging/stg_taxi_trips.sql`.
- Intermediate join/enrichment layer consumed by marts. See the lab's `models/intermediate/int_taxi_hourly.sql`.
- Fact table reading from an intermediate via `ref()`; `group by` aggregation pattern. See the lab's `models/marts/fct_taxi_hourly.sql`.
- Generic tests attached to columns: `not_null`, `unique`, `accepted_values`. See the lab's `models/schema.yml`. Ref: [dbt — Data tests](https://docs.getdbt.com/docs/build/data-tests).
- Singular test: returns rows where a metric is invalid. See the lab's `tests/assert_nonneg_trip_count.sql`.
- dbt 1.8 unit-test pattern (forward reference; Phase 2 Module 04 owns unit tests). Ref: [dbt — Unit tests](https://docs.getdbt.com/docs/build/unit-tests).
- Custom schema-naming macro (stretch-goal reference). Ref: [dbt — Custom schema names](https://docs.getdbt.com/docs/build/custom-schemas).

## Official dbt docs (docs.getdbt.com)
- [About dbt projects](https://docs.getdbt.com/docs/build/projects) — project structure and the role of `dbt_project.yml`.
- [dbt_project.yml reference](https://docs.getdbt.com/reference/dbt_project.yml) — every key, including per-path model config.
- [profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml) — connection file layout and target selection.
- [Models](https://docs.getdbt.com/docs/build/models) — `.sql` file semantics, Jinja, `config()`.
- [Materializations](https://docs.getdbt.com/docs/build/materializations) — `view`, `table`, `incremental`, `ephemeral`.
- [Incremental models](https://docs.getdbt.com/docs/build/incremental-models) — `is_incremental()`, `unique_key`, `on_schema_change`.
- [Sources](https://docs.getdbt.com/docs/build/sources) — `source()` function and `sources.yml`.
- [Source freshness](https://docs.getdbt.com/docs/build/sources#snapshotting-source-data-freshness) — `loaded_at_field`, `warn_after` / `error_after`.
- [ref function](https://docs.getdbt.com/reference/dbt-jinja-functions/ref) — DAG construction rule.
- [Data tests](https://docs.getdbt.com/docs/build/data-tests) — generic + singular tests.
- [Unit tests](https://docs.getdbt.com/docs/build/unit-tests) — mocked-input tests introduced in dbt 1.8.
- [Seeds](https://docs.getdbt.com/docs/build/seeds) — CSV-loaded reference tables.
- [Snapshots](https://docs.getdbt.com/docs/build/snapshots) — SCD Type 2 captures.
- [Packages](https://docs.getdbt.com/docs/build/packages) — `packages.yml` and `dbt deps`.
- [dbt build](https://docs.getdbt.com/reference/commands/build) — run + test in DAG order.
- [dbt run](https://docs.getdbt.com/reference/commands/run) — model-only execution.
- [dbt test](https://docs.getdbt.com/reference/commands/test) — test-only execution.
- [How we structure our dbt projects](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) — staging → intermediate → marts convention.
- [Trino setup (dbt-trino)](https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup) — adapter profile keys and auth methods.

## Destination / engine docs
- [Trino — Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) — table properties (`format`, `partitioning`) that dbt-trino forwards.
- [dbt-trino releases](https://github.com/starburstdata/dbt-trino/releases) — version-pinning reference for the `dbt-core` / `dbt-trino` minor match.

## Compose context
- `phase_3_core_tools/compose/full-stack/docker-compose.yml:L105-L125` — the Trino service the dbt lab connects to.
- `phase_3_core_tools/04_dlt/` — upstream module that lands the `raw_taxi.yellow_taxi_trips` source the lab reads from.
- `phase_2_core_domain/04_data_quality/` — owns broader data-quality theory; forward reference for unit-test patterns.
