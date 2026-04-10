# Quiz — 05_sql_postgres

Ten multiple-choice questions. Answers at the bottom.

---

**1.** You have a daily `sales(day, store_id, amount)` table and want a 7-day rolling sum per store. Which clause is correct?

A. `SUM(amount) OVER (PARTITION BY store_id ORDER BY day)`
B. `SUM(amount) OVER (PARTITION BY store_id ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`
C. `SUM(amount) OVER (ORDER BY store_id, day)`
D. `SUM(amount) GROUP BY store_id, day`

**2.** Three rows tie for 2nd place by `score`. Which ranking function gives them all rank `2` and assigns rank `3` to the next row?

A. `ROW_NUMBER()`
B. `RANK()`
C. `DENSE_RANK()`
D. `NTILE(2)`

**3.** Which query gets "rows in `orders` that have at least one matching `line_item`" with no row multiplication?

A. `SELECT o.* FROM orders o JOIN line_items li ON li.order_id = o.id;`
B. `SELECT o.* FROM orders o WHERE EXISTS (SELECT 1 FROM line_items li WHERE li.order_id = o.id);`
C. `SELECT DISTINCT o.* FROM orders o, line_items li;`
D. `SELECT o.* FROM orders o GROUP BY o.id;`

**4.** `EXPLAIN ANALYZE` shows `Seq Scan on trips  (rows=54000)` followed by `Filter: (tpep_pickup_datetime > ...)`. How do you likely shrink the runtime?

A. Run `VACUUM FULL`
B. Rewrite as a subquery
C. `CREATE INDEX ON trips (tpep_pickup_datetime);` and re-run after `ANALYZE`
D. Add `LIMIT 1000` to the query

**5.** After bulk-loading 50k rows with `COPY`, the planner picks terrible plans. What is the minimal fix?

A. `REINDEX TABLE`
B. `VACUUM FULL`
C. `ANALYZE <table>;`
D. Restart Postgres

**6.** Which statement about `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (the default window frame) is correct?

A. It includes all rows in the partition
B. It includes all rows up to and including every row that is a peer of the current row under the `ORDER BY` key
C. It is identical to `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`
D. It is only valid for numeric columns

**7.** You need to traverse a parent-child category tree of unknown depth. The right tool is:

A. A self-join repeated N times
B. A `WITH RECURSIVE` CTE
C. A correlated subquery
D. A stored procedure

**8.** Which index type is the right default for querying `jsonb` containment (`WHERE doc @> '{"status":"open"}'`)?

A. B-tree
B. Hash
C. GIN
D. BRIN

**9.** A `Hash Join` appears in a plan. Which statement is accurate?

A. Both inputs must be sorted on the join key
B. Postgres builds a hash on the smaller input and probes it with the larger — typical for equi-joins on unindexed columns
C. It only runs on partitioned tables
D. It requires a covering index

**10.** Which pair dumps and restores a single database using the format that supports parallel restore?

A. `pg_dump db > db.sql` / `psql db < db.sql`
B. `pg_dump -Fc db > db.dump` / `pg_restore -d db db.dump`
C. `pg_dumpall > all.sql` / `psql < all.sql`
D. `COPY ... TO` / `COPY ... FROM`

---

## Answer key

1. **B** — The default frame is peer-based `RANGE`; a physical 7-row rolling window requires explicit `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`. [Window function calls](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)
2. **C** — `DENSE_RANK` does not leave gaps after ties; `RANK` would skip to `5` after three ties at `2`. [Window functions](https://www.postgresql.org/docs/current/functions-window.html)
3. **B** — `EXISTS` filters without multiplying rows; a join would duplicate an order per line item. [Subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html)
4. **C** — A B-tree on the filtered column turns the `Seq Scan + Filter` into an `Index Scan`. [Indexes](https://www.postgresql.org/docs/current/indexes.html) · [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
5. **C** — `ANALYZE` refreshes planner statistics immediately; autovacuum will eventually run it, but not before your next query. [ANALYZE](https://www.postgresql.org/docs/current/sql-analyze.html)
6. **B** — `RANGE` is peer-based on the `ORDER BY` key. [Window function calls](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)
7. **B** — `WITH RECURSIVE` is the documented mechanism for tree / graph traversal of unknown depth. [WITH queries](https://www.postgresql.org/docs/current/queries-with.html)
8. **C** — GIN is the type documented for `jsonb`, arrays, and full text. [Index types](https://www.postgresql.org/docs/current/indexes-types.html)
9. **B** — Hash join builds a hash on the smaller side and probes with the larger; typical for equi-joins lacking supporting indexes. [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
10. **B** — `pg_dump -Fc` produces the custom format that `pg_restore -j` can parallelize. [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html) · [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)
