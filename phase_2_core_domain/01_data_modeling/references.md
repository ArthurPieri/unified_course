# 01 Data Modeling — References

## Books (canonical)
- *The Data Warehouse Toolkit* (3rd ed.), Ralph Kimball & Margy Ross, Wiley 2013
  - Ch. 1 — Dimensional modeling primer, four-step design process, fact additivity, star vs snowflake
  - Ch. 2 — Dimensional modeling techniques (cheat-sheet / reference)
  - Ch. 3 — Retail case study; conformed dimensions and the bus matrix
  - Ch. 5 — Slowly Changing Dimensions (Types 0/1/2/3/6); late-arriving dimensions and facts
- *Building the Data Warehouse* (4th ed.), W. H. Inmon, Wiley 2005
  - Ch. 1 — Evolution of decision-support systems; subject-oriented, integrated, time-variant, non-volatile
  - Ch. 2 — Corporate Information Factory architecture
  - Ch. 3 — Data warehouse data modeling (3NF enterprise layer)
- *Building a Scalable Data Warehouse with Data Vault 2.0*, Dan Linstedt & Michael Olschimke, Morgan Kaufmann 2015
  - Ch. 1 — Introduction to Data Vault 2.0
  - Ch. 2 — Scalable data warehouse architecture; hub / link / satellite object types

## Official documentation
- [PostgreSQL: CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html) — DDL syntax, primary/foreign keys, check constraints
- [PostgreSQL: Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) — primary key, unique, foreign key, exclusion
- [PostgreSQL: Data Types](https://www.postgresql.org/docs/current/datatype.html) — `timestamp`, `date`, `numeric`
- [Docker: `docker run`](https://docs.docker.com/reference/cli/docker/container/run/) — running the Postgres container used in the lab

## Sibling-dir exemplars
- `../../../dataeng/dbt_project/models/marts/dim_zones.sql:L1-L19` — denormalized dimension (star-schema style)
- `../../../dataeng/dbt_project/models/marts/fct_trip_metrics.sql:L1-L32` — fact table with declared grain (date × pickup_borough) and a non-additive `avg_tip_percentage`
- `../../../dataeng/dbt_project/snapshots/snap_taxi_zones.sql:L1-L25` — dbt snapshot implementing SCD Type 2 with a timestamp strategy

## Cross-references
- Glossary: [`../../references/glossary.md`](../../references/glossary.md) — SCD, star schema, Data Vault
- Books index: [`../../references/books.md`](../../references/books.md)
- Sibling source index: [`../../references/sibling_sources.md`](../../references/sibling_sources.md) (rows tagged "Phase 2 · 01_data_modeling")
- Reuse policy: [`../../docs/REUSE_POLICY.md`](../../docs/REUSE_POLICY.md)
