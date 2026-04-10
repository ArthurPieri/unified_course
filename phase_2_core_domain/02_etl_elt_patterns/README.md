# Module 02: ETL / ELT Patterns (10h)

## Learning goals
- Explain where the "T" runs in ETL vs. ELT and why ELT dominates modern analytics lakehouses
- Pick between full-refresh, incremental-append, and incremental-merge load strategies for a given source
- Choose between CDC, snapshot-diff, and watermark-based change detection based on source capabilities
- Define idempotency for a pipeline run and state two concrete design rules that preserve it
- Map a pipeline to the Bronze/Silver/Gold (Medallion) layers and justify the boundary between layers
- Execute a targeted backfill without corrupting existing Gold tables
- Distinguish a DAG from a "pipeline" and explain why orchestrators use DAGs

## Prerequisites
- [../01_data_modeling/README.md](../01_data_modeling/README.md)
- [../../phase_1_foundations/05_sql_postgres/README.md](../../phase_1_foundations/05_sql_postgres/README.md)

## Reading order
1. This README
2. `labs/lab_02_dlt_incremental/` (build in Phase 3 · 04_dlt)
3. `quiz.md`

## Concepts

### ETL vs. ELT — where does the T run?
In **ETL**, raw data is pulled, transformed in a dedicated processing tier (historically an ETL server running SSIS/Informatica/Talend), and only the cleaned, conformed output is loaded into the warehouse. In **ELT**, raw data is loaded first into scalable storage (object store, MPP warehouse, or lakehouse) and transformed in place using the same engine that serves analytics. ELT won for analytics once object storage and MPP engines made "load everything, transform later" cheaper than pre-processing in a separate tier, and once SQL-first transformation tools made the T reproducible in version control (`*Fundamentals of Data Engineering*, Reis & Housley`, lifecycle chapter; `../dataeng/enhanced-plan.md:L460` describes the course stack as ELT where `dlt = E+L, dbt = T, Trino = compute`). The practical consequence: in an ELT lakehouse you keep raw data forever, and every transformation is rerunnable from source.

Ref: [dlt documentation](https://dlthub.com/docs/intro) · [dbt documentation](https://docs.getdbt.com/docs/introduction)

### Full refresh vs. incremental
A **full refresh** truncates the target and reloads from source every run. It is the simplest correct pattern, survives arbitrary source mutations, and has no state. It becomes infeasible when source volume exceeds a run budget. **Incremental** loads read only rows changed since the last successful run; they require a reliable change signal (timestamp cursor, monotonic id, log sequence number) and per-run state. dlt implements incremental loading via a cursor column passed to `dlt.sources.incremental`, demonstrated at `../dataeng/dlt_pipelines/taxi_pipeline.py:L52-L110` where the `yellow_taxi_trips` resource declares `write_disposition="append"` and an incremental cursor on `tpep_pickup_datetime` so subsequent runs forward only rows newer than the last-seen timestamp.

Ref: [dlt incremental loading](https://dlthub.com/docs/general-usage/incremental-loading)

### CDC vs. snapshot-diff vs. watermark
Three change-detection strategies, ordered by fidelity and operational cost:

1. **Watermark (cursor)** — read rows `WHERE updated_at > :last_seen`. Cheap, works on any table with a reliable monotonically-updated timestamp or id, but cannot see deletes and misses updates that do not touch the cursor column.
2. **Snapshot-diff** — periodically dump the full source and diff against the prior snapshot. Captures deletes and all updates, but scales with total table size, not change volume.
3. **CDC (Change Data Capture)** — tail the database's write-ahead log (WAL / binlog / redo) and emit every row-level change as a stream. Captures inserts, updates, and deletes with ordering, without scanning the base table. Debezium is the canonical open-source implementation and reads the transaction log directly (`[Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html)`; *DDIA, Kleppmann, Ch. 11*).

CDC is the highest-fidelity option and the only one that captures deletes correctly without a full scan, which is why it is the default for replicating OLTP databases into a lakehouse (*DDIA, Kleppmann, Ch. 11*).

### Idempotency and re-runnability
A pipeline step is **idempotent** when running it N times with the same inputs produces the same output as running it once. The two design rules that buy you idempotency:

1. **Deterministic targets.** A run writes to a partition keyed on a run-input (date, batch id), not "append to the end." Re-running overwrites the partition; prior partitions are untouched.
2. **Transactional commits.** Either the entire partition is visible, or none of it is. Open table formats provide this: Iceberg commits are atomic snapshot swaps (`[Iceberg spec](https://iceberg.apache.org/spec/)`), so a failed or retried write never leaves a half-loaded partition. Without atomic commits you must emulate this with staging tables and swap, which is the same idea applied at the warehouse level (*DDIA, Kleppmann, Ch. 7* on transactions).

`../dataeng/enhanced-plan.md:L681` lists idempotency alongside ETL/ELT as a core pipeline-paradigm concept for this curriculum.

### Medallion architecture (Bronze / Silver / Gold)
The Medallion pattern refines data through three layers: **Bronze** holds raw ingested data as-is (schema close to source, append-only, audit of everything received); **Silver** holds cleaned, conformed, deduplicated data with enforced types and data contracts; **Gold** holds business-ready aggregates and dimensional marts consumed by BI and ML. Databricks documents this as a "multi-hop" design pattern whose goal is to incrementally improve data quality and structure as it flows between layers (`[Databricks Medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion)`).

Two practical rules for drawing the boundaries: Bronze is the replay buffer — if Silver or Gold logic changes, you must be able to regenerate them from Bronze alone, so Bronze retention is the hardest constraint. Silver is where data contracts go (`[dbt model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts)`); nothing reaches Gold without passing them.

### Backfill strategies
A **backfill** is a targeted rerun of historical partitions after a bug fix, a late-arriving source, or a new column. Three safe patterns:

1. **Partition-scoped overwrite.** Limit the run to a date range and overwrite only those partitions. Requires deterministic targets (see idempotency). Dagster exposes this directly via partitioned asset backfills; `../dataeng/enhanced-plan.md:L1565` contrasts `airflow dags backfill --start-date` with Dagster's partition-backfill UI.
2. **Shadow table, then swap.** Rebuild into a parallel table, validate, then atomically rename. Safe for schema changes. Iceberg's snapshot commits make this a metadata operation (`[Iceberg docs](https://iceberg.apache.org/docs/latest/)`).
3. **Forward fix.** Ship the corrected transformation and wait for the affected partitions to age out. Only acceptable when downstream consumers can tolerate stale history.

Never backfill by appending a "correction delta" on top of a corrupted partition — that destroys reproducibility and makes future point-in-time queries unreliable.

### DAG vs. pipeline mental models
A **pipeline** is a logical sequence of transformations from source to sink. A **DAG** (directed acyclic graph) is how an orchestrator represents that pipeline for scheduling: nodes are units of work, edges encode data or ordering dependencies, and acyclicity guarantees a topological execution order. Both Airflow and Dagster use DAGs, but they model nodes differently — Airflow nodes are tasks (imperative: "run this operator"), Dagster nodes are Software-Defined Assets (declarative: "this dataset should exist") (`[Airflow core concepts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html)`; `[Dagster concepts](https://docs.dagster.io/concepts)`). The asset model is easier to reason about for backfills because the asset and its partitions are first-class, not a side effect of running a task.

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_02_dlt_incremental` | Run the NYC taxi dlt pipeline twice; verify only new rows load on the second run | 60m | built in [../../phase_3_core_tools/04_dlt/](../../phase_3_core_tools/04_dlt/) |
| `lab_02_medallion_boundary` | Classify 10 real transformations into Bronze / Silver / Gold | 30m | see quiz Q7 |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Incremental pipeline silently drops updates | Cursor column not updated by source on row edit | Switch to CDC, or add a trigger that bumps the cursor | *DDIA, Kleppmann, Ch. 11* |
| Re-running a pipeline double-counts rows | Append-only load with no deterministic partition key | Move to partition-scoped overwrite or merge on a natural key | [Iceberg spec](https://iceberg.apache.org/spec/) |
| Backfill corrupts current-day partition | Backfill window overlaps today's incremental run | Pause the schedule, backfill, then resume | [Dagster partitioned assets](https://docs.dagster.io/concepts) |
| Silver table drifts from source schema | No contract enforced between Bronze and Silver | Enable dbt model contracts at the Silver boundary | [dbt contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] State the location of the T in ETL vs. ELT and give one reason ELT wins for a lakehouse
- [ ] Choose watermark, snapshot-diff, or CDC for three different source systems and justify each
- [ ] Write the two design rules that make a pipeline step idempotent
- [ ] Draw the Bronze/Silver/Gold boundaries for a taxi-trips pipeline and point to where data contracts live
- [ ] Describe a safe backfill procedure that does not corrupt current-day data
