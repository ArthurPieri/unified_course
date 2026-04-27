# Module 05: Performance — Warehouses, Caching, Clustering, Profiling

Performance and cost are Core Domain 3.0 (16%) and DEA Domain 2.0 (19%). At the Platform level, Domain 3.0 also covers warehouses (sizing, scaling, auto-suspend) — so this module is useful on all three exams. **Sibling source is thin here:** Phase 1 has a warehouse lab but no performance-optimization study notes, so this module cites official Snowflake docs and the PDF study guides primarily.

## Learning goals
- Distinguish **scaling up** (warehouse size) from **scaling out** (multi-cluster) and when to use each.
- Read a Query Profile and identify spilling, pruning, and exploding joins.
- Describe the result cache, warehouse cache, and Query Acceleration Service and when each applies.
- Decide when to add a clustering key and when to enable Search Optimization Service (SOS).
- Use `SYSTEM$CLUSTERING_INFORMATION` to check clustering depth.

## Prerequisites
- `../01_architecture/` (cache types, micro-partitions)
- `../02_loading/` (warehouse context for COPY INTO)

## Reading order
1. This README
2. [Snowflake Quickstarts](https://quickstarts.snowflake.com/) — warehouse sizing, auto-suspend, multi-cluster, Cortex
3. `quiz.md`

## Concepts

### Virtual warehouses — sizing and scaling
Warehouse sizes are XS, S, M, L, XL, 2XL, 3XL, 4XL, 5XL, 6XL. Each size roughly **doubles** compute (and credit burn per second) from the previous. **Scaling up** (increase size) helps a single large query that is compute-bound or spilling. **Scaling out** (multi-cluster warehouses) helps concurrency: Snowflake spins up additional clusters of the same size when the queue grows past the scaling policy threshold. Multi-cluster is Enterprise+.

Ref: [Warehouses overview](https://docs.snowflake.com/en/user-guide/warehouses) · *SnowPro Core Study Guide, Domain 3.0, p. 8* · [Snowflake Quickstarts](https://quickstarts.snowflake.com/).

### Auto-suspend, auto-resume, and policies
`AUTO_SUSPEND` (seconds) stops the warehouse after idle time. `AUTO_RESUME = TRUE` restarts it on the next query. Multi-cluster warehouses add `SCALING_POLICY = STANDARD | ECONOMY` — STANDARD spins up clusters eagerly to minimize queueing, ECONOMY delays to maximize utilization.

Ref: [ALTER WAREHOUSE](https://docs.snowflake.com/en/sql-reference/sql/alter-warehouse) · `lab_03_warehouses.sql:L121-L203`.

### Caching (recap with perf lens)
- **Result cache** — 24-hour TTL, extended up to 31 days on re-use, invalidated by DML or non-deterministic functions.
- **Warehouse (local disk SSD) cache** — cleared on suspend or resize.
- **Metadata cache** — serves `COUNT(*)`, `MIN`, `MAX` without a warehouse.

For cost/perf tuning, prefer leaving the warehouse running a bit longer (warmer SSD cache) when queries repeatedly re-read the same large tables.

Ref: [Using persisted query results](https://docs.snowflake.com/en/user-guide/querying-persisted-results) · *Core Study Guide Domain 3.0, p. 8*.

### Query Acceleration Service (QAS)
QAS offloads portions of a query (table scans, filters) to a serverless pool when the query has a selective predicate but needs to scan a lot of data. Enable per-warehouse with `ENABLE_QUERY_ACCELERATION = TRUE`. Billed serverlessly.

Ref: [Query Acceleration Service](https://docs.snowflake.com/en/user-guide/query-acceleration-service) · *Core Study Guide Domain 3.0, p. 8*.

### Clustering keys
By default Snowflake clusters data by insertion order; pruning still works for most workloads. For very large tables (>1 TB) where queries repeatedly filter on a non-insertion-order column, define a **clustering key** (`ALTER TABLE t CLUSTER BY (col)`). Snowflake then auto-reclusters in the background. Measure with `SYSTEM$CLUSTERING_INFORMATION` and `SYSTEM$CLUSTERING_DEPTH`.

Ref: [Clustering keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys) · *DEA Study Guide §3.2, p. 8*.

### Search Optimization Service (SOS)
SOS builds a persistent lookup structure that accelerates **point-lookup and substring/regex** queries on columns the clustering key does not cover. Enable with `ALTER TABLE t ADD SEARCH OPTIMIZATION ON EQUALITY(col), SUBSTRING(col2);`. Enterprise+ feature; billed serverlessly.

Ref: [Search optimization service](https://docs.snowflake.com/en/user-guide/search-optimization-service) · *Core Study Guide Domain 3.0, p. 8*.

### Query Profile
Snowsight's Query Profile tree shows operator-by-operator bytes scanned, partitions scanned vs total, bytes spilled to local or remote storage, and join row explosion. Red flags to look for:
- **Bytes spilled to remote storage** — warehouse is undersized; scale up.
- **Partitions scanned == partitions total** — no pruning; check predicates, consider clustering key.
- **JoinFilter** with huge row count — missing filter predicate or cartesian join.

Ref: [Query Profile](https://docs.snowflake.com/en/user-guide/ui-query-profile) · *DEA Study Guide §2.1, p. 7*.

### Resource monitors and budgets
`CREATE RESOURCE MONITOR` sets credit quotas with actions (`NOTIFY`, `SUSPEND`, `SUSPEND_IMMEDIATE`) at percentage thresholds. Scope to account or specific warehouses. **Snowflake Budgets** (in Snowsight) provide a higher-level spend-tracking layer. Query `SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY` for retrospective analysis.

Ref: [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors) · *Core Study Guide Domain 3.0, p. 8*.

## Hands-on drills

| # | Drill | Est. time | Source |
|---|---|---|---|
| D1 | Create three warehouses (XS, S, M) and run the same analytic query on each — observe elapsed time and credits in Query Profile. | 30 min | `lab_03_warehouses.sql:L17-L120` |
| D2 | Set `AUTO_SUSPEND = 60` and `AUTO_RESUME = TRUE`; walk away, come back, confirm suspend and resume. | 15 min | `lab_03_warehouses.sql:L121-L154` |
| D3 | Configure a multi-cluster warehouse with `MIN_CLUSTER_COUNT = 1`, `MAX_CLUSTER_COUNT = 3`, run concurrent queries and observe cluster count. | 30 min | `lab_03_warehouses.sql:L155-L203` |
| D4 | Create a resource monitor with a 10-credit quota and `SUSPEND` action at 100%. | 20 min | [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors) |
| D5 | Run `SELECT SYSTEM$CLUSTERING_INFORMATION('snowflake_sample_data.tpch_sf1.lineitem', '(l_shipdate)');` and interpret average depth vs constant. | 20 min | [Clustering keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys) |
| D6 | Force spilling: run a `SORT` on a very large sample table on an XS warehouse; open Query Profile and find "Bytes spilled to remote storage". | 25 min | [Query Profile](https://docs.snowflake.com/en/user-guide/ui-query-profile) |

## Common failures (exam gotchas)

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| "Multi-cluster fixes slow single queries" | False | Multi-cluster addresses concurrency, not per-query latency. Scale **up** for a slow single query. | *Core Study Guide Domain 3.0, p. 8* |
| "Search Optimization replaces clustering" | False | SOS and clustering are complementary. Clustering prunes partitions; SOS accelerates point lookups. | [SOS docs](https://docs.snowflake.com/en/user-guide/search-optimization-service) |
| "Result cache serves all identical queries forever" | False | 24h TTL (extended to 31d on re-use); invalidated by DML or non-deterministic functions. | [Persisted results](https://docs.snowflake.com/en/user-guide/querying-persisted-results) |
| "Resizing a warehouse preserves local cache" | False | Resize provisions new VMs; cache is cleared. | `../01_architecture/README.md` |
| "Query Acceleration runs on the warehouse cluster" | False | QAS is serverless — billed separately, not on the warehouse. | [QAS docs](https://docs.snowflake.com/en/user-guide/query-acceleration-service) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Pick scale-up vs scale-out for a given scenario.
- [ ] Identify spilling and poor pruning in a Query Profile screenshot.
- [ ] Choose between clustering key, SOS, materialized view, and QAS for a given query pattern.
- [ ] Create a resource monitor that suspends a warehouse at a credit quota.
