# Module 04: Data Quality — References

## dbt docs (docs.getdbt.com)
- [Add data tests to your DAG](https://docs.getdbt.com/docs/build/data-tests) — tests overview, generic vs. singular
- [Generic data tests](https://docs.getdbt.com/docs/build/data-tests#generic-data-tests) — `unique`, `not_null`, `accepted_values`, `relationships`
- [Singular data tests](https://docs.getdbt.com/docs/build/data-tests#singular-data-tests) — standalone SQL in `tests/`
- [Unit tests](https://docs.getdbt.com/docs/build/unit-tests) — CI-time tests with fixture rows, added in dbt 1.8
- [Test configurations (severity)](https://docs.getdbt.com/reference/resource-configs/severity) — `error` vs. `warn`, `warn_if`, `error_if`
- [Model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts) — enforced column names, types, constraints at build time
- [Source freshness](https://docs.getdbt.com/docs/build/sources#snapshotting-source-data-freshness) — `dbt source freshness`
- [Best practice workflows](https://docs.getdbt.com/best-practices/best-practice-workflows) — CI/CD and slim CI

## Dagster docs (docs.dagster.io)
- [Asset checks](https://docs.dagster.io/concepts/assets/asset-checks) — `@asset_check`, `AssetCheckResult`, UI integration
- [Freshness checks](https://docs.dagster.io/concepts/assets/asset-checks/checking-for-data-freshness) — `build_last_update_freshness_checks`, `build_time_partition_freshness_checks`
- [Testing assets](https://docs.dagster.io/concepts/testing) — unit-testing assets in Python

## Great Expectations docs (docs.greatexpectations.io)
- [Core concepts — Introduction](https://docs.greatexpectations.io/docs/core/introduction/) — Expectations, Validators, Data Docs
- [Expectations gallery](https://greatexpectations.io/expectations/) — catalog of built-in expectations

## Canonical books
- *Fundamentals of Data Engineering*, Reis & Housley, O'Reilly 2022 — Ch. 10 (undercurrent: data management, quality framing)

## Working patterns (based on the companion lakehouse project)
- Singular test: a SQL file that selects rows from `fct_daily_revenue` where `total_revenue < 0` (zero rows = pass). See [dbt — Singular data tests](https://docs.getdbt.com/docs/build/data-tests#singular-data-tests).
- Unit test: a YAML file feeding fixture rows into `fct_daily_revenue` and asserting aggregated output. See [dbt — Unit tests](https://docs.getdbt.com/docs/build/unit-tests).
- `check_revenue_positive` asset check: queries Trino for negative revenue rows, passes iff count is zero. See [Dagster — Asset checks](https://docs.dagster.io/concepts/assets/asset-checks).
- `check_row_counts` asset check: loops over silver tables and fails if any is empty. See [Dagster — Asset checks](https://docs.dagster.io/concepts/assets/asset-checks).

## Cross-course index
- `references/docs.md:L55-L57` — dbt docs and model contracts entry
- `references/glossary.md:L75-L80` — "Data contract" and "Schema evolution" entries
