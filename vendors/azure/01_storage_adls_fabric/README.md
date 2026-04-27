# Module 01 — Storage: ADLS Gen2, OneLake, Fabric Lakehouse

> DP-700 exam weight: folds into Domain 2 (Ingest and transform data — storage design) plus Domain 1 (governance of OneLake artifacts). Roughly 20–25 hours of study.

## Learning goals

- Explain the ADLS Gen2 object hierarchy (account → container → directory → file) and the purpose of the hierarchical namespace (HNS).
- Describe OneLake as a single logical data lake built on ADLS Gen2 and the "one copy of data" principle.
- Create a Fabric Lakehouse and a Fabric Warehouse in the same workspace and explain how each surfaces tables to the SQL analytics endpoint.
- Use OneLake shortcuts and Fabric mirroring to virtualize data without copy.
- Choose partitioning, file size, and Delta Lake layout (V-Order + OPTIMIZE) for analytical workloads.
- Describe how the `abfss://` and `https://onelake.dfs.fabric.microsoft.com/` URIs address the same underlying bytes.

## Prerequisites

- Unified course `phase_3_core_tools/` Delta Lake and Parquet modules.
- `00_exam_profile/README.md`.

## Concepts

### ADLS Gen2 and the hierarchical namespace

ADLS Gen2 is Azure Blob Storage with a **hierarchical namespace (HNS)** that gives directory-level operations, POSIX ACLs, and atomic renames. HNS is irreversible once enabled and cannot be turned off; it is set at storage account creation or by running `Invoke-AzStorageAccountHierarchicalNamespaceUpgrade`, which causes downtime. Without HNS, you still have Blob Storage but lose rename atomicity, ACLs, and the Data Lake Storage SDK path semantics.
Ref: [ADLS Gen2 introduction](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)

### OneLake — the logical lake for Fabric

OneLake is a single, tenant-wide logical data lake automatically provisioned with every Fabric tenant. It sits on ADLS Gen2 but is exposed through a unified namespace: `https://onelake.dfs.fabric.microsoft.com/<workspace>/<item>.<itemtype>/Files/...`. The "one copy of data" promise: multiple Fabric items (Lakehouse, Warehouse, KQL Database, Power BI semantic models) can read the same Delta tables from OneLake without duplication.
Ref: [OneLake overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview)

### Fabric Lakehouse vs Fabric Warehouse

Both live in OneLake and store data as **Delta Lake tables** (Parquet + `_delta_log`), but they differ in their compute and write path. A **Lakehouse** is Spark-first: you use notebooks, Dataflow Gen2, or pipelines to write Delta files, and you read via the auto-provisioned SQL analytics endpoint (read-only T-SQL). A **Warehouse** is T-SQL-first and read/write via T-SQL DDL/DML (`CREATE TABLE`, `INSERT`, `UPDATE`, `MERGE`, `COPY INTO`), still writing Delta under the hood. Within a workspace, Warehouse tables show up in the Lakehouse's SQL endpoint as external references through OneLake.
Ref: [Fabric Lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview) · [Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing)

### OneLake shortcuts and mirroring

**Shortcuts** are symbolic links to data stored outside a Fabric item — other workspaces, other OneLakes, ADLS Gen2, Amazon S3, Google Cloud Storage, Dataverse — exposed as if local. Shortcuts are read-through virtualization; they do not copy data. **Mirroring** replicates a source database (Azure SQL Database, Cosmos DB, Snowflake) into OneLake in near real time as Delta tables, enabling analytical queries without ETL. Both are central to DP-700 and together replace the DP-203 concepts of linked services + external tables + Polybase.
Ref: [OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts) · [Fabric mirroring](https://learn.microsoft.com/en-us/fabric/database/mirrored-database/overview)

### Delta Lake in Fabric: V-Order + OPTIMIZE

Fabric writes Delta with **V-Order** by default — an additional shuffle and sort during write that improves read performance for Power BI, SQL endpoint, and Spark at the cost of ~15% write time. `OPTIMIZE` compacts small files (target 256 MB – 1 GB); `OPTIMIZE ... ZORDER BY (col)` co-locates data on up to 3–4 columns; `VACUUM` removes files older than retention (default 7 days — shorter retention breaks time travel).
Ref: [Delta optimization and V-Order in Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order) · [Delta Lake table maintenance](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance)

### Partitioning and file sizing

Partition Hive-style (`year=2024/month=01/day=15/...`). Target files 256 MB – 1 GB compressed Parquet. Anti-pattern: partitioning on high-cardinality columns (e.g., `customer_id`) produces thousands of tiny files and crushes query planners. Guidance: partition when data exceeds tens of GB and queries consistently filter on the partition column.
Ref: [Delta optimization and V-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order) — see partitioning guidance

### Service comparison: Synapse dedicated pool vs Fabric Warehouse

| Feature | Synapse dedicated SQL pool (DP-203 legacy) | Fabric Warehouse (DP-700 current) |
|---|---|---|
| Storage | Proprietary columnstore | OneLake Delta (open format) |
| Distribution tuning | Hash / round-robin / replicated | Automatic; no user-visible distributions |
| DWU scaling | Manual / paused | Capacity-based (F-SKUs), pay-as-you-go |
| Loading pattern | Stage heap RR → CTAS to hash CCI | `COPY INTO` or T-SQL INSERT directly into Delta |
| PolyBase / external tables | Yes (key topic in DP-203) | Replaced by shortcuts and mirroring |
| Cross-engine reads | Requires external table plumbing | SQL endpoint + Spark read the same Delta files |

Ref: [Fabric Warehouse vs Lakehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing)

## Labs

| Lab | Goal | Est. time | Source |
|---|---|---|---|
| L01.1 Delta fundamentals | MERGE, time travel, history on a local/Databricks notebook; adapt logic to a Fabric notebook | 60 m | [Microsoft Learn: Delta Lake](https://learn.microsoft.com/en-us/azure/databricks/delta/) |
| L01.2 OneLake shortcut | Create a shortcut from a Lakehouse to an ADLS Gen2 container; query the shortcut table via SQL endpoint | 45 m | [OneLake shortcuts how-to](https://learn.microsoft.com/en-us/fabric/onelake/create-onelake-shortcut) |
| L01.3 Warehouse load | `COPY INTO` a Fabric Warehouse from ADLS Gen2 Parquet; verify via SQL endpoint | 45 m | [Load data using COPY statement](https://learn.microsoft.com/en-us/fabric/data-warehouse/ingest-data-copy) |
| L01.4 Partition strategy | Reproduce the "thousands of 1 MB files" anti-pattern, then fix with `OPTIMIZE` | 30 m | [Delta optimization and V-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order) |

## Common failures

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `abfss://` URI fails to list directories | HNS not enabled on the storage account | Recreate account with HNS, or upgrade (irreversible, downtime) | [ADLS Gen2 access](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction) |
| Time travel to yesterday fails after `VACUUM RETAIN 0 HOURS` | VACUUM removed the underlying Parquet files | Never VACUUM below 168 h in production | [Delta Lake table maintenance](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance) |
| Fabric Warehouse table not visible in Lakehouse SQL endpoint | Warehouse and Lakehouse are in different workspaces | Use a shortcut, or move the items into a common workspace | [Fabric Warehouse docs](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing) |
| Small files degrade SQL endpoint performance | Writers produced micro-batches without OPTIMIZE | Schedule `OPTIMIZE` + rely on V-Order default | [Delta optimization](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order) |

## References

See [references.md](./references.md). Quiz in [quiz.md](./quiz.md).

## Checkpoint

- [ ] I can draw OneLake as ADLS Gen2 + a logical namespace and explain what a shortcut is.
- [ ] I can load data into a Fabric Warehouse two ways (`COPY INTO`, pipeline).
- [ ] I can run OPTIMIZE on a Delta table in a Fabric notebook and check file count before/after.
- [ ] I can articulate the Synapse dedicated pool → Fabric Warehouse migration story to a teammate.
