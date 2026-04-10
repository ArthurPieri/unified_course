# Module 06 — Quiz: DEA Advanced

12 questions. Key + citations at the bottom.

---

**1.** A stream on `orders` has not been consumed for longer than the source table's `DATA_RETENTION_TIME_IN_DAYS`. What happens?
A. The stream auto-extends the retention window.
B. The stream becomes **stale** and cannot be queried; it must be recreated.
C. The stream pauses until retention increases.
D. The stream downgrades to an append-only stream.

**2.** Which stream type is cheapest for a high-volume **insert-only** source table?
A. Standard stream
B. Append-only stream
C. Insert-only stream on an external table
D. UDAF stream

**3.** Which function should you use in a task's `WHEN` clause to skip runs where a stream has no new data?
A. `SYSTEM$CLUSTERING_INFORMATION`
B. `SYSTEM$STREAM_HAS_DATA`
C. `SYSTEM$PIPE_STATUS`
D. `SYSTEM$TASK_RUNNING`

**4.** A team wants incremental refresh of a derived table with `TARGET_LAG = '10 minutes'` using only declarative SQL — no DAG wiring. Which feature fits?
A. Materialized view
B. Stream + task
C. Dynamic Table
D. Snowpipe

**5.** Which Snowflake compute option is tuned for memory-heavy Snowpark Python UDFs?
A. Standard XS warehouse
B. Snowpark-optimized warehouse
C. Serverless task
D. Query Acceleration Service

**6.** Which function type takes N rows in and returns M rows out, used to fan-out transformations?
A. UDF (scalar)
B. UDTF
C. UDAF
D. External function

**7.** An external function calls an AWS API Gateway endpoint. What Snowflake object represents the trust relationship with the gateway?
A. Storage integration
B. API integration
C. Network policy
D. Security integration

**8.** Which statement about Snowflake's support for Apache Iceberg is **correct**?
A. Snowflake supports Iceberg only in read-only mode.
B. Snowflake supports Iceberg tables with either a Snowflake-managed catalog or an externally managed catalog.
C. Iceberg tables in Snowflake require Virtual Private Snowflake.
D. Iceberg tables cannot coexist with standard Snowflake tables.

**9.** Which limitation applies to materialized views in Snowflake (not Dynamic Tables)?
A. They support window functions.
B. They typically support only a single base table.
C. They have no lag; Dynamic Tables do.
D. Both B and C.

**10.** When would you choose **Snowpipe Streaming** over a stream+task pipeline?
A. When you need a declarative SQL-only transform
B. When you need sub-second row-level ingestion from a producer application
C. When you need to express CDC deltas in a consumer
D. When you need to run on a Snowpark-optimized warehouse

**11.** A Snowpark Python UDF needs `numpy`. What is the idiomatic way to supply it?
A. Upload a ZIP with numpy in `IMPORTS`
B. Add `'numpy'` to the `PACKAGES` clause; Snowflake pulls it from the Snowflake Anaconda channel
C. `pip install` at runtime from within the UDF
D. Not supported — use Java

**12.** True or False: Dynamic Tables can depend on other Dynamic Tables, forming a refresh DAG that Snowflake orders automatically.

---

## Answer key

1. **B** — Stream staleness when the offset falls outside source retention. [Streams](https://docs.snowflake.com/en/user-guide/streams-intro).
2. **B** — Append-only streams skip delete/update tracking. [Streams](https://docs.snowflake.com/en/user-guide/streams-intro); *DEA §1.4, p. 5*.
3. **B** — `SYSTEM$STREAM_HAS_DATA`. [System stream has data](https://docs.snowflake.com/en/sql-reference/functions/system_stream_has_data).
4. **C** — Dynamic Tables are the declarative incremental pattern. [Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about); *DEA §1.4, p. 5*.
5. **B** — Snowpark-optimized warehouses have more RAM per worker. [Snowpark-optimized warehouses](https://docs.snowflake.com/en/user-guide/warehouses-snowpark-optimized); *DEA §2.2, p. 7*.
6. **B** — UDTF = table function. [UDTFs](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-tabular-functions).
7. **B** — API integration. [API integration](https://docs.snowflake.com/en/sql-reference/sql/create-api-integration); [External functions](https://docs.snowflake.com/en/sql-reference/external-functions).
8. **B** — Two modes: managed or externally managed. [Iceberg tables](https://docs.snowflake.com/en/user-guide/tables-iceberg); *DEA §1.7, p. 6*.
9. **B** — MVs support a single base table (no joins across multiple tables). [Materialized views](https://docs.snowflake.com/en/user-guide/views-materialized). Note: MVs are lower lag than Dynamic Tables — they are maintained automatically.
10. **B** — Snowpipe Streaming is for sub-second row-level ingestion. [Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-overview); *DEA §1.4, p. 5*.
11. **B** — Use `PACKAGES` + Snowflake Anaconda channel. [Snowpark Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index).
12. **True** — Dynamic Tables form DAGs; Snowflake coordinates refreshes. [Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about).
