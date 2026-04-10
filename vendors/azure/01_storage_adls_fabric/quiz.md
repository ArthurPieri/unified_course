# Module 01 — Quiz (Storage)

1. What does enabling hierarchical namespace (HNS) on an Azure storage account provide that flat Blob Storage does not?
   - A. Automatic encryption at rest.
   - B. POSIX ACLs, atomic directory renames, and Data Lake SDK path semantics.
   - C. Cross-region replication.
   - D. Lifecycle policies.

2. You created a storage account for ADLS Gen2 but forgot to enable HNS. Which statement is true?
   - A. You can enable HNS at any time with no downtime and no data loss.
   - B. You must delete and recreate the account; upgrade is impossible.
   - C. You can upgrade using `Invoke-AzStorageAccountHierarchicalNamespaceUpgrade`, which causes downtime and is irreversible.
   - D. You can toggle HNS on and off as needed.

3. Which Fabric feature exposes data that physically lives outside a Fabric item without copying it?
   - A. Fabric mirroring.
   - B. Dataflow Gen2.
   - C. OneLake shortcut.
   - D. V-Order.

4. Fabric mirroring is best described as:
   - A. A shortcut to an S3 bucket.
   - B. Near-real-time replication of a source database (Azure SQL DB, Cosmos DB, Snowflake) into OneLake as Delta tables.
   - C. A backup of a Lakehouse to another region.
   - D. A lift-and-shift of SSIS packages.

5. You write data to a Fabric Lakehouse with default settings. Which optimization is applied automatically?
   - A. Z-ORDER by primary key.
   - B. V-Order write-time shuffle and sort.
   - C. Automatic partitioning by date.
   - D. Bloom filters.

6. In the same Fabric workspace you have a Lakehouse and a Warehouse. Which statement is correct?
   - A. They store data in incompatible proprietary formats.
   - B. Both store data as Delta Lake in OneLake, and the Warehouse supports T-SQL DDL/DML while the Lakehouse is Spark-first with a read-only SQL analytics endpoint.
   - C. The Lakehouse supports T-SQL updates; the Warehouse does not.
   - D. Only the Warehouse supports Delta Lake.

7. You run `VACUUM my_delta_table RETAIN 0 HOURS`. What happens to time travel queries that reference versions older than the current one?
   - A. They are unaffected.
   - B. They return an empty result set.
   - C. They fail because the underlying Parquet files have been deleted.
   - D. Time travel is automatically re-built from the transaction log.

8. You have a 100 M-row table partitioned by `customer_id` (5 M distinct customers). Queries are slow. Why?
   - A. Not enough DWUs.
   - B. High-cardinality partitioning produces thousands of tiny files, overwhelming the query planner.
   - C. Delta V-Order is disabled.
   - D. The columnstore index is fragmented.

9. Which of the following is the Fabric-era replacement for Synapse PolyBase external tables that pointed at ADLS Gen2?
   - A. Linked services.
   - B. OneLake shortcuts and Fabric mirroring.
   - C. Dataflow Gen2.
   - D. Integration Runtime.

10. Target file size after `OPTIMIZE` on a Fabric Delta table is approximately:
    - A. 10–50 MB
    - B. 256 MB – 1 GB
    - C. 5–10 GB
    - D. 10–100 KB

---

## Answer key

1. **B** — [ADLS Gen2 introduction](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction).
2. **C** — Irreversible HNS upgrade; [ADLS Gen2 upgrade](https://learn.microsoft.com/en-us/azure/storage/blobs/upgrade-to-data-lake-storage-gen2-how-to) and `../../../../azure_certified/IMPLEMENTATION-PLAN.md:L178-L185`.
3. **C** — [OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts).
4. **B** — [Fabric mirroring](https://learn.microsoft.com/en-us/fabric/database/mirrored-database/overview).
5. **B** — [Delta optimization and V-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order).
6. **B** — [Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing) and [Fabric Lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview).
7. **C** — [Delta Lake VACUUM](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance); `../../../../azure_certified/IMPLEMENTATION-PLAN.md:L197-L220`.
8. **B** — Over-partitioning anti-pattern; `../../../../azure_certified/IMPLEMENTATION-PLAN.md:L210-L235`.
9. **B** — Shortcuts + mirroring replace external tables in Fabric ([OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts)).
10. **B** — [Delta optimization](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order).
