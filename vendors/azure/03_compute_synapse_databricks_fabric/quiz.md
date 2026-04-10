# Module 03 — Quiz (Compute)

1. You call `df.filter(...).groupBy(...).agg(...).show()`. When does computation happen?
   - A. Immediately on `filter`.
   - B. When `show` (an action) triggers execution of the logical plan.
   - C. Only when you call `write`.
   - D. Never, until a notebook is exported.

2. Which Spark operation is a full shuffle that can increase or decrease the number of partitions?
   - A. `coalesce(n)`
   - B. `repartition(n)`
   - C. `cache()`
   - D. `persist()`

3. You join a 10 TB fact table with a 20 MB dimension. Which strategy is safest for performance?
   - A. Shuffle join both sides.
   - B. Broadcast the 20 MB dimension to all executors.
   - C. Broadcast the 10 TB fact table.
   - D. Collect the fact table to the driver.

4. Which MERGE clause deletes target rows that have no match in the source?
   - A. `WHEN MATCHED THEN DELETE`
   - B. `WHEN NOT MATCHED THEN DELETE`
   - C. `WHEN NOT MATCHED BY SOURCE THEN DELETE`
   - D. `WHEN NOT MATCHED BY TARGET THEN DELETE`

5. In Fabric Warehouse T-SQL, which of the following is NOT supported?
   - A. `COPY INTO` from ADLS Parquet
   - B. `MERGE`
   - C. `CREATE INDEX` (non-clustered rowstore)
   - D. Stored procedures

6. You have a 500 GB fact table frequently joined on `customer_id` and a 50 MB dimension in a Synapse dedicated SQL pool. Best distributions?
   - A. Hash fact on `customer_id`; replicate dimension.
   - B. Round-robin both.
   - C. Replicate fact; hash dimension on `customer_id`.
   - D. Hash both on `customer_id`.

7. Which language queries an Eventhouse / KQL database in Fabric Real-Time Intelligence?
   - A. T-SQL
   - B. Power Query M
   - C. KQL (Kusto Query Language)
   - D. Spark SQL

8. A KQL query to count events per 5-minute bin in the last hour would start with:
   - A. `SELECT COUNT(*) GROUP BY dateadd(...)`
   - B. `Events | where Timestamp > ago(1h) | summarize count() by bin(Timestamp, 5m)`
   - C. `df.groupBy(window(...))`
   - D. `@pipeline().parameters.window`

9. In Fabric Warehouse, the storage format for tables is:
   - A. Proprietary columnstore inaccessible to Spark.
   - B. Delta Lake in OneLake, readable by Spark notebooks.
   - C. CSV in ADLS Gen2.
   - D. Parquet without a transaction log.

10. A Fabric notebook writes 10,000 small Delta files. Which command compacts them?
    - A. `VACUUM`
    - B. `OPTIMIZE`
    - C. `DESCRIBE HISTORY`
    - D. `REFRESH TABLE`

---

## Answer key

1. **B** — Lazy evaluation; action triggers execution (`../../../../azure_certified/flashcards/top-33-flashcards.md` Card 2).
2. **B** — `repartition` full shuffle (`../../../../azure_certified/IMPLEMENTATION-PLAN.md:L287-L295`).
3. **B** — Broadcast the small side; [Spark SQL performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html).
4. **C** — `WHEN NOT MATCHED BY SOURCE` ([Delta MERGE](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/delta-merge-into)).
5. **C** — Fabric Warehouse is columnstore-only; no user index DDL ([T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area)).
6. **A** — Hash fact, replicate small dim ([distributions](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-distribute)).
7. **C** — [KQL reference](https://learn.microsoft.com/en-us/kusto/query/).
8. **B** — Standard KQL `summarize ... by bin()` ([KQL tutorial](https://learn.microsoft.com/en-us/kusto/query/tutorial)).
9. **B** — [Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing).
10. **B** — [Delta OPTIMIZE](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order).
