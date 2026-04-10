# Module 04: Data Quality — Tests, Contracts, and Checks (8h)

> Partial-reuse module. Reuses three working artifacts from `../dataeng/`: a dbt singular test, a dbt unit test, and Dagster asset checks. Concept scaffolding is written from primary docs (dbt, Dagster, Great Expectations) and *Fundamentals of Data Engineering* framing.

## Learning goals
- Name the six classic classes of data-quality issues and give one concrete test for each
- Write a dbt generic test (`unique`, `not_null`, `accepted_values`, `relationships`) in a `schema.yml`, and a dbt singular test as a standalone SQL file
- Explain the difference between a dbt **data test** (runtime, on real data) and a dbt **unit test** (CI-time, on fixture rows)
- Add a Dagster `@asset_check` and attach a `FreshnessPolicy` / freshness check to an asset
- Justify using a dbt **model contract** as a preventive control rather than a reactive test
- Decide whether a quality failure should `error`, `warn`, or just log — and whether to place the gate at CI-time, runtime, or post-deployment

## Prerequisites
- [`../02_etl_elt_patterns/`](../02_etl_elt_patterns/) — pipeline boundaries and idempotency
- Working dbt + Dagster setup (covered in Phase 3); this module is conceptual and can be completed before Phase 3 if the learner accepts the lab as "read and annotate" rather than "run"

## Reading order
1. This README
2. `../dataeng/dbt_project/tests/assert_positive_revenue.sql` — a real singular test
3. `../dataeng/dbt_project/unit_tests/test_revenue_calculation.yml` — a real unit test
4. `../dataeng/dagster/lakehouse/assets/quality.py` — real Dagster asset checks
5. [`quiz.md`](quiz.md)

## Concepts

### The six classes of quality issues
Data-quality writing conventionally groups problems into six **dimensions**, each answerable with a different kind of test:

1. **Completeness** — are required values present? Test: `not_null`, `COUNT(*)` vs. expected row count.
2. **Uniqueness** — are primary/business keys unique? Test: `unique`, `count(distinct k) = count(k)`.
3. **Validity** — do values match a domain or format? Test: `accepted_values`, regex, type/range check.
4. **Consistency** — do related values agree across tables? Test: `relationships` (foreign key), cross-table reconciliation.
5. **Timeliness / freshness** — is the data recent enough? Test: max timestamp within SLA window.
6. **Accuracy** — does the value match reality? Hardest to test automatically; usually needs a trusted reference set.

These six categories are the vocabulary used by Great Expectations ([Expectations gallery](https://greatexpectations.io/expectations/)) and are the organising frame used in *Fundamentals of Data Engineering*, Reis & Housley, Ch. 10. You will not find a tool that tests "accuracy" out of the box — accuracy tests are always bespoke.

### Tests as code: dbt generic tests
In dbt, **generic tests** (formerly "schema tests") are the four built-in assertions you attach to columns or models in a YAML file: `unique`, `not_null`, `accepted_values`, and `relationships`. Ref: [dbt — Add tests to your DAG](https://docs.getdbt.com/docs/build/data-tests) and [Generic data tests](https://docs.getdbt.com/docs/build/data-tests#generic-data-tests).

```yaml
# models/marts/schema.yml
models:
  - name: fct_trip_metrics
    columns:
      - name: trip_id
        data_tests:
          - unique
          - not_null
      - name: payment_type
        data_tests:
          - accepted_values:
              values: [1, 2, 3, 4]
      - name: pickup_zone_id
        data_tests:
          - relationships:
              to: ref('dim_zones')
              field: zone_id
```

A generic test compiles to a `SELECT` that should return **zero rows** if the assertion holds. `dbt test` runs every compiled test and fails the command if any returns rows.

### Singular tests
When a generic test is not enough, dbt lets you drop a SQL file under `tests/` that returns the offending rows. This is a **singular test**. Ref: [dbt — Singular data tests](https://docs.getdbt.com/docs/build/data-tests#singular-data-tests).

The working example in this stack is `../dataeng/dbt_project/tests/assert_positive_revenue.sql:L1-L10` — it selects rows from `fct_daily_revenue` where `total_revenue < 0`. Any row returned fails the test, halting the run before the mart is exposed downstream.

### Unit tests — CI-time, on fixture rows
dbt **unit tests** (added in dbt Core 1.8) test transformation logic against **static input rows** defined in YAML, not against whatever happens to be in the warehouse today. They answer "does the SQL correctly transform this input into that output?" and they run in CI before deployment. Ref: [dbt — Unit tests](https://docs.getdbt.com/docs/build/unit-tests).

The working example: `../dataeng/dbt_project/unit_tests/test_revenue_calculation.yml:L1-L81` feeds three fixture rows of `int_trips_enriched` into `fct_daily_revenue` and asserts two aggregated output rows. Because inputs and outputs are inline, this test is deterministic and fast — it belongs in CI.

A data test answers "is today's data OK?"; a unit test answers "does the SQL still compute the right thing?". You need both.

### Dagster asset checks
Dagster models quality as **asset checks**: functions decorated with `@dg.asset_check(asset=...)` that run against a declared asset and emit an `AssetCheckResult(passed=...)` with metadata. Asset checks are first-class in the UI and can block downstream materialization. Ref: [Dagster — Asset checks](https://docs.dagster.io/concepts/assets/asset-checks).

The working example is `../dataeng/dagster/lakehouse/assets/quality.py:L18-L71`. Two checks run against the `dbt_lakehouse` multi-asset:
- `check_revenue_positive` (`:L18-L42`) queries Trino for rows with `total_revenue <= 0` and passes iff the count is zero — the exact same assertion as the dbt singular test, but expressed at the orchestrator layer so the UI shows pass/fail per run.
- `check_row_counts` (`:L45-L71`) loops over three silver tables and fails if any is empty.

Dagster also provides **freshness checks**: `build_last_update_freshness_checks` and `build_time_partition_freshness_checks` produce asset checks that fail when an asset has not been materialized within an SLA. Ref: [Dagster — Freshness checks](https://docs.dagster.io/concepts/assets/asset-checks/checking-for-data-freshness). Use them to catch **silent staleness** — the pipeline "succeeded" but the source stopped sending data.

### Contracts: preventive controls, not reactive tests
Every test discussed so far runs **after** data has been written. A **model contract** runs **before**: dbt enforces the declared column names, types, and constraints at build time, and fails the build if the model's SELECT would produce a different shape. Ref: [dbt — Model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts) (also indexed at `references/docs.md:L56`).

```yaml
models:
  - name: fct_daily_revenue
    config:
      contract:
        enforced: true
    columns:
      - name: revenue_date
        data_type: date
        constraints: [{ type: not_null }]
      - name: total_revenue
        data_type: double
```

A contract turns a downstream consumer's schema assumption into a **producer-enforced invariant**. It is the cheapest control to operate, because violations fail `dbt build` instead of leaking into a dashboard.

### Runtime vs CI-time vs post-deployment gates
The same assertion can live in three very different places:

| Gate | Runs when | Example | Failure cost |
|---|---|---|---|
| **CI-time** | On every PR, before merge | dbt unit tests, `dbt build --select state:modified --defer` on a slim CI dataset | Low — nothing shipped yet |
| **Runtime** | Inside the pipeline, during materialization | dbt generic/singular tests, Dagster asset checks, model contracts | Medium — pipeline halts, stale data remains visible |
| **Post-deployment** | After data is live | Freshness checks, reconciliation jobs, Great Expectations scheduled runs | High — consumers may have already read bad data |

Push assertions **as far left** as they will go. A contract beats a runtime test; a runtime test beats a post-deployment alert. Great Expectations positions itself for the post-deployment case and for non-dbt stacks — see [GX — Core concepts](https://docs.greatexpectations.io/docs/core/introduction/).

### Fail vs warn vs log
dbt tests support a `severity` of `error` or `warn` and a `warn_if` / `error_if` threshold. Ref: [dbt — Test configurations](https://docs.getdbt.com/reference/resource-configs/severity).

- **Fail (error)** when the downstream consumer would be actively misled — nulls in a join key, negative revenue, broken FK. Halt the pipeline.
- **Warn** when the condition is a symptom to investigate but the data is still usable — e.g., row count dropped more than 20% day-over-day.
- **Log only** when the metric is informational — e.g., cardinality histograms stored for later drift analysis.

The rule of thumb: **if a human needs to take action before the next consumer reads the table, fail. Otherwise, warn.** Warnings that nobody reads are worse than no warning at all, because they train the team to ignore the quality system.

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_04_data_quality` (Phase 3) | Add generic + singular + unit tests + one Dagster asset check to `fct_daily_revenue` | 90m | covered alongside Phase 3 · 05_dbt and 06_dagster labs |

> This module is conceptual. The hands-on practice is threaded into the Phase 3 dbt and Dagster labs, so the learner exercises the same tests against the real lakehouse stack.

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `dbt test` is green but a dashboard shows stale numbers | No freshness check; tests only assert shape, not recency | Add a Dagster freshness check or a `dbt source freshness` block | [Dagster freshness checks](https://docs.dagster.io/concepts/assets/asset-checks/checking-for-data-freshness) |
| Unit test passes locally, data test fails in prod | Fixture rows don't cover a real edge case | Add the offending row as a new `given:` case | [dbt unit tests](https://docs.getdbt.com/docs/build/unit-tests) |
| Every PR triggers a full `dbt test` against prod | CI is running data tests instead of unit tests | Split CI: unit tests + `dbt build --select state:modified` on a slim dataset | [dbt — Best practices for CI](https://docs.getdbt.com/best-practices/best-practice-workflows) |
| Contract change silently breaks a downstream mart | Producer ignored the contract; no `enforced: true` | Set `contract: { enforced: true }` on the model | [dbt model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts) |
| Asset check reports pass but Trino query returns rows | Wrong asset attached to `@asset_check(asset=...)` | Point the check at the materializing asset, not an upstream one | `../dataeng/dagster/lakehouse/assets/quality.py:L18-L42` |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Name the six quality dimensions and give one test type per dimension
- [ ] Write a `schema.yml` block with `unique`, `not_null`, `accepted_values`, and `relationships` tests
- [ ] Explain when to reach for a singular test vs. a generic test
- [ ] Contrast a dbt data test and a dbt unit test in one sentence each
- [ ] Read `../dataeng/dagster/lakehouse/assets/quality.py:L18-L71` and describe what each check asserts
- [ ] Justify enforcing a dbt contract instead of adding another runtime test
- [ ] Place a given assertion at CI-time, runtime, or post-deployment and defend the choice
