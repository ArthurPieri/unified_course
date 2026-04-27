# Module 06: Dagster — References

## Patterns (based on the companion lakehouse project)
- Canonical `dagster-dlt` wrapping pattern (dlt pipeline as asset). Used as the shape for `raw_taxi` in the lab. Ref: [Dagster — dagster-dlt](https://docs.dagster.io/integrations/dlt).
- `@dbt_assets(manifest=...)` pattern for turning a dbt project into Dagster assets. Shape for `staging_taxi` and `mart_taxi`. Ref: [Dagster — dagster-dbt](https://docs.dagster.io/integrations/dbt).
- `@asset_check` pattern (row-count / null-rate checks attached to specific assets). Shape for the lab's row-count check. Ref: [Dagster — Asset checks](https://docs.dagster.io/concepts/assets/asset-checks).
- Iceberg compaction/optimize job pattern (forward reference, Phase 4 advanced orchestration).
- dlt wrapped as a Dagster resource; used by the lab's `Definitions(resources=...)` block. Ref: [Dagster — Resources](https://docs.dagster.io/concepts/resources).
- `DbtCliResource` wiring, including `project_dir` and `profiles_dir`. Ref: [Dagster — dagster-dbt reference](https://docs.dagster.io/integrations/dbt/reference).
- Trino client resource (used by quality checks).
- Schedule pattern over the asset job. Ref: [Dagster — Schedules](https://docs.dagster.io/concepts/automation/schedules).
- `workspace.yaml` code location wiring (`python_module: lakehouse`). Ref: [Dagster — Workspace files](https://docs.dagster.io/concepts/code-locations/workspace-files).
- Instance config (`dagster.yaml`) with Postgres run storage, schedule storage. Ref: [Dagster — Instance](https://docs.dagster.io/deployment/dagster-instance).
- Pinned `dagster==1.9.*` runtime image for the compose services.
- Asset unit-test pattern with in-memory resources.

## Official Dagster docs (docs.dagster.io)
- [Software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets) — the `@asset` mental model.
- [Asset definitions](https://docs.dagster.io/concepts/assets/asset-definitions) — `@asset`, dependencies via arg names, `AssetKey`.
- [Asset graph in the UI](https://docs.dagster.io/concepts/webserver/ui#asset-graph) — browsing lineage.
- [Resources](https://docs.dagster.io/concepts/resources) — declaring and injecting config/clients.
- [IO managers](https://docs.dagster.io/concepts/io-management/io-managers) — storing and loading asset outputs.
- [Jobs](https://docs.dagster.io/concepts/assets/asset-jobs) — `define_asset_job` and selections.
- [Schedules](https://docs.dagster.io/concepts/automation/schedules) — cron-driven job triggers.
- [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) — event-driven triggers.
- [Partitions](https://docs.dagster.io/concepts/partitions-schedules-sensors/partitions) — `DailyPartitionsDefinition` and friends.
- [Asset checks](https://docs.dagster.io/concepts/assets/asset-checks) — `@asset_check`, blocking behaviour, freshness.
- [dagster-dlt integration](https://docs.dagster.io/integrations/dlt) — `build_dlt_assets`, translator pattern.
- [dagster-dbt integration](https://docs.dagster.io/integrations/dbt) — `@dbt_assets`, manifest loading.
- [dagster-dbt reference](https://docs.dagster.io/integrations/dbt/reference) — `DbtCliResource` options.
- [Workspace files](https://docs.dagster.io/concepts/code-locations/workspace-files) — `workspace.yaml` shape.
- [Webserver deployment](https://docs.dagster.io/deployment/dagster-webserver) — UI + GraphQL process.
- [Daemon deployment](https://docs.dagster.io/deployment/dagster-daemon) — schedules, sensors, run queue.
- [CLI reference](https://docs.dagster.io/_apidocs/cli) — `dagster asset materialize`, `dagster definitions validate`.

## Compose context
- `phase_3_core_tools/compose/full-stack/docker-compose.yml:L169-L222` — `dagster-db`, `dagster-webserver`, `dagster-daemon` service definitions (image, ports, `DAGSTER_HOME`, Postgres env).
- `phase_3_core_tools/compose/full-stack/docker-compose.yml:L105-L125` — Trino catalog used by the dbt models that the Dagster `@dbt_assets` run.

## Forward references
- Phase 4 observability — freshness checks and asset SLAs build on the `@asset_check` introduced here.
- Phase 5 `03_airflow_bridge` — same taxi pipeline expressed as Airflow tasks; the explicit contrast for "asset graph vs task graph".
- Phase 4 advanced orchestration — sensors (e.g. MinIO event sensors) and partitioned backfills. Ref: [Dagster — Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors).
