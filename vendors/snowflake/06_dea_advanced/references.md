# Module 06 — References

> **Sibling gap notice:** Phases 2 and 3 of `../../../../snowflake_eng/` (Core and DEA deep content) do **not** exist. This module has **no** sibling-notes citations and relies entirely on the DEA + Core PDF study guides and docs.snowflake.com. See `../../../references/sibling_sources.md:L158-L178`.

## Snowflake docs (primary)
- [Streams intro](https://docs.snowflake.com/en/user-guide/streams-intro)
- [Tasks intro](https://docs.snowflake.com/en/user-guide/tasks-intro)
- [CREATE STREAM](https://docs.snowflake.com/en/sql-reference/sql/create-stream)
- [CREATE TASK](https://docs.snowflake.com/en/sql-reference/sql/create-task)
- [Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)
- [CREATE DYNAMIC TABLE](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table)
- [Materialized views](https://docs.snowflake.com/en/user-guide/views-materialized)
- [User-defined functions overview](https://docs.snowflake.com/en/developer-guide/udf/udf-overview)
- [Secure UDFs](https://docs.snowflake.com/en/developer-guide/udf/udf-secure)
- [UDTFs](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-tabular-functions)
- [External functions](https://docs.snowflake.com/en/sql-reference/external-functions)
- [API integration](https://docs.snowflake.com/en/sql-reference/sql/create-api-integration)
- [Snowpark for Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)
- [Snowpark-optimized warehouses](https://docs.snowflake.com/en/user-guide/warehouses-snowpark-optimized)
- [Iceberg tables](https://docs.snowflake.com/en/user-guide/tables-iceberg)
- [External tables](https://docs.snowflake.com/en/user-guide/tables-external-intro)
- [SYSTEM$STREAM_HAS_DATA](https://docs.snowflake.com/en/sql-reference/functions/system_stream_has_data)
- [TASK_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/task_history)

## Official study guides
- *SnowPro Advanced: Data Engineer Study Guide*, Domain 1.0 "Data Movement", pp. 5-6 — §1.4 continuous pipelines (Streams, Tasks, Dynamic Tables, Snowpipe, Snowpipe Streaming), §1.5 connectors, §1.7 table types (external, Iceberg, hybrid, Horizon Catalog).
- *SnowPro Advanced: Data Engineer Study Guide*, Domain 5.0 "Data Transformation", pp. 10-11 — §5.1 UDFs (Snowpark, secure, SQL/JS, UDTFs, UDAFs), §5.2 external functions, §5.3 stored procedures, §5.7 Snowpark for transformations.
- *SnowPro Core Study Guide*, Domain 5.0 "Data Transformations", p. 11 — streams, tasks, UDFs, stored procedures, semi-structured FLATTEN.

## Iceberg spec (canonical per REUSE_POLICY §2)
- [Apache Iceberg table spec](https://iceberg.apache.org/spec/)

## Sibling reuse
- None. Sibling gap — see top of file.
