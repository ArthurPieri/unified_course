# 01 Data Modeling — Quiz

12 multiple-choice questions. Answers and source citations at the bottom.

---

**1. Which statement best describes the difference between OLTP and OLAP workloads?**
A. OLTP uses columnar storage; OLAP uses row storage.
B. OLTP runs many small transactions against a normalized schema; OLAP runs fewer large scans against a denormalized schema.
C. OLTP and OLAP are two names for the same workload on different hardware.
D. OLTP forbids foreign keys; OLAP requires them.

**2. A table is in 3NF when:**
A. Every column is atomic.
B. Every non-key column depends on the whole primary key and only on the key (no transitive dependencies).
C. All foreign keys are indexed.
D. The table has no nullable columns.

**3. In Kimball's four-step dimensional design process, which step comes first?**
A. Identify the dimensions.
B. Identify the facts (measurements).
C. Declare the grain.
D. Select the business process.

**4. A fact table stores `account_balance` with one row per account per day. This fact is:**
A. Fully additive across all dimensions.
B. Semi-additive — additive across accounts but not across time.
C. Non-additive — cannot be aggregated.
D. Additive only if converted to a percentage.

**5. You need to track a customer's address changes so that historical orders always join to the address that was current at the time of the order. Which SCD type fits?**
A. Type 0
B. Type 1
C. Type 2
D. Type 3

**6. When is SCD Type 3 (a `prior_value` column) appropriate?**
A. When unlimited history is required.
B. When users only need the current and the immediately previous value.
C. When the attribute never changes.
D. When the dimension has no natural key.

**7. A snowflake schema differs from a star schema because:**
A. It has more fact tables.
B. Its dimensions are normalized into sub-dimensions instead of denormalized.
C. It has no foreign keys.
D. It uses only surrogate keys.

**8. In Kimball's bus architecture, a "conformed dimension" is:**
A. A dimension that has been compressed to save space.
B. A dimension that means the same thing — same grain, same keys, same semantics — in every fact table that uses it.
C. A dimension stored outside the warehouse.
D. A dimension with no history.

**9. The central object types in Data Vault 2.0 are:**
A. Fact, dimension, bridge.
B. Hub, link, satellite.
C. Staging, core, mart.
D. Source, sink, transform.

**10. A sale for customer 42 arrives today with an event timestamp of three weeks ago. Customer 42's address has since changed and the change is recorded as a new SCD Type 2 row. Which row should the fact join to?**
A. The row where `is_current = true`.
B. The SCD2 row whose `[valid_from, valid_to)` interval contains the event timestamp.
C. Any row — SCD2 joins ignore the timestamp.
D. Both rows, and average the result.

**11. Which of the following is the strongest argument for choosing Data Vault 2.0 over a Kimball star schema as the warehouse core?**
A. It produces simpler SQL for BI users.
B. It requires fewer tables than a star schema.
C. It provides insert-only, source-tagged history and makes integrating multiple heterogeneous sources auditable.
D. It removes the need for slowly changing dimensions.

**12. `fct_trip_metrics.sql` stores `avg_tip_percentage` as a pre-computed average. Why is this column considered non-additive?**
A. Because it is a string.
B. Because averaging an average across further dimensions (e.g., summing across dates) produces an incorrect result; you would need to re-aggregate from the underlying numerator and denominator.
C. Because PostgreSQL cannot sum floats.
D. Because it uses `case when`.

---

## Answer key

1. **B** — OLTP: many small transactions, normalized; OLAP: few large scans, denormalized. *Kimball DW Toolkit, Ch. 1*; *Inmon Building the DW, Ch. 1*.
2. **B** — 3NF forbids transitive dependencies on non-key columns. *Inmon Building the DW, Ch. 3*; [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html).
3. **D** — Select the business process, then declare the grain, then the dimensions, then the facts. *Kimball DW Toolkit, Ch. 1*.
4. **B** — Balances are semi-additive: they roll up across accounts but not across time. *Kimball DW Toolkit, Ch. 1*.
5. **C** — Type 2 adds a new row with `valid_from`/`valid_to`/`is_current`; historical facts join to the row that was current at event time. *Kimball DW Toolkit, Ch. 5*.
6. **B** — Type 3 supports exactly one level of history via a `prior_value` column. *Kimball DW Toolkit, Ch. 5*.
7. **B** — Snowflake normalizes dimensions into sub-dimensions; star keeps them denormalized. *Kimball DW Toolkit, Ch. 1*.
8. **B** — Conformed dimensions have identical grain, keys, and semantics across fact tables, enabling drill-across. *Kimball DW Toolkit, Ch. 3*.
9. **B** — Hub (business keys), link (relationships), satellite (descriptive, time-variant attributes). *Linstedt & Olschimke, Data Vault 2.0, Ch. 2*.
10. **B** — Late-arriving facts must join to the SCD2 row whose validity interval contains the event timestamp, not the currently-current row. *Kimball DW Toolkit, Ch. 5*.
11. **C** — Data Vault's insert-only, hash-keyed, source-tagged design prioritizes auditability and multi-source integration over BI ergonomics. *Linstedt & Olschimke, Data Vault 2.0, Ch. 1*.
12. **B** — Ratios and averages are non-additive; store numerator and denominator and compute the ratio at query time. *Kimball DW Toolkit, Ch. 1*.
