# Quiz — 02 ETL / ELT Patterns

10 multiple-choice questions. Pick the single best answer. Answer key with source citations at the bottom.

---

**Q1.** In an ELT lakehouse stack built on dlt + dbt + Trino, where does the "T" execute?
- A. Inside the dlt Python process before the load step
- B. In a dedicated ETL tier separate from the warehouse
- C. In the query engine (Trino) against already-loaded raw data
- D. In the source database before extraction

**Q2.** Which change-detection strategy reliably captures row deletes without scanning the full source table?
- A. Watermark on an `updated_at` column
- B. Snapshot-diff against yesterday's dump
- C. Log-based CDC (e.g., Debezium reading the WAL/binlog)
- D. Full refresh

**Q3.** A pipeline appends rows to a target table on every run with no partitioning key tied to the run. A transient failure causes a retry. What is the most likely correctness issue?
- A. The second run is a no-op
- B. Rows from the first attempt are double-counted
- C. The target table loses rows
- D. The schema evolves unexpectedly

**Q4.** The two design rules that most directly buy a pipeline step idempotency are:
- A. Retry on failure, and log every action
- B. Deterministic partition targets, and transactional/atomic commits
- C. Use an orchestrator, and enable email alerts
- D. Cache source responses, and compress the output

**Q5.** In a Medallion architecture, which statement correctly describes the Bronze layer?
- A. Bronze holds business-ready aggregates consumed by BI
- B. Bronze enforces data contracts and type coercion
- C. Bronze holds raw ingested data, acts as the replay buffer, and is append-only
- D. Bronze is optional if you have CDC

**Q6.** Which backfill approach is safest when fixing a bug in a Silver transformation?
- A. Append a "correction delta" to the affected partitions
- B. Rerun the Silver transform scoped to the affected partition range, overwriting those partitions
- C. Drop and recreate the whole Silver table in place during business hours
- D. Edit the affected rows manually in the Gold layer

**Q7.** A dlt resource is declared with `write_disposition="append"` and `dlt.sources.incremental("tpep_pickup_datetime")`. On a second run with no new source rows, what happens?
- A. The pipeline errors because the cursor is exhausted
- B. All rows are reloaded and duplicated
- C. No new rows are forwarded downstream
- D. Only rows where the cursor is NULL are loaded

**Q8.** What is the key structural difference between an Airflow DAG and a Dagster asset graph?
- A. Airflow DAGs can have cycles; Dagster graphs cannot
- B. Airflow nodes are tasks (imperative "run this"); Dagster nodes are assets (declarative "this dataset should exist")
- C. Dagster does not support scheduling
- D. Airflow cannot run Python code

**Q9.** A source table has an `updated_at` column that is **not** touched when certain columns are edited. You use a watermark incremental pipeline. What will you miss?
- A. Inserts with future timestamps
- B. Updates that do not modify the watermark column
- C. Rows with NULL primary keys
- D. Nothing — watermark is equivalent to CDC

**Q10.** Why did ELT displace ETL for analytics in the lakehouse era?
- A. Object storage + MPP engines made "load raw, transform later" cheaper than a separate ETL tier, and SQL-first transform tools made the T reproducible
- B. ELT is required by the Iceberg specification
- C. Data contracts only work in ETL
- D. ELT eliminates the need for a DAG

---

## Answer key

| Q | Answer | Source |
|---|---|---|
| 1 | C | `../dataeng/enhanced-plan.md:L460` ("this stack is ELT: dlt = E+L, dbt = T, Trino = compute"); [dbt documentation](https://docs.getdbt.com/docs/introduction) |
| 2 | C | *DDIA, Kleppmann, Ch. 11*; [Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html) |
| 3 | B | *DDIA, Kleppmann, Ch. 7* (atomicity and retries); [Iceberg spec](https://iceberg.apache.org/spec/) |
| 4 | B | *DDIA, Kleppmann, Ch. 7*; [Iceberg spec](https://iceberg.apache.org/spec/) |
| 5 | C | [Databricks Medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion) |
| 6 | B | [Dagster concepts](https://docs.dagster.io/concepts); `../dataeng/enhanced-plan.md:L1565` |
| 7 | C | [dlt incremental loading](https://dlthub.com/docs/general-usage/incremental-loading); `../dataeng/dlt_pipelines/taxi_pipeline.py:L52-L110` |
| 8 | B | [Airflow core concepts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html); [Dagster concepts](https://docs.dagster.io/concepts) |
| 9 | B | *DDIA, Kleppmann, Ch. 11* (change-detection limitations of timestamp cursors) |
| 10 | A | *Fundamentals of Data Engineering*, Reis & Housley (lifecycle framing); `../dataeng/enhanced-plan.md:L460` |
