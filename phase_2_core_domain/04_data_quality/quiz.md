# Module 04: Data Quality — Exit Quiz

10 multiple-choice questions. Pass mark: 8/10. Answers with primary-source citations at the bottom.

---

**Q1.** A column should never contain `NULL`. Which dbt generic test expresses this?

A. `unique`
B. `not_null`
C. `accepted_values`
D. `relationships`

---

**Q2.** You need to assert that every `pickup_zone_id` in `fct_trip_metrics` corresponds to an existing `zone_id` in `dim_zones`. Which dbt generic test is the right tool?

A. `unique`
B. `accepted_values`
C. `relationships`
D. `not_null`

---

**Q3.** Which statement best describes the difference between a dbt **data test** and a dbt **unit test**?

A. They are synonyms
B. Data tests run against real warehouse data at runtime; unit tests run against inline fixture rows in CI to validate transformation logic
C. Unit tests run against real warehouse data; data tests run against fixture rows
D. Unit tests are only for Python models

---

**Q4.** In the sibling test `../dataeng/dbt_project/tests/assert_positive_revenue.sql`, the SQL selects rows where `total_revenue < 0`. How does dbt decide the test passed or failed?

A. The test fails if the SQL errors out
B. The test passes iff the query returns zero rows
C. The test passes iff `total_revenue` is flagged `not_null`
D. The test always passes; dbt just logs the result

---

**Q5.** Which Dagster feature catches the case where a pipeline "succeeded" but the source stopped delivering new data hours ago?

A. `@asset_check` with a `COUNT(*) > 0` assertion
B. A freshness check (e.g., `build_last_update_freshness_checks`)
C. `dbt source freshness` inside a dbt asset
D. A `retry_policy` on the asset

---

**Q6.** A dbt **model contract** with `enforced: true` fails the build when...

A. A runtime `not_null` test returns a row
B. The model's SELECT would produce a column name, type, or constraint that disagrees with the declared contract
C. A downstream consumer changes their query
D. The warehouse is unreachable

---

**Q7.** You have a single assertion "no negative revenue". Which placement is the strongest preventive control?

A. A scheduled post-deployment Great Expectations run
B. A Dagster asset check after materialization
C. A dbt singular test at runtime
D. A dbt model contract declaring `total_revenue` with a `check` constraint (or the assertion pushed as far left as possible)

---

**Q8.** The six conventional data-quality dimensions are completeness, uniqueness, validity, consistency, timeliness, and...

A. latency
B. accuracy
C. throughput
D. cardinality

---

**Q9.** You want a dbt test to **warn** (not fail) when row count drops slightly, and **fail** only when it drops drastically. Which dbt feature do you configure?

A. `materialized: incremental`
B. `severity` with `warn_if` / `error_if` thresholds
C. `on_schema_change: fail`
D. `persist_docs: true`

---

**Q10.** In `../dataeng/dagster/lakehouse/assets/quality.py`, the `check_row_counts` check iterates over `SILVER_TABLES` and marks the run as failed when...

A. Any silver table has more than 1 million rows
B. Any silver table is empty (row count equals zero)
C. Trino is unreachable
D. The dbt job has not run today

---

## Answer key

1. **B** — `not_null` asserts the column has no nulls. Ref: [dbt generic tests](https://docs.getdbt.com/docs/build/data-tests#generic-data-tests)
2. **C** — `relationships` is dbt's foreign-key test (`to: ref('...')`, `field: ...`). Ref: [dbt generic tests](https://docs.getdbt.com/docs/build/data-tests#generic-data-tests)
3. **B** — Data tests run on real data at runtime; unit tests run on inline fixture rows at CI time. Ref: [dbt unit tests](https://docs.getdbt.com/docs/build/unit-tests)
4. **B** — dbt tests are SELECTs; zero returned rows = pass, any returned rows = fail. Ref: [dbt — Singular data tests](https://docs.getdbt.com/docs/build/data-tests#singular-data-tests); example at `../../../dataeng/dbt_project/tests/assert_positive_revenue.sql:L1-L10`
5. **B** — Freshness checks detect stale assets. Ref: [Dagster freshness checks](https://docs.dagster.io/concepts/assets/asset-checks/checking-for-data-freshness)
6. **B** — Contracts enforce declared shape (columns, types, constraints) at build time. Ref: [dbt model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts)
7. **D** — Push the assertion left: a contract prevents the bad shape before any row is written. Ref: [dbt model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts)
8. **B** — Accuracy is the sixth dimension (and the hardest to test). Ref: *Fundamentals of Data Engineering*, Reis & Housley, Ch. 10
9. **B** — `severity`, `warn_if`, and `error_if` configure warn vs. fail thresholds. Ref: [dbt test severity](https://docs.getdbt.com/reference/resource-configs/severity)
10. **B** — The loop flags any table with `count == 0`. Ref: `../../../dataeng/dagster/lakehouse/assets/quality.py:L54-L65`
