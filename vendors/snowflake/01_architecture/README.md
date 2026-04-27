# Module 01: Snowflake Architecture

Snowflake's three-layer architecture is the single highest-yield topic across all three certs. Platform Domain 1.0 weights it at 35% and Core Domain 1.0 at 24%. Understanding it cold unlocks correct answers on warehouses, storage, caching, and workload isolation questions in later modules.

## Learning goals
- Name the three architecture layers and one responsibility of each, without notes.
- Explain **separation of storage and compute** and why it enables workload isolation.
- Define a **micro-partition** and list three pieces of metadata Snowflake tracks per micro-partition.
- Distinguish the three cache types (metadata, result, warehouse) and a trigger that invalidates each.
- Identify which layer is always-on and cannot be suspended.

## Prerequisites
- `../00_exam_profile/` — know which exam each concept is weighted for.

## Reading order
1. This README
2. [Snowflake Architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts) (layers, key facts)
3. [Snowflake Quickstarts](https://quickstarts.snowflake.com/) — hands-on architecture labs
4. `quiz.md`

## Concepts

### The three layers (HIGH-YIELD)
Snowflake decomposes into **Database Storage**, **Query Processing (Virtual Warehouses)**, and **Cloud Services**. Storage is compressed columnar files in cloud object storage (S3, Azure Blob, or GCS) that Snowflake manages internally — users never touch the raw files. Query Processing is one or more virtual warehouses (MPP clusters of cloud VMs) that can start, stop, resize, and clone without affecting stored data. Cloud Services is the always-on control plane that handles authentication, metadata, query parsing and optimization, and transactions.

Ref: *SnowPro Associate: Platform Study Guide, §1.1 "Outline key features", p. 5* · [Snowflake Architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts).

### Separation of storage and compute
Legacy warehouses couple storage and compute; scaling one requires scaling the other. Snowflake decouples them, so multiple warehouses can read the same storage concurrently without contention — this is **workload isolation**. Suspending a warehouse stops billing on that compute cluster without affecting stored data. Cloud Services is always on and cannot be suspended.

Ref: [Snowflake key concepts](https://docs.snowflake.com/en/user-guide/intro-key-concepts).

### Micro-partitions and metadata
Snowflake stores tables as immutable **micro-partitions**, each typically 50-500 MB of uncompressed data (~16 MB compressed). For every micro-partition Snowflake records column min/max, distinct counts, null counts, and the range of values — this metadata drives **static pruning** during query planning. You cannot read or write micro-partitions directly; they are managed internally and rewritten when you run DML that touches them.

Ref: [Micro-partitions & data clustering](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions) · *SnowPro Core Study Guide, §1.4 "Outline Snowflake storage concepts", p. 6*.

### Cache types
Three distinct caches, each with different invalidation rules:
- **Metadata cache** — in Cloud Services; serves queries like `SELECT COUNT(*) FROM t` without touching a warehouse. Invalidated by DML on the table.
- **Result cache** — in Cloud Services; persists query results for 24 hours (extended up to 31 days on re-use). Invalidated by any change to the underlying data or by any non-deterministic function in the query.
- **Warehouse (local disk) cache** — SSD on each warehouse's VMs. Cleared when the warehouse is suspended or resized.

Ref: [Using persisted query results](https://docs.snowflake.com/en/user-guide/querying-persisted-results) · *SnowPro Core Study Guide, Domain 3.0 "Performance and Cost Optimization", p. 8*.

### Object hierarchy
Account -> Database -> Schema -> object (table, view, stage, pipe, stream, task, UDF, stored proc, sequence, file format). Every object's fully qualified name is `database.schema.object`. Privileges cascade along this hierarchy and are evaluated with **future grants**.

Ref: *SnowPro Associate: Platform Study Guide, §1.5 "Snowflake objects and hierarchy", p. 5* · [Snowflake Architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts).

## Hands-on drills

| # | Drill | Est. time | Source |
|---|---|---|---|
| D1 | Create database/schema/warehouse, observe the three layers in Snowsight Admin. | 20 min | [Snowflake Quickstarts](https://quickstarts.snowflake.com/) |
| D2 | Explore the SNOWFLAKE_SAMPLE_DATA TPCH database and inspect a table's micro-partition count via `SYSTEM$CLUSTERING_INFORMATION`. | 20 min | [Snowflake Quickstarts](https://quickstarts.snowflake.com/) |
| D3 | Run the same `SELECT` twice and confirm the second hits the result cache (Query Profile shows no bytes scanned from storage). | 15 min | [Using persisted query results](https://docs.snowflake.com/en/user-guide/querying-persisted-results) |
| D4 | Suspend and resize a warehouse, re-run D3, confirm the warehouse (SSD) cache was cleared. | 15 min | *SnowPro Core Study Guide, Domain 3.0, p. 8* |
| D5 | Create a view and a secure view over `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER`; confirm secure views do not expose underlying data lineage to unprivileged roles. | 20 min | [Snowflake Quickstarts](https://quickstarts.snowflake.com/) |

## Common failures (exam gotchas)

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| "Suspending a warehouse frees storage" | Confusing compute with storage | Warehouses are compute only. Suspending affects only compute billing. | `domain_1_0_architecture.md:L84` |
| "Cloud Services can be suspended to save cost" | False | Cloud Services is always on; billed only if it exceeds 10% of daily compute spend. | `domain_1_0_architecture.md:L85` |
| "Result cache always serves stale reads" | Misremembering | Result cache invalidates immediately on any DML touching source data. | [docs](https://docs.snowflake.com/en/user-guide/querying-persisted-results) |
| "Micro-partitions are Parquet" | Format assumption | Snowflake uses a proprietary columnar format; not directly readable. | *Platform Guide §1.1, p. 5* |
| "Resizing a warehouse preserves cache" | Wrong | Resizing provisions new VMs; local disk cache is cleared. | *Core Guide §3.0, p. 8* |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Draw the three layers and label which is always-on.
- [ ] Explain why two warehouses reading the same table do not contend.
- [ ] Name three metadata attributes Snowflake tracks per micro-partition.
- [ ] Describe an invalidation rule for each of the three caches.
