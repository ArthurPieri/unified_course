# Module 01: Data Modeling (14h)

Working-level data modeling for an analytics warehouse: when to normalize, when to denormalize, and how to keep history without rewriting it. The goal is to move between an OLTP source schema and an analytical star schema without guessing, and to know where Inmon's CIF and Data Vault fit when Kimball is not the right hammer.

## Learning goals
- Contrast OLTP and OLAP workloads and explain why they demand different physical layouts.
- Normalize a schema to 3NF and recognize when BCNF matters.
- Design a star schema from a business process: pick the grain, identify the facts, conform the dimensions.
- Choose an SCD type (0/1/2/3/6) for a given dimension attribute and defend the trade-off.
- Contrast Kimball's bus architecture with Inmon's Corporate Information Factory and Data Vault 2.0, and name one scenario where each is the right call.
- Handle late-arriving facts and conformed dimensions without breaking downstream marts.

## Prerequisites
- [`../../phase_1_foundations/05_sql_postgres/`](../../phase_1_foundations/05_sql_postgres/) — SQL DDL, joins, window functions.
- [`../../phase_1_foundations/04_docker/`](../../phase_1_foundations/04_docker/) — running Postgres in a container.

## Reading order
1. This README
2. [`labs/lab_L2_star_schema/README.md`](labs/lab_L2_star_schema/README.md)
3. [`quiz.md`](quiz.md)

## Concepts

### OLTP vs OLAP mental model
OLTP (online transaction processing) systems handle many small, short-lived reads and writes against a highly normalized schema — think order entry, inventory, banking. OLAP (online analytical processing) systems run few, long, scan-heavy queries over denormalized history — think revenue-by-region-by-month. The physical trade-offs differ: OLTP favors row storage, tight locking, and foreign-key integrity; OLAP favors columnar storage, bulk loads, and denormalization so that a single fact table answers most questions with a star join instead of a seven-way normalized join.
Ref: *The Data Warehouse Toolkit*, Kimball & Ross, Ch. 1 · *Building the Data Warehouse*, Inmon, Ch. 1

### Normalization (1NF → 3NF → BCNF)
Normalization removes redundancy so updates cannot leave the database inconsistent. 1NF: atomic columns, no repeating groups. 2NF: every non-key column depends on the **whole** primary key (only meaningful with composite keys). 3NF: no transitive dependencies — non-key columns depend only on the key, not on another non-key column. BCNF is a stricter 3NF that covers the edge case where a non-prime attribute determines part of a candidate key. Operational source systems should be at 3NF; analytical marts deliberately denormalize back.
Ref: [PostgreSQL: Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) · *Building the Data Warehouse*, Inmon, Ch. 3

### Dimensional modeling: fact, dimension, grain
A dimensional model organizes data around a business process. The **fact table** stores measurements at a declared **grain** — the level of detail a single row represents (e.g., "one row per taxi trip" or "one row per line item per order"). The **dimensions** are the descriptive context: who, what, where, when, why, how. Declaring the grain *first* is non-negotiable; every fact column and every dimension foreign key must be true at that grain, or the model will silently double-count.
Ref: *Kimball DW Toolkit, Ch. 1* (Four-Step Dimensional Design Process)

### Fact additivity
Facts are classified by how they roll up across dimensions. **Fully additive** facts (e.g., `trip_count`, `fare_amount`) can be summed across any dimension. **Semi-additive** facts (e.g., `account_balance`) can be summed across some dimensions but not time — you do not sum today's balance and yesterday's balance. **Non-additive** facts (e.g., ratios, percentages, `avg_tip_percentage`) cannot be summed at all; store the numerator and denominator and compute the ratio at query time.
Ref: *Kimball DW Toolkit, Ch. 1* (note: a fact table storing `avg_tip_percentage` is a textbook example of non-additivity)

### Star vs snowflake
A **star schema** keeps each dimension as a single denormalized table directly joined to the fact. A **snowflake schema** normalizes dimensions into sub-dimensions (e.g., `dim_product → dim_category → dim_department`). Star is the default: fewer joins, simpler SQL, better compression in columnar stores. Snowflake is occasionally defensible when a sub-dimension is genuinely shared across many dimensions or is enormous, but the storage savings rarely justify the query complexity.
Ref: *Kimball DW Toolkit, Ch. 1*

### Slowly Changing Dimensions (SCD)
Dimension attributes change (a customer moves, a product is reclassified). SCD types define how you record the change:
- **Type 0** — retain original, never update. Used for attributes that must never change historically (date of birth, original signup source).
- **Type 1** — overwrite. Fast, loses history. Acceptable when history is irrelevant or tracked elsewhere.
- **Type 2** — add a new row, mark the old row with `valid_from` / `valid_to` / `is_current`. The standard technique for tracking history; all historical facts continue to join to the row that was current at the time of the event.
- **Type 3** — add a `prior_value` column on the same row. Supports exactly one level of history; used when users want to toggle between "old" and "new" without a full time series.
- **Type 6** — hybrid of 1 + 2 + 3: a Type 2 row plus a Type 1 "current value" column copied onto every historical row, so "group by current region" and "group by historical region" both work.

Ref: *Kimball DW Toolkit, Ch. 5* · glossary: [`../../references/glossary.md`](../../references/glossary.md) (SCD) · dbt's `snapshot` with `strategy='timestamp'` implements Type 2 by writing `dbt_valid_from` / `dbt_valid_to` columns behind the scenes ([dbt — Snapshots](https://docs.getdbt.com/docs/build/snapshots)).

### Inmon CIF vs Kimball bus architecture
Inmon's **Corporate Information Factory** puts a 3NF, subject-oriented, integrated, time-variant, non-volatile enterprise data warehouse at the center; dimensional **data marts** are derived downstream for specific departments. Kimball's **bus architecture** inverts this: you build conformed dimensions and a bus matrix first, then add fact tables for each business process; there is no separate 3NF layer. Inmon is easier to govern when source systems are heterogeneous and compliance requires a single historized record; Kimball is faster to deliver business value and is the default for most analytics teams. Modern lakehouses often use an Inmon-style silver layer (normalized, historized) feeding a Kimball-style gold layer (dimensional marts).
Ref: *Building the Data Warehouse*, Inmon, Ch. 2 · *Kimball DW Toolkit, Ch. 1*

### Data Vault (hub / link / satellite)
Data Vault 2.0 models the warehouse as three object types: **hubs** hold unique business keys, **links** hold the many-to-many relationships between hubs, and **satellites** hold the descriptive, time-variant attributes. Every object is insert-only, hash-keyed, and source-tagged, which makes loads massively parallel and fully auditable. Data Vault shines when (a) multiple source systems must be integrated without losing provenance, (b) regulatory audit trails require every historical state, or (c) source schemas change frequently and you cannot afford to refactor a 3NF EDW every time. It is **not** a query layer — you still build a Kimball-style mart on top for BI consumers.
Ref: *Building a Scalable Data Warehouse with Data Vault 2.0*, Linstedt & Olschimke, Ch. 1–2

### Conformed dimensions
A **conformed dimension** is a dimension table that means the same thing in every fact table that uses it — same grain, same keys, same attribute semantics. Conformed `dim_date`, `dim_customer`, and `dim_product` are what let you drill across business processes: "join orders and support tickets on customer and date" only works if both fact tables reference the same `dim_customer`. The bus matrix is the planning tool — rows are business processes, columns are conformed dimensions, cells mark which dimensions each process uses.
Ref: *Kimball DW Toolkit, Ch. 3*

### Late-arriving facts
A late-arriving (or "out-of-sequence") fact is an event that shows up in the warehouse after the dimension rows it should reference have already moved on — e.g., a sale recorded today for a customer whose address changed last week. With SCD Type 2 dimensions, the correct behavior is to join the fact to the dimension row that was **current at the fact's event timestamp**, not the row that is current at load time. This is why SCD2 rows carry `valid_from` / `valid_to` — the ETL performs a point-in-time lookup on the event date, not the current date.
Ref: *Kimball DW Toolkit, Ch. 5* (Late-Arriving Dimensions and Facts)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L2_star_schema` | Build a `dim_customer` (SCD2) + `fct_orders` star in PostgreSQL and run a point-in-time revenue query | 90m | [labs/lab_L2_star_schema/](labs/lab_L2_star_schema/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Fact row counts double after a new join | Grain was never declared; a dimension join produces >1 row per fact | Re-declare the grain, enforce it with a uniqueness test on the fact's natural key | *Kimball DW Toolkit, Ch. 1* |
| SCD Type 2 query returns duplicates for "current" customers | `is_current` filter missing, or multiple rows have `valid_to IS NULL` | Add `WHERE is_current = true`; assert exactly one open row per business key | *Kimball DW Toolkit, Ch. 5* |
| Averages of averages produce wrong totals | Non-additive fact (a ratio) was stored and re-averaged downstream | Store numerator + denominator, compute the ratio at query time | *Kimball DW Toolkit, Ch. 1* |
| Historical reports shift when a customer attribute changes | Dimension is SCD Type 1; history was overwritten | Convert the attribute to Type 2, or add a Type 3 `prior_value` column if one level is enough | *Kimball DW Toolkit, Ch. 5* |
| Cross-process drill-across joins return no rows | Dimensions are not conformed — `dim_customer` in mart A and mart B use different keys | Build a single conformed `dim_customer` upstream; make marts `ref` it | *Kimball DW Toolkit, Ch. 3* |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Declare the grain of a fact table in one sentence and defend it.
- [ ] Pick an SCD type for a given attribute (customer address, product category, signup date) and justify the choice.
- [ ] Draw the difference between a star and a snowflake on paper.
- [ ] Explain when you would reach for Data Vault instead of Kimball.
- [ ] Write the SQL to answer "what was customer X's region as of 2025-03-01" against an SCD2 dimension.
- [ ] Explain why `avg_tip_percentage` in `fct_trip_metrics.sql` is non-additive.
