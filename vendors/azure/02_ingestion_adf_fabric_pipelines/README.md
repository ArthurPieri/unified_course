# Module 02 — Ingestion: ADF, Synapse Pipelines, Fabric Data Factory, Dataflow Gen2

> DP-700 exam weight: core of Domain 2 (Ingest and transform data, 30–35%). Roughly 25–30 hours of study — the heaviest single module.

## Learning goals

- Distinguish Copy Activity (movement only) from Mapping Data Flows and Dataflow Gen2 (transformation).
- Design an incremental-load pipeline using the watermark pattern.
- Write a Dataflow Gen2 with Power Query M to clean and reshape a batch input.
- Choose the right trigger (schedule vs tumbling window vs event-based) for a scenario.
- Parameterize pipelines and pass values between activities using expressions.
- Map legacy ADF / Synapse pipeline concepts to their Fabric Data Factory equivalents.

## Prerequisites

- `01_storage_adls_fabric/README.md`
- `phase_3_core_tools/` dbt or orchestration module (for pipeline design intuition).

## Concepts

### Azure Data Factory, Synapse Pipelines, Fabric Data Factory — one engine, three wrappers

**Azure Data Factory (ADF)** is Azure's standalone orchestration and data-movement service. **Synapse Pipelines** is ADF embedded in a Synapse workspace — same runtime, same activities, same JSON definitions. **Fabric Data Factory** is the Fabric incarnation with two surfaces: **Pipelines** (visually indistinguishable from ADF, minus a few activities and with Fabric-native sinks) and **Dataflow Gen2** (Power Query M transformations on the Fabric Spark runtime). DP-700 tests Fabric Pipelines + Dataflow Gen2 primarily, but you must still recognize ADF artifacts because most DP-700 candidates migrate from them.
Ref: [Fabric Data Factory](https://learn.microsoft.com/en-us/fabric/data-factory/) · [Azure Data Factory introduction](https://learn.microsoft.com/en-us/azure/data-factory/introduction) · `../../../azure_certified/IMPLEMENTATION-PLAN.md:L304-L325`

### Copy Activity — movement only

Copy Activity is the 90+-connector data-movement workhorse. It reads from a source, optionally applies format conversions and column mappings, and writes to a sink. It does **not** transform: no joins, no aggregations, no derived columns beyond simple mapping. Key tunables: Data Integration Units (DIUs, max 256), parallel copies, and staging via Blob/ADLS for cross-cloud hops. Fault tolerance: skip incompatible rows, log to a file for reprocessing.
Ref: [Copy activity](https://learn.microsoft.com/en-us/fabric/data-factory/copy-data-activity) · `../../../azure_certified/labs/04-batch-and-pipeline-patterns.md:L7-L450`

### Mapping Data Flows (ADF) and Dataflow Gen2 (Fabric)

**Mapping Data Flows** in ADF/Synapse are visual Spark-based transformations (Derived Column, Aggregate, Join, Pivot, Conditional Split, Flatten). Microsoft wrote the code generator so users without Spark experience can build jobs. **Dataflow Gen2** in Fabric replaces this with **Power Query M** — the same language used by Power BI and Excel — running on Fabric's Spark compute with OneLake as sink. DP-700 tests Dataflow Gen2 heavily because it is both new and Fabric-specific: M functions, step-by-step transformations, staging, destinations, and refresh behavior.
Ref: [Dataflow Gen2 overview](https://learn.microsoft.com/en-us/fabric/data-factory/dataflows-gen2-overview) · [Power Query M reference](https://learn.microsoft.com/en-us/powerquery-m/power-query-m-function-reference)

### Incremental load — watermark pattern

The canonical three-step: (1) **Lookup** reads the last watermark from a control table, (2) **Copy Activity** issues `SELECT * WHERE modified_date > @{activity('Lookup').output.firstRow.watermark}`, (3) a **Stored Procedure** or Script activity updates the control table to the new maximum. Failure between step 2 and step 3 re-copies rows on the next run — design your sink to be idempotent (Delta `MERGE`, upsert, or dedup key).
Ref: `../../../azure_certified/IMPLEMENTATION-PLAN.md:L315-L325` · `../../../azure_certified/flashcards/top-33-flashcards.md` Card 8

### Change data capture options

- **SQL Server CDC / Azure SQL CDC** — change tables consumed via a CDC-aware source dataset.
- **Cosmos DB Change Feed** — pull via Copy Activity or a Spark connector.
- **Databricks Auto Loader** — `cloudFiles` with file-notification mode on ADLS Gen2, incremental by directory listing or Event Grid.
- **Delta Change Data Feed (CDF)** — `readChangeFeed` emits row-level deltas from a Delta table to downstream consumers.
- **Fabric mirroring** — zero-ETL CDC for Azure SQL DB, Cosmos DB, Snowflake; see module 01.

Ref: [Delta CDF](https://learn.microsoft.com/en-us/azure/databricks/delta/delta-change-data-feed) · `../../../azure_certified/IMPLEMENTATION-PLAN.md:L315-L325`

### Triggers

| Trigger | Use case | Key feature |
|---|---|---|
| Schedule | Hourly/daily cron-like | Many-to-many with pipelines; fire-and-forget |
| Tumbling window | Time-slice processing with backfill | Stateful, can backfill, supports dependencies between windows |
| Event-based (Storage) | File-arrival processing | Requires Event Grid subscription |
| Custom event | Custom Event Grid topics | Flexible event-driven |
| Manual | Ad-hoc testing | "Trigger now" / REST API |

If the question mentions *backfill* or *one execution per date partition with dependencies*, the answer is almost always tumbling window.
Ref: `../../../azure_certified/flashcards/top-33-flashcards.md` Card 12 · [ADF triggers](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipeline-execution-triggers)

### Integration Runtime (ADF / Synapse Pipelines)

| IR type | Location | Use case |
|---|---|---|
| Azure IR | Azure-managed | Cloud-to-cloud movement and transforms |
| Self-hosted IR | Your network | On-premises / private network sources |
| Azure-SSIS IR | Azure-managed | Lift-and-shift SSIS packages |

Fabric Data Factory currently uses Fabric capacity compute (no user-visible IRs); **on-premises data gateways** play the equivalent role of self-hosted IR for Fabric.
Ref: [Integration runtime](https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime) · [On-premises data gateway for Fabric](https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-onprem)

### Parameterization and expressions

Pipeline parameters (`@pipeline().parameters.x`), activity outputs (`@activity('Name').output.firstRow.col`), system variables (`@pipeline().RunId`, `@utcnow()`), and global parameters for environment promotion. Dynamic content lets you compose folder paths: `@concat('bronze/', formatDateTime(utcnow(), 'yyyy/MM/dd'))`.
Ref: [Expressions and functions](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-expression-language-functions)

## Labs

| Lab | Goal | Est. time | Source |
|---|---|---|---|
| L02.1 Copy + Data Flow | Build Copy Activity → Mapping Data Flow pipeline in ADF portal (sandbox) | 60 m | `../../../azure_certified/labs/04-batch-and-pipeline-patterns.md:L7-L450` |
| L02.2 Watermark incremental | Implement Lookup → Copy → Stored Procedure watermark pipeline | 60 m | `../../../azure_certified/labs/04-batch-and-pipeline-patterns.md:L842-L1424` |
| L02.3 Dataflow Gen2 in Fabric | Ingest a CSV, apply M transformations, land in a Lakehouse | 45 m | [Dataflow Gen2 quickstart](https://learn.microsoft.com/en-us/fabric/data-factory/create-first-dataflow-gen2) |
| L02.4 Tumbling window backfill | Configure a tumbling window trigger and backfill 7 days | 30 m | `../../../azure_certified/labs/04-batch-and-pipeline-patterns.md:L1424-L1850` |

## Common failures

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Copy Activity "cannot transform" | Tried to add derived columns in Copy | Use Mapping Data Flow or Dataflow Gen2 | [Copy activity](https://learn.microsoft.com/en-us/fabric/data-factory/copy-data-activity) |
| Rows duplicated after pipeline retry | Watermark updated before failure in copy sink | Make sink idempotent (Delta MERGE / upsert) | `../../../azure_certified/flashcards/top-33-flashcards.md` Card 8 |
| On-premises source unreachable | Azure IR only; no self-hosted IR / on-prem gateway | Install self-hosted IR (ADF) or on-premises data gateway (Fabric) | [IR concepts](https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime) |
| Tumbling window pipeline runs but does not backfill | Used Schedule trigger instead | Switch to Tumbling Window trigger with start time in the past | [ADF triggers](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipeline-execution-triggers) |

### ADF / Synapse vs Fabric Data Factory — service comparison

| Concept | ADF / Synapse Pipelines | Fabric Data Factory |
|---|---|---|
| Orchestration artifact | Pipeline (JSON) | Pipeline (visual, Fabric-hosted) |
| Code-based transforms | Mapping Data Flow (Spark) | Dataflow Gen2 (Spark + Power Query M) |
| On-prem connectivity | Self-hosted IR | On-premises data gateway |
| Source code | Git integration to Azure Repos / GitHub | Git integration + deployment pipelines |
| Compute billing | DIUs / cluster cores | Fabric capacity units |
| Lineage to catalog | Purview integration | Fabric governance + Purview |

Ref: [Fabric Data Factory](https://learn.microsoft.com/en-us/fabric/data-factory/) · `../../../azure_certified/IMPLEMENTATION-PLAN.md:L304-L390`

## References

See [references.md](./references.md). Quiz in [quiz.md](./quiz.md).

## Checkpoint

- [ ] I can name the three Integration Runtime types and when to use each.
- [ ] I can sketch a watermark incremental pipeline and describe what happens on failure.
- [ ] I can build a Dataflow Gen2 with at least five Power Query M steps.
- [ ] I can choose the correct trigger type for "backfill 90 days of partitioned data".
