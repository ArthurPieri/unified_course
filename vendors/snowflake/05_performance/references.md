# Module 05 — References

> **Sibling gap notice:** `../../../../snowflake_eng/phase1_platform/` contains a warehouses SQL lab (`lab_03_warehouses.sql`) but **no Performance & Cost study notes**. Phases 2-3 of `../../../../snowflake_eng/` (Core and DEA) do not yet exist. This module therefore cites the PDF study guides and docs.snowflake.com as primary sources, with one sibling lab file for hands-on drills. See `../../../references/sibling_sources.md:L158-L178`.

## Snowflake docs (primary)
- [Virtual warehouses overview](https://docs.snowflake.com/en/user-guide/warehouses)
- [Multi-cluster warehouses](https://docs.snowflake.com/en/user-guide/warehouses-multicluster)
- [ALTER WAREHOUSE](https://docs.snowflake.com/en/sql-reference/sql/alter-warehouse)
- [Query Profile](https://docs.snowflake.com/en/user-guide/ui-query-profile)
- [Using persisted query results (result cache)](https://docs.snowflake.com/en/user-guide/querying-persisted-results)
- [Clustering keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)
- [SYSTEM$CLUSTERING_INFORMATION](https://docs.snowflake.com/en/sql-reference/functions/system_clustering_information)
- [SYSTEM$CLUSTERING_DEPTH](https://docs.snowflake.com/en/sql-reference/functions/system_clustering_depth)
- [Search Optimization Service](https://docs.snowflake.com/en/user-guide/search-optimization-service)
- [Query Acceleration Service](https://docs.snowflake.com/en/user-guide/query-acceleration-service)
- [Materialized views](https://docs.snowflake.com/en/user-guide/views-materialized)
- [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [WAREHOUSE_METERING_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history)

## Official study guides
- *SnowPro Core Study Guide*, Domain 3.0 "Performance and Cost Optimization Concepts", p. 8 — Query Profile, caching, clustering, materialized views, search optimization, query acceleration, cost optimization, resource monitors.
- *SnowPro Advanced: Data Engineer Study Guide*, Domain 2.0 "Performance Optimization", p. 7 — troubleshoot queries, scale out vs up, Snowpark-optimized warehouses, pipeline monitoring, alerts, data quality metric functions.
- *SnowPro Associate: Platform Study Guide*, §3.2 "Virtual warehouses", p. 7 — sizing, multi-cluster, scaling up/down.

## Sibling reuse (limited)
- `../../../../snowflake_eng/phase1_platform/labs/lab_03_warehouses.sql:L17-L435` — warehouse sizing, properties, auto-suspend/resume, multi-cluster, Cortex LLM, quick-reference exam notes.
