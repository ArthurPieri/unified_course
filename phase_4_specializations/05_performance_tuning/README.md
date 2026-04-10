# Module 05: Performance Tuning — Trino, Spark, Iceberg (10h)

> Phase 4's penultimate specialization turns the lakehouse stack from Phase 3 into a *tuned* lakehouse stack. You learn a mental model for where query time goes, then walk through the dominant tuning levers in each engine: `EXPLAIN ANALYZE` for Trino plan reading, Adaptive Query Execution (AQE) and broadcast joins for Spark, and physical layout controls (file sizing, compaction, partition spec, snapshot expiration) for Iceberg. The lab deliberately builds a pathological dataset — 10 million rows in 10 000 tiny Parquet files — and asks you to diagnose, fix, and measure the difference.

## Learning goals
- Classify a slow query as IO-bound, CPU-bound, or shuffle-bound from its plan and runtime counters, citing the Trino and Spark tuning guides.
- Read a Trino `EXPLAIN ANALYZE` plan and identify the most expensive stage using CPU time, input rows, and input bytes.
- Enable and interpret Spark Adaptive Query Execution (AQE): coalescing shuffle partitions, dynamic join strategy switching, and skew join handling.
- Decide between a shuffle hash join and a broadcast hash join based on the smaller side's size relative to `spark.sql.autoBroadcastJoinThreshold`.
- Apply the Iceberg target file size range (128–512 MB), run `rewrite_data_files` to compact, and expire snapshots to reclaim storage.
- Detect partition skew from stage-level task durations and apply a mitigation (AQE skew handling, salting, repartition).
- Explain why columnar formats enable predicate pushdown and column pruning, citing the Parquet spec and the Trino/Spark engine behavior.

## Prerequisites
- `phase_3_core_tools/compose/full-stack/` stack running (MinIO, Trino, Spark, Iceberg, HMS).
- `phase_2_core_domain/06_lakehouse_bridge/` — you should be comfortable reading Parquet files and addressing MinIO over the S3 API.
- Python 3.11+ with `uv` installed for the lab data generator.

## Reading order
1. This README
2. `labs/lab_L4c_perf_tuning/README.md`
3. `quiz.md`

## Concepts

### A mental model for query time: IO, CPU, shuffle
Every distributed query's wall time breaks into three buckets: **IO** (bytes read from storage and deserialized), **CPU** (expression evaluation, aggregation, compression/decompression), and **shuffle** (redistributing rows across executors for joins and group-bys, which writes to local disk and crosses the network). The Spark tuning guide frames tuning as finding the bucket that dominates and attacking it — reduce bytes read (pruning, pushdown), reduce CPU (cache when reused, avoid UDFs), or reduce shuffle (broadcast, bucketing, partition pruning). Trino's tuning page echoes the same framing for its stage/operator model.
Ref: [Spark SQL performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html) · [Trino — Properties reference: tuning](https://trino.io/docs/current/admin/properties-general.html)

### EXPLAIN ANALYZE in Trino
`EXPLAIN ANALYZE` runs the query and returns the distributed plan annotated with actual wall time, CPU time, and input/output rows per stage and operator. The Trino docs state the command "executes a statement and shows the distributed execution plan of the statement along with the cost of each operation", which is what lets you attribute time to a specific `ScanFilterProject`, `Aggregate`, or `Join` node. You read top-down: find the stage with the highest CPU time or the largest `Input: ... rows, ... bytes` and ask whether its inputs could have been pruned upstream.
Ref: [Trino — EXPLAIN ANALYZE](https://trino.io/docs/current/sql/explain-analyze.html) · [Trino — EXPLAIN](https://trino.io/docs/current/sql/explain.html)

### Spark Adaptive Query Execution (AQE)
AQE rewrites the physical plan *at runtime* using statistics collected from completed shuffle stages. The Spark docs describe three optimizations: **coalescing shuffle partitions** (merging small post-shuffle partitions to avoid tiny tasks), **dynamically switching join strategies** (turning a sort-merge join into a broadcast join when one side turns out to be small), and **dynamically handling skew joins** (splitting oversized partitions into sub-partitions). AQE is controlled by `spark.sql.adaptive.enabled`, which is enabled by default since Spark 3.2.0.
Ref: [Spark SQL performance tuning — Adaptive Query Execution](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution)

### Broadcast joins
A broadcast hash join sends the entire smaller table to every executor and joins locally, skipping the shuffle of the larger side. Spark uses a broadcast join automatically when the smaller side is below `spark.sql.autoBroadcastJoinThreshold` (default 10 MB), or when you force it with the `BROADCAST` join hint. This is the single biggest win when a dimension table joins a fact table — no shuffle of the fact means no network transfer of the bulk of the data.
Ref: [Spark SQL performance tuning — Broadcast Hint for SQL Queries](https://spark.apache.org/docs/latest/sql-performance-tuning.html#broadcast-hint-for-sql-queries)

### Shuffle: why it hurts, how to minimize
Shuffle is expensive because it materializes partitioned output to local disk on every map task and then pulls it over the network on every reduce task — two disk passes plus network for every row. The Spark tuning guide recommends (1) reducing data before the shuffle via column pruning and predicate pushdown, (2) using broadcast joins to skip it entirely for small dimensions, (3) tuning `spark.sql.shuffle.partitions` (default 200) to match cluster size and data volume, and (4) using bucketing on join keys so co-partitioned inputs can skip the shuffle altogether.
Ref: [Spark tuning guide — Level of Parallelism](https://spark.apache.org/docs/latest/tuning.html#level-of-parallelism) · [Spark SQL performance tuning — Other configuration options](https://spark.apache.org/docs/latest/sql-performance-tuning.html#other-configuration-options)

### Iceberg file sizing and compaction
Iceberg's maintenance docs describe a `rewrite_data_files` action that compacts small files into the target size range, with `target-file-size-bytes` defaulting to 512 MB and controllable per-table. Too-small files cause per-file overhead (open, read footer, schedule task) to dominate IO time; too-large files reduce parallelism. The Spark procedure `CALL catalog.system.rewrite_data_files(table => 'db.t')` (and the Trino equivalent) rewrites eligible files in place, producing a new snapshot. It is the single most common tuning action on a lakehouse that has been ingesting streaming writes or micro-batches.
Ref: [Iceberg — Maintenance: Compact data files](https://iceberg.apache.org/docs/latest/maintenance/#compact-data-files) · [Iceberg — Spark procedures: rewrite_data_files](https://iceberg.apache.org/docs/latest/spark-procedures/#rewrite_data_files)

### Expire snapshots
Iceberg retains old snapshots so you can time-travel; snapshots that are no longer needed must be explicitly expired, otherwise their data files cannot be deleted. The maintenance doc states that expiring snapshots removes metadata files and the underlying data files no longer referenced by any retained snapshot. Run `expire_snapshots` on a schedule (Spark procedure or Trino call), usually retaining N days or K most-recent snapshots.
Ref: [Iceberg — Maintenance: Expire Snapshots](https://iceberg.apache.org/docs/latest/maintenance/#expire-snapshots) · [Iceberg — Spark procedures: expire_snapshots](https://iceberg.apache.org/docs/latest/spark-procedures/#expire_snapshots)

### Partition spec and hidden partitioning
Iceberg's partition spec is declared on the table and stored in metadata, so writers and readers use the same transform (`days(ts)`, `bucket(16, user_id)`, etc.) without the user hand-crafting partition columns. The Iceberg docs describe this as "hidden partitioning": queries filter on the logical column and Iceberg automatically applies the transform to prune files. A good partition spec maps the most selective filter in typical queries to a transform that yields partitions large enough to hold target-sized files.
Ref: [Iceberg — Partitioning](https://iceberg.apache.org/docs/latest/partitioning/) · [Iceberg — Table spec: partition spec](https://iceberg.apache.org/spec/#partition-specs)

### Partition skew detection
Skew shows up as a stage where most tasks finish in seconds while one or two run for minutes. Spark's AQE skew handling splits these oversized partitions into sub-partitions and replicates the join side, controlled by `spark.sql.adaptive.skewJoin.enabled` (default true with AQE on). Without AQE, the fallback mitigation is salting: add a random prefix to skewed keys to distribute them across tasks. Detect skew in the Spark UI stage view (task duration histogram) or in Trino's query UI (per-stage task time distribution).
Ref: [Spark SQL performance tuning — Optimizing Skew Join](https://spark.apache.org/docs/latest/sql-performance-tuning.html#optimizing-skew-join)

### Predicate pushdown and column pruning
Columnar formats win on analytics because the engine can (1) read only the columns the query references (**column pruning**) and (2) skip whole row groups whose min/max statistics rule out the predicate (**predicate pushdown**). The Parquet spec stores per-column statistics in the row group metadata precisely so readers can do this. Trino and Spark both push supported predicates down to the Parquet reader; filters on partition columns additionally prune entire files before opening them, which is why a good partition spec matters.
Ref: [Apache Parquet format specification](https://parquet.apache.org/docs/file-format/) · [Trino — Hive connector: performance tuning](https://trino.io/docs/current/connector/hive.html#performance)

### When to cache in Spark — and when it hurts
`df.cache()` materializes a DataFrame into executor memory (spilling to disk if configured) so subsequent actions reuse it. Cache helps when the same DataFrame is scanned multiple times *and* the inputs are expensive (wide scans, complex upstream transformations). It hurts when (1) the DataFrame is used once — cache adds a write, (2) it doesn't fit in memory and spills, making it slower than reading Parquet again, or (3) it is cached before an operation that would otherwise push filters into the Parquet reader, defeating predicate pushdown. The Spark tuning guide is explicit that caching is a targeted optimization, not a default.
Ref: [Spark SQL performance tuning — Caching Data In Memory](https://spark.apache.org/docs/latest/sql-performance-tuning.html#caching-data-in-memory)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L4c_perf_tuning` | Diagnose a slow Trino/Spark query on 10 000 tiny Parquet files, compact with Iceberg `rewrite_data_files`, measure the speedup | 120–180m | [labs/lab_L4c_perf_tuning/](labs/lab_L4c_perf_tuning/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Query scans every file despite a date filter | No partition pruning — filter column is not a partition transform | Add `PARTITIONED BY (days(ts))` or rewrite with the right transform | [Iceberg partitioning](https://iceberg.apache.org/docs/latest/partitioning/) |
| 10 000+ tasks for a small-bytes read | File-per-task parallelism on tiny files | `CALL system.rewrite_data_files` to compact to 128–512 MB files | [Iceberg maintenance](https://iceberg.apache.org/docs/latest/maintenance/#compact-data-files) |
| One Spark task runs 10× longer than the rest | Partition skew on a join key | Enable AQE skew handling or salt the key | [Spark — Optimizing Skew Join](https://spark.apache.org/docs/latest/sql-performance-tuning.html#optimizing-skew-join) |
| Join does a full shuffle on a 5 MB dimension | Broadcast threshold not tripped or AQE disabled | Use `BROADCAST` hint or raise `autoBroadcastJoinThreshold` | [Spark — Broadcast Hint](https://spark.apache.org/docs/latest/sql-performance-tuning.html#broadcast-hint-for-sql-queries) |
| `rewrite_data_files` runs but disk usage does not drop | Old snapshots still reference rewritten files | Run `expire_snapshots` | [Iceberg — Expire Snapshots](https://iceberg.apache.org/docs/latest/maintenance/#expire-snapshots) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Read a Trino `EXPLAIN ANALYZE` plan and name the most expensive operator.
- [ ] Enable AQE in a Spark session and explain what its three core optimizations do.
- [ ] Decide whether a given join should be a broadcast join based on the small side's size.
- [ ] Run `rewrite_data_files` and `expire_snapshots` on an Iceberg table and show the before/after file count and storage footprint.
- [ ] Detect partition skew from the Spark UI and apply AQE skew handling or salting.
- [ ] Justify, in one sentence, why column pruning and predicate pushdown make columnar formats faster for analytics.
