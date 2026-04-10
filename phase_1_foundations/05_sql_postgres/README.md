# Module 05: SQL Depth with PostgreSQL (10h)

> Every downstream tool (dbt, Trino, Spark SQL, Snowflake, Redshift, Fabric) speaks a dialect of ANSI SQL with window functions, CTEs, and a query planner you are expected to read. This module uses PostgreSQL 16 as a universal SQL sandbox so you can learn the concepts against a single, well-documented engine.

## Learning goals
- Write ranking, offset, and rolling-window queries using `OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN ...)`
- Decompose complex logic with CTEs (including recursive) and know when a subquery is clearer
- Read a PostgreSQL query plan well enough to distinguish a sequential scan from an index scan and a nested loop from a hash join
- Pick the right index type (B-tree, GIN, partial, multicolumn) for a query
- Use `VACUUM`, `ANALYZE`, and `pg_stat_statements` to keep the planner honest
- Back up and restore a database with `pg_dump` / `pg_restore`

## Prerequisites
- [../04_docker/](../04_docker/) — you will run Postgres in the Phase 1 gate container from Lab L1
- Basic `SELECT`/`JOIN`/`GROUP BY` fluency (if rusty: [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html))

## Reading order
1. This README
2. [labs/lab_03_nyc_taxi_sql/README.md](labs/lab_03_nyc_taxi_sql/README.md)
3. [quiz.md](quiz.md)

## Concepts

### Window functions
A window function computes a value over a set of rows **related to the current row** without collapsing the result — unlike `GROUP BY`, the row count is preserved. The `OVER` clause defines the window: `PARTITION BY` slices, `ORDER BY` sequences, and `ROWS BETWEEN` / `RANGE BETWEEN` frames the subset used for the current row's calculation. Ranking functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`) assign positions; `LEAD`/`LAG` peek at neighbours; aggregates (`SUM`, `AVG`, `COUNT`) with `OVER` produce running totals and moving averages.
Ref: [Window function tutorial](https://www.postgresql.org/docs/current/tutorial-window.html) · [Window function calls](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)

`ROW_NUMBER` vs `RANK` vs `DENSE_RANK`: on ties, `ROW_NUMBER` assigns distinct sequential numbers, `RANK` gives tied rows the same rank and skips the next values, `DENSE_RANK` gives tied rows the same rank without gaps.
Ref: [Window functions](https://www.postgresql.org/docs/current/functions-window.html)

### Frames: `ROWS` vs `RANGE`
`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` is a physical 7-row window — exactly what you want for a 7-day rolling sum on a daily table. `RANGE` is logical: it includes all peers of the current row under the `ORDER BY` key, which is subtle and often not what you want for time series with gaps.
Ref: [Window function calls — frame clause](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)

### CTEs and recursive CTEs
A `WITH` clause names a subquery so it can be referenced later in the same statement, improving readability and letting a value be reused without repetition. Recursive CTEs (`WITH RECURSIVE`) express graph and hierarchy traversals — parent-child trees, bill-of-materials, reachability — that cannot be written with vanilla joins of unknown depth.
Ref: [WITH queries (CTEs)](https://www.postgresql.org/docs/current/queries-with.html)

### Subqueries vs joins
A correlated subquery and an equivalent join often produce the same result; the planner sometimes rewrites one into the other. Prefer a join when you need columns from both sides and the relationship is set-based. Prefer a subquery / `EXISTS` when you only need a filter ("rows in A that have at least one match in B") — `EXISTS` short-circuits per outer row and avoids row multiplication from many-to-many joins.
Ref: [Subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html) · [SELECT — FROM clause](https://www.postgresql.org/docs/current/sql-select.html)

### Reading `EXPLAIN` and `EXPLAIN ANALYZE`
`EXPLAIN <query>` shows the planner's chosen plan with estimated cost, row counts, and widths. `EXPLAIN ANALYZE <query>` actually runs the query and annotates each node with measured time and real row counts — the definitive source of truth when estimates lie. Scan nodes you will see: `Seq Scan` (read the whole table), `Index Scan` (walk an index, fetch heap rows), `Index Only Scan` (answer from the index alone when the table is visibility-clean). Join nodes: `Nested Loop` (fast on a small outer side + indexed inner), `Hash Join` (build a hash on the smaller side, probe with the larger — typical for equi-joins on unindexed columns), `Merge Join` (both inputs sorted on the join key). A large gap between `rows=` estimated and actual is a signal that statistics are stale — run `ANALYZE`.
Ref: [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) · [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)

### Indexes
PostgreSQL's default B-tree index accelerates equality and range predicates on scalar columns and supports `ORDER BY` without a sort. **Multicolumn** B-trees help queries that filter on a leading prefix of the index columns. **Partial** indexes (`CREATE INDEX ... WHERE <predicate>`) cover only a subset of rows — smaller and faster when queries always include the predicate. **GIN** indexes fit "many values per row" data: `jsonb`, arrays, and full-text `tsvector`. Every index costs write amplification; index only what queries actually need.
Ref: [Indexes](https://www.postgresql.org/docs/current/indexes.html) · [Index types](https://www.postgresql.org/docs/current/indexes-types.html) · [Multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html) · [Partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html)

### `VACUUM`, `ANALYZE`, and autovacuum
PostgreSQL's MVCC creates dead tuples on every `UPDATE` and `DELETE`. `VACUUM` reclaims that space for reuse; `VACUUM FULL` rewrites the table to shrink it on disk (holds an exclusive lock). `ANALYZE` refreshes the statistics the planner uses to pick plans. Autovacuum does both on thresholds — but after a bulk load you should `ANALYZE` manually so the very next query gets a sane plan.
Ref: [Routine vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html) · [ANALYZE](https://www.postgresql.org/docs/current/sql-analyze.html)

### Observability: `pg_stat_activity` and `pg_stat_statements`
`pg_stat_activity` is a live view of current sessions, their state, and the query text — the first place to look when something is hanging. `pg_stat_statements` is an extension that aggregates execution stats per normalized query (total time, calls, mean time, rows) and is the canonical tool for finding the slow queries worth tuning.
Ref: [pg_stat_activity](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW) · [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)

### Backup and restore
`pg_dump` produces a consistent logical backup of a single database; defaults to a plain SQL script, `-Fc` gives a custom-format archive that `pg_restore` can reorder, parallelize (`-j`), and restore selectively. For cluster-wide backups (roles, tablespaces) use `pg_dumpall`.
Ref: [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html) · [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_03_nyc_taxi_sql` | Load ~50k NYC Taxi rows, write 5 window-function queries, run `EXPLAIN ANALYZE`, add an index, compare plans | 90m | [labs/lab_03_nyc_taxi_sql/](labs/lab_03_nyc_taxi_sql/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `EXPLAIN` estimates wildly wrong | Stats stale after bulk load | `ANALYZE <table>;` | [ANALYZE](https://www.postgresql.org/docs/current/sql-analyze.html) |
| Index exists but planner ignores it | Query returns a large fraction of the table — seq scan is cheaper | Expected; rethink the predicate or use a partial/covering index | [Using EXPLAIN — examples](https://www.postgresql.org/docs/current/using-explain.html) |
| Window aggregate returns unexpected totals | Missing `ROWS BETWEEN` — default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` with peer grouping | Specify `ROWS BETWEEN ... PRECEDING AND CURRENT ROW` | [Window function calls](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS) |
| `COUNT(*)` very slow | Seq scan of a big table; MVCC requires heap visit | Use `pg_class.reltuples` for estimates; real counts cost real time | [Routine vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html) |
| `pg_restore` fails on owner mismatch | Backup references a role that does not exist | Restore with `--no-owner --role=<current-role>` | [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Write a 7-day rolling sum using `SUM() OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`
- [ ] Rank rows within groups and explain the difference between `RANK` and `DENSE_RANK`
- [ ] Read an `EXPLAIN ANALYZE` plan and identify `Seq Scan`, `Index Scan`, `Hash Join`
- [ ] Create a B-tree index and demonstrate a plan change with before/after timings
- [ ] Dump and restore a database with `pg_dump -Fc` and `pg_restore`
