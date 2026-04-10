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

## Reused sibling sources (cited with line ranges)
- `../../../dataeng/dbt_project/tests/assert_positive_revenue.sql:L1-L10` — singular test example
- `../../../dataeng/dbt_project/unit_tests/test_revenue_calculation.yml:L1-L81` — unit test example (fixture rows + expected output)
- `../../../dataeng/dagster/lakehouse/assets/quality.py:L11-L15` — silver table list used by `check_row_counts`
- `../../../dataeng/dagster/lakehouse/assets/quality.py:L18-L42` — `check_revenue_positive` asset check
- `../../../dataeng/dagster/lakehouse/assets/quality.py:L45-L71` — `check_row_counts` asset check

## Cross-course index
- `references/docs.md:L55-L57` — dbt docs and model contracts entry
- `references/glossary.md:L75-L80` — "Data contract" and "Schema evolution" entries
