# Module 06: Dagster — Quiz

10 multiple-choice questions. Answer key at the bottom.

---

**1.** What is the defining difference between Dagster's asset-centric model and a task-centric orchestrator like Airflow?
- A. Dagster has a prettier UI.
- B. Dagster tracks named, persistent artefacts (assets) and derives the task graph from their dependencies; Airflow tracks task runs and leaves the data as a side effect.
- C. Dagster cannot run Python — only YAML definitions.
- D. Airflow supports schedules and Dagster does not.

**2.** In a `@asset` function body `def staging_taxi(raw_taxi): ...`, how does Dagster know `raw_taxi` is an upstream dependency?
- A. Dagster scans the file for SQL strings.
- B. The function-parameter name is matched against other asset keys in the code location.
- C. You must declare it in a separate YAML file.
- D. Dagster infers it from the asset's IO manager.

**3.** The default Dagster IO manager pickles asset outputs to the local filesystem. Why do `@dbt_assets` and `build_dlt_assets` not rely on that behaviour?
- A. They disable IO managers entirely and nothing is stored.
- B. The asset body itself writes the table (dbt/dlt materializes it); Dagster only stores metadata and the IO manager is not used for the row data.
- C. They store the full Parquet file in Dagster's run storage.
- D. They require a custom cloudpickle subclass.

**4.** Which process must be running for a Dagster schedule to actually fire?
- A. `dagster-webserver` alone.
- B. `dagster-daemon`.
- C. The dbt CLI.
- D. The Hive Metastore.

**5.** You write `@dbt_assets(manifest=Path("target/manifest.json"))` and point a `DbtCliResource(project_dir=...)` at the dbt project. What does Dagster emit?
- A. One asset for the entire dbt project.
- B. One Dagster asset per dbt model, with dependencies matching dbt's `ref()` graph.
- C. A single job with no assets.
- D. One asset per dbt source only.

**6.** `build_dlt_assets(dlt_source=..., dlt_pipeline=...)` from `dagster-dlt` produces:
- A. A single asset named after the dlt pipeline.
- B. One asset per dlt resource in the source, wired to the dlt load graph, with `load_info` attached as metadata.
- C. A dbt model.
- D. A sensor that fires on dlt state changes.

**7.** `@asset_check(asset="staging_taxi")` returns `AssetCheckResult(passed=False)`. With `blocking=True`, what happens to downstream assets in the same run?
- A. They materialize anyway — asset checks are advisory.
- B. They are skipped; the blocking check failure stops downstream materialization in that run.
- C. The entire code location is disabled.
- D. The daemon restarts.

**8.** Which statement about resources is correct?
- A. Resources are global singletons configured in `workspace.yaml`.
- B. Resources are declared on `Definitions(resources=...)`, injected into assets by keyword name, and keep connection/credential code out of the asset body.
- C. Resources can only be used by sensors, not assets.
- D. Each asset must define its own resource inline.

**9.** A learner runs `dagster asset materialize --select mart_taxi -m lakehouse` and sees "no definitions found". The most likely cause is:
- A. The daemon is stopped.
- B. The `-m` module path does not resolve to a Python module that exports `defs = Definitions(...)`.
- C. The dbt manifest is stale.
- D. MinIO is down.

**10.** In the sibling reference, `../dataeng/dagster/lakehouse/assets/quality.py:L11-L71` shows:
- A. A dbt profile YAML.
- B. An `@asset_check` pattern that queries the materialized table (via the Trino resource) and asserts a row-count / null-rate condition.
- C. A schedule definition.
- D. An Iceberg compaction job.

---

## Answer key
1. **B** — asset-centric vs task-centric is the thesis; see [Software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets).
2. **B** — parameter names are matched against asset keys in the code location.
3. **B** — the asset body materializes the table; the IO manager only records metadata.
4. **B** — the daemon evaluates schedules and sensors; the webserver alone will not fire them.
5. **B** — `@dbt_assets` emits one Dagster asset per dbt model, with dependencies from the manifest.
6. **B** — one asset per dlt resource, with the dlt `load_info` surfaced as metadata.
7. **B** — blocking check failures stop downstream asset materialization in the same run.
8. **B** — resources are declared on `Definitions(...)` and injected by name.
9. **B** — the `-m` argument must be an importable module that exports `defs`.
10. **B** — `quality.py:L11-L71` is the row-count / null-rate `@asset_check` pattern used as the lab reference.
