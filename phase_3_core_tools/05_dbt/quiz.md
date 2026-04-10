
# Module 05: dbt — Quiz

10 multiple-choice questions. Answer key with per-question citations at the bottom.

---

**1.** Which statement best captures dbt's thesis?
- A. dbt is an orchestration engine that schedules Python transformations.
- B. dbt is a SQL compilation layer: every model is a `SELECT`, version-controlled and tested, executed against an adapter.
- C. dbt is an ingestion tool that extracts data from source systems.
- D. dbt is a BI layer that serves dashboards over a semantic model.

**2.** Why does dbt prefer `{{ ref('stg_taxi_trips') }}` over writing `iceberg.silver.stg_taxi_trips` directly?
- A. `ref()` is slightly faster at runtime.
- B. `ref()` registers an edge in the dependency graph, so dbt can run models in topological order and detect cycles.
- C. `ref()` hides the schema so multiple developers can share one target.
- D. `ref()` is required by Trino but not by other adapters.

**3.** Which materialization fits a 2-billion-row append-only event feed where full rebuilds would be too expensive?
- A. `view`
- B. `ephemeral`
- C. `incremental` with a `unique_key` and `is_incremental()` guard
- D. `table` with `+full_refresh: true`

**4.** In `../dataeng/dbt_project/models/sources.yml:L10-L17`, a `freshness` block sets `warn_after: {count: 48, period: hour}` and `loaded_at_field: _dlt_load_id`. What does `dbt source freshness` do with these?
- A. It deletes rows older than 48 hours.
- B. It runs `select max(_dlt_load_id) from <source>` and warns if the result is more than 48 hours behind wall-clock.
- C. It refuses to build models from a source older than 48 hours.
- D. It truncates the source table every 48 hours.

**5.** Which of the following is a **singular** test (as opposed to a generic test)?
- A. `tests: [unique, not_null]` under a column in `schema.yml`.
- B. An `accepted_values` test under a `payment_type` column.
- C. A file at `tests/assert_positive_revenue.sql` whose query returns rows where `total_revenue < 0`.
- D. A unit test in a `.yml` file under `unit_tests/`.

**6.** You run `dbt build` and one test on `stg_taxi_trips` fails. What happens to models downstream of `stg_taxi_trips` in the same invocation?
- A. They run anyway; tests never block runs.
- B. They are skipped because `dbt build` short-circuits downstream of a failing test.
- C. dbt rolls back the entire run, including models that already succeeded.
- D. They run but are marked as "warn".

**7.** The Phase 3 lab configures `profiles.yml` with `type: trino`, `method: none`, `host: localhost`, `port: 8080`, `database: iceberg`, `schema: silver`. What does the `database` key actually point at?
- A. The PostgreSQL database behind Hive Metastore.
- B. The Trino **catalog** name (Trino's top-level namespace, here the Iceberg catalog).
- C. A dbt-internal sqlite file.
- D. The MinIO bucket.

**8.** You add a new column upstream and the next `dbt build` fails with `Column X not found` on an incremental model. What is the minimal fix that keeps history?
- A. Add `--full-refresh` permanently.
- B. Drop the incremental model and rerun.
- C. Set `on_schema_change='append_new_columns'` in the model `config()`, then rerun.
- D. Downgrade dbt-trino.

**9.** Which command combination is **equivalent** to `dbt build` for a single model and its tests?
- A. `dbt run --select my_model` only.
- B. `dbt test --select my_model` only.
- C. `dbt run --select my_model` followed by `dbt test --select my_model`, interleaved per node.
- D. `dbt seed --select my_model`.

**10.** A learner sees `AttributeError: 'TrinoAdapter' object has no attribute 'get_relation_v2'` on first `dbt run`. The most likely cause is:
- A. Missing `packages.yml`.
- B. dbt-core and dbt-trino minor versions are mismatched; pin them to the same minor release.
- C. Trino is not running.
- D. The `ref()` function is misspelled.

---

## Answer key

1. **B** — dbt compiles SQL and runs it against an adapter; it is not an orchestrator, ingestor, or BI tool. Cite: [dbt — About dbt projects](https://docs.getdbt.com/docs/build/projects); module README section "Thesis".
2. **B** — `ref()` builds the DAG automatically; dbt uses it to order runs and detect cycles. Cite: [dbt — ref function](https://docs.getdbt.com/reference/dbt-jinja-functions/ref); `../dataeng/dbt_project/models/marts/fct_trip_metrics.sql:L1-L5`.
3. **C** — incremental with a `unique_key` is the append-only pattern; `../dataeng/dbt_project/models/staging/stg_taxi_trips.sql:L1-L20` is the canonical example. Cite: [dbt — Incremental models](https://docs.getdbt.com/docs/build/incremental-models).
4. **B** — `source freshness` issues a `max(loaded_at_field)` probe and compares it to wall-clock. Cite: [dbt — Source freshness](https://docs.getdbt.com/docs/build/sources#snapshotting-source-data-freshness); `../dataeng/dbt_project/models/sources.yml:L10-L17`.
5. **C** — a singular test is a `.sql` file under `tests/` that fails when its query returns rows. Cite: [dbt — Data tests](https://docs.getdbt.com/docs/build/data-tests); `../dataeng/dbt_project/tests/assert_positive_revenue.sql:L1-L9`.
6. **B** — `dbt build` interleaves run+test and short-circuits the downstream DAG on test failure. Cite: [dbt — dbt build](https://docs.getdbt.com/reference/commands/build).
7. **B** — in the `dbt-trino` adapter the `database` key maps to the Trino catalog. Cite: [dbt — Trino setup](https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup); `../dataeng/dbt_project/profiles.yml:L1-L12`.
8. **C** — `on_schema_change='append_new_columns'` adds the new column in place; used in `../dataeng/dbt_project/models/staging/stg_taxi_trips.sql:L1-L7`. Cite: [dbt — Incremental models](https://docs.getdbt.com/docs/build/incremental-models).
9. **C** — `dbt build` is functionally "run then test, per node, in DAG order". Cite: [dbt — dbt build](https://docs.getdbt.com/reference/commands/build).
10. **B** — adapter/core version drift is the classic `AttributeError` source; pin both to the same minor. Cite: [dbt-trino releases](https://github.com/starburstdata/dbt-trino/releases); module README "dbt-trino specifics".
