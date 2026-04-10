# References — 05_sql_postgres

All citations are to the PostgreSQL official manual, `current` version, which tracks the latest stable release.

## Tutorials
- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html) — baseline if `SELECT`/`JOIN`/`GROUP BY` feel rusty
- [Window function tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)
- [Tutorial — joins between tables](https://www.postgresql.org/docs/current/tutorial-join.html)

## Queries & expressions
- [WITH queries (Common Table Expressions)](https://www.postgresql.org/docs/current/queries-with.html) — CTEs and `WITH RECURSIVE`
- [SELECT](https://www.postgresql.org/docs/current/sql-select.html)
- [Value expressions — window function calls](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS) — frame clause (`ROWS`/`RANGE`/`GROUPS`)
- [Window functions (reference)](https://www.postgresql.org/docs/current/functions-window.html) — `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LEAD`, `LAG`, `NTILE`
- [Subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html) — `EXISTS`, `IN`, `ANY`, `ALL`

## Planning & performance
- [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) — how to read plans, cost model, ANALYZE option
- [EXPLAIN (SQL reference)](https://www.postgresql.org/docs/current/sql-explain.html)
- [Routine vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html) — MVCC, `VACUUM`, autovacuum
- [ANALYZE](https://www.postgresql.org/docs/current/sql-analyze.html)

## Indexes
- [Indexes — intro](https://www.postgresql.org/docs/current/indexes.html)
- [Index types](https://www.postgresql.org/docs/current/indexes-types.html) — B-tree, Hash, GiST, SP-GiST, GIN, BRIN
- [Multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [Partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html)
- [Index-only scans and covering indexes](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)

## Monitoring
- [Monitoring stats — pg_stat_activity](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW)
- [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)

## Backup & restore
- [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
- [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [pg_dumpall](https://www.postgresql.org/docs/current/app-pg-dumpall.html)
- [COPY](https://www.postgresql.org/docs/current/sql-copy.html) — bulk load CSV/TSV
