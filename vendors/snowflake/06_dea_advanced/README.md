# Module 06: DEA Advanced — Streams, Tasks, Dynamic Tables, Snowpark, UDFs, External Functions, Iceberg

This module is the **DEA-C02 delta** on top of Platform + Core. It touches COF-C02 Domain 5.0 (Data Transformations, 18%) only for streams, tasks, and UDF basics; everything else is DEA Domain 1.0 (Data Movement, 28%) and Domain 5.0 (Data Transformation, 25%).

This module cites the [Snowflake certification study guides](https://www.snowflake.com/certifications/) and [Snowflake documentation](https://docs.snowflake.com/) exclusively.

## Learning goals
- Explain what a **stream** captures (CDC for a source table) and the three stream types.
- Design a stream + task pipeline and state the alternative: **Dynamic Tables**.
- Write a Snowpark Python UDF and explain how dependencies are packaged.
- Differentiate **UDFs**, **UDTFs**, **UDAFs**, and **external functions**.
- Describe Iceberg tables in Snowflake: managed vs unmanaged catalog, and when to choose them over standard tables.
- Pick between stream+task and Dynamic Tables for a given pipeline.

## Prerequisites
- Active SnowPro Core (per DEA-C02 official prerequisite).
- `../02_loading/` — Snowpipe and Snowpipe Streaming.
- `../03_access/` — role context for UDF execution.
- `../05_performance/` — Snowpark-optimized warehouses.

## Reading order
1. This README
2. *SnowPro Advanced: Data Engineer Study Guide*, Domain 1.0 pp. 5-6 and Domain 5.0 pp. 10-11.
3. [Streams intro](https://docs.snowflake.com/en/user-guide/streams-intro) and [Tasks intro](https://docs.snowflake.com/en/user-guide/tasks-intro)
4. [Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)
5. `quiz.md`

## Concepts

### Streams (CDC)
A **stream** records insert/update/delete offsets on a source table since the last consumer read. Query the stream like a table: it exposes the source columns plus `METADATA$ACTION` (`INSERT` / `DELETE`), `METADATA$ISUPDATE`, and `METADATA$ROW_ID`. Consuming a stream in a DML transaction advances its offset. Three types:
- **Standard stream** — tracks all DML.
- **Append-only stream** — tracks inserts only; cheaper for append workloads.
- **Insert-only stream** (on external tables and directory tables).

Streams interact with Time Travel: if a stream's offset falls outside the source table's retention window, the stream becomes **stale** and must be recreated.

Ref: [Streams intro](https://docs.snowflake.com/en/user-guide/streams-intro) · *DEA Study Guide, §1.4, p. 5*.

### Tasks
A **task** runs a SQL statement or stored procedure on a schedule (CRON or interval) or when a **predecessor task** completes, forming a DAG (`AFTER` clause). Tasks can run on a user-managed warehouse or use **serverless tasks**. Use `SYSTEM$STREAM_HAS_DATA('my_stream')` in a `WHEN` clause to skip idle runs.

Ref: [Tasks intro](https://docs.snowflake.com/en/user-guide/tasks-intro) · [CREATE TASK](https://docs.snowflake.com/en/sql-reference/sql/create-task) · *DEA Study Guide §1.4, p. 5*.

### Dynamic Tables (the modern alternative)
A **Dynamic Table** declares a query; Snowflake incrementally refreshes the result to meet a target **freshness lag** (e.g., `TARGET_LAG = '5 minutes'`). No streams, no tasks, no manual DAG wiring. Good for declarative ELT where you specify the *what* and Snowflake handles the *how*. Dynamic Tables can depend on other Dynamic Tables. Refresh mode is `INCREMENTAL` when possible, `FULL` otherwise.

Ref: [Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about) · *DEA Study Guide §1.4, p. 5*.

**When to choose which:**

| If the pipeline... | Use |
|---|---|
| needs fine-grained error handling, custom procedural logic | Stream + Task |
| is mostly declarative SQL with a freshness target | Dynamic Table |
| needs ordering across multiple DMLs in one unit | Stream + Task in a stored procedure |
| Produces CDC deltas for a downstream consumer | Stream |

### Snowpark (Python / Java / Scala)
Snowpark is a DataFrame API that compiles to SQL executed on a Snowflake warehouse. Snowpark Python additionally supports **UDFs and stored procedures written in Python** executed server-side inside Snowflake's sandbox. Dependencies are either pinned Anaconda packages (from the Snowflake Anaconda channel) or uploaded ZIPs via `PACKAGES` / `IMPORTS`.

For CPU- or memory-heavy UDFs, use a **Snowpark-optimized warehouse** (`WAREHOUSE_TYPE = SNOWPARK-OPTIMIZED`) which has more RAM per worker.

Ref: [Snowpark for Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index) · *DEA Study Guide §5.1, §5.7, pp. 10-11*.

### UDFs, UDTFs, UDAFs
- **UDF** — scalar function: 1 row in, 1 scalar out. Languages: SQL, JavaScript, Python, Java, Scala.
- **UDTF** — table function: N rows in, M rows out. Useful for fan-out transformations.
- **UDAF** — aggregate function, user-defined state.
- **Secure UDF** — hides the function body from consumers who have USAGE but not OWNERSHIP; prevents side-channel leakage of masked data.

Ref: [User-defined functions](https://docs.snowflake.com/en/developer-guide/udf/udf-overview) · *DEA Study Guide §5.1, p. 10*.

### External functions
An **external function** is a UDF whose handler is hosted outside Snowflake — typically behind an API Gateway (AWS) or Azure API Management. Snowflake calls the gateway over HTTPS via an **API integration**. Use for calls to ML models, third-party APIs, or logic that cannot run in-sandbox. Limited by request/response size and timeout.

Ref: [External functions](https://docs.snowflake.com/en/sql-reference/external-functions) · *DEA Study Guide §5.2, p. 10*.

### Iceberg tables
Snowflake supports **Apache Iceberg** tables in two modes:
- **Snowflake-managed catalog** — Snowflake writes Iceberg metadata and data to external cloud storage you configure; Snowflake owns the catalog.
- **Externally managed catalog** — Snowflake reads Iceberg tables managed by an external catalog (AWS Glue, Polaris, Apache Iceberg REST catalog). Snowflake is a read/compute engine on top of tables someone else writes.

Iceberg tables store data as Parquet with Iceberg metadata in your object store, so other engines (Trino, Spark) can read them. Choose Iceberg when interop is required; choose standard tables when it is not.

Ref: [Iceberg tables](https://docs.snowflake.com/en/user-guide/tables-iceberg) · *DEA Study Guide §1.7, p. 6*.

### Materialized views (vs Dynamic Tables)
Materialized views are maintained automatically by Snowflake; they are limited (no joins across multiple tables in Standard edition, no window functions, single base table) but have zero lag. Dynamic Tables lift those limits but introduce a configurable lag. Materialized views are Enterprise+.

Ref: [Materialized views](https://docs.snowflake.com/en/user-guide/views-materialized).

## Hands-on drills

| # | Drill | Est. time | Source |
|---|---|---|---|
| D1 | Create a standard stream on a source table, run INSERT/UPDATE/DELETE, consume the stream in a `MERGE` into a target. | 40 min | [Streams](https://docs.snowflake.com/en/user-guide/streams-intro) |
| D2 | Create a task that runs the MERGE every 5 minutes, guarded by `SYSTEM$STREAM_HAS_DATA`. | 30 min | [Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro) |
| D3 | Replace D1+D2 with a Dynamic Table that targets a 5-minute lag. Compare authoring effort. | 45 min | [Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about) |
| D4 | Write a Snowpark Python UDF that applies a regex classifier; call it from SQL; time it on a normal vs Snowpark-optimized warehouse. | 60 min | [Snowpark Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index) |
| D5 | Create an API integration and an external function calling a public echo endpoint. | 45 min | [External functions](https://docs.snowflake.com/en/sql-reference/external-functions) |
| D6 | Create a Snowflake-managed Iceberg table on an external volume; load and query; confirm metadata files in the object store. | 60 min | [Iceberg tables](https://docs.snowflake.com/en/user-guide/tables-iceberg) |

## Common failures (exam gotchas)

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| "Streams forever, no retention limit" | False | Stream offsets are bounded by the source table's Time Travel retention; outside that window the stream becomes **stale**. | [Streams](https://docs.snowflake.com/en/user-guide/streams-intro) |
| "Tasks have their own scheduler you can view in UI only" | Incomplete | Tasks run on a user-managed warehouse or serverless; history is in `TASK_HISTORY` view. | [Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro) |
| "Dynamic Tables are zero-lag" | False | They meet a target lag; not real-time. Use streams+tasks or Snowpipe Streaming for sub-second. | [Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about) |
| "Snowpark runs on your laptop" | Wrong | Snowpark DataFrame operations compile to SQL that runs on a Snowflake warehouse. UDFs run in Snowflake's Python sandbox. | [Snowpark](https://docs.snowflake.com/en/developer-guide/snowpark/python/index) |
| "Iceberg tables are always Snowflake-managed" | False | Two modes; externally managed means an outside catalog writes; Snowflake is read/compute. | [Iceberg tables](https://docs.snowflake.com/en/user-guide/tables-iceberg); *DEA §1.7, p. 6* |
| "External functions are low latency" | False | Per-call HTTPS round-trip; batch your inputs. | [External functions](https://docs.snowflake.com/en/sql-reference/external-functions) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Build a stream + task MERGE pipeline and explain stream staleness.
- [ ] Rewrite that pipeline as a Dynamic Table and explain when each is preferable.
- [ ] Write and deploy a Snowpark Python UDF with an Anaconda dependency.
- [ ] Differentiate UDF / UDTF / UDAF / external function.
- [ ] Explain managed vs externally managed Iceberg catalogs.
