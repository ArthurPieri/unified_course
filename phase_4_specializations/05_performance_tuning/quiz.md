# Quiz — Module 05: Performance Tuning

10 multiple-choice questions. Answer key at the bottom.

---

**Q1.** A Trino query over a lakehouse table runs for 4 minutes. You want to attribute wall time to specific operators. Which single statement is the right tool?

A. `EXPLAIN (TYPE LOGICAL) SELECT ...`
B. `EXPLAIN ANALYZE SELECT ...`
C. `SHOW STATS FOR t`
D. `DESCRIBE t`

---

**Q2.** Which three runtime optimizations does Spark Adaptive Query Execution (AQE) provide, as listed in the Spark SQL performance tuning docs?

A. Vectorized reads, whole-stage codegen, Tungsten memory.
B. Coalescing post-shuffle partitions, dynamically switching join strategies, dynamic skew-join handling.
C. Predicate pushdown, column pruning, runtime filtering.
D. Broadcast join, shuffle hash join, sort-merge join.

---

**Q3.** A Spark join pairs a 2 GB fact with a 5 MB dimension. You want to skip shuffling the fact. Which approach does the Spark docs recommend?

A. Repartition both sides by the join key.
B. Use a broadcast hash join (either automatically via `spark.sql.autoBroadcastJoinThreshold` or explicitly with the `BROADCAST` hint).
C. Disable AQE.
D. Increase `spark.sql.shuffle.partitions` to 2000.

---

**Q4.** Which Iceberg procedure compacts small files into the configured target size?

A. `CALL catalog.system.rewrite_data_files(table => 'db.t')`
B. `CALL catalog.system.vacuum(table => 'db.t')`
C. `OPTIMIZE FULL db.t`
D. `ANALYZE TABLE db.t`

---

**Q5.** The Iceberg `write.target-file-size-bytes` default is closest to which value?

A. 1 MB
B. 64 MB
C. 512 MB
D. 5 GB

---

**Q6.** Why is compacting tiny Parquet files a big win for a cold-cache scan?

A. It reduces disk space by deduplicating rows.
B. It replaces row-oriented pages with columnar pages.
C. It eliminates per-file open/plan/read-footer overhead that dominates IO time on thousands of small files.
D. It recomputes column statistics, which speeds up the CPU.

---

**Q7.** In a Spark stage, 199 tasks finish in 3 s and one task runs for 4 minutes. Which diagnosis fits, and what is the AQE-based mitigation?

A. GC pressure; add more executor memory.
B. Partition skew on a join key; enable `spark.sql.adaptive.skewJoin.enabled` (on by default with AQE) or salt the key.
C. Serialization overhead; switch to Kryo.
D. Slow disk on one executor; restart the worker.

---

**Q8.** Which statement about predicate pushdown and column pruning in Parquet is correct?

A. Pushdown uses column statistics in row-group metadata to skip groups, and pruning reads only referenced columns.
B. Pushdown rewrites the Parquet file in place to remove non-matching rows.
C. Pruning and pushdown require a proprietary index file next to each Parquet file.
D. Pruning applies only to partition columns, never to data columns.

---

**Q9.** You ran `rewrite_data_files` but object storage usage did not drop. What is the Iceberg-correct next step?

A. Delete files manually with `mc rm`.
B. Call `expire_snapshots` to drop snapshots that still reference the old files so the data files can be removed.
C. Run `VACUUM FULL`.
D. Rebuild the table from scratch.

---

**Q10.** Per the Spark SQL performance tuning docs, when does caching a DataFrame *hurt* more than help?

A. When the DataFrame is reused across many actions and fits in memory.
B. When the cached DataFrame fits comfortably and is computed from expensive upstream transforms.
C. When the DataFrame is used once, or when caching sits between a reader and a predicate that could have been pushed into the Parquet scan.
D. Never — caching always helps.

---

## Answer key

1. **B** — `EXPLAIN ANALYZE` runs the query and reports distributed plan cost per operator. ([Trino EXPLAIN ANALYZE](https://trino.io/docs/current/sql/explain-analyze.html))
2. **B** — AQE: coalesce shuffle partitions, dynamic join strategy, dynamic skew-join handling. ([Spark — AQE](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution))
3. **B** — Broadcast hash join avoids shuffling the large side. ([Spark — Broadcast Hint](https://spark.apache.org/docs/latest/sql-performance-tuning.html#broadcast-hint-for-sql-queries))
4. **A** — `rewrite_data_files` is the Iceberg Spark procedure to compact. ([Iceberg — Spark procedures](https://iceberg.apache.org/docs/latest/spark-procedures/#rewrite_data_files))
5. **C** — 512 MB default for `write.target-file-size-bytes`. ([Iceberg — Configuration](https://iceberg.apache.org/docs/latest/configuration/))
6. **C** — Per-file overhead (open, read footer, schedule) dominates for many tiny files. ([Iceberg — Maintenance: compact](https://iceberg.apache.org/docs/latest/maintenance/#compact-data-files))
7. **B** — Classic skew signature; AQE skew-join splits oversized partitions; salting is the non-AQE fallback. ([Spark — Optimizing Skew Join](https://spark.apache.org/docs/latest/sql-performance-tuning.html#optimizing-skew-join))
8. **A** — Row-group min/max statistics power pushdown; pruning reads only referenced columns. ([Parquet format](https://parquet.apache.org/docs/file-format/))
9. **B** — Data files remain on disk as long as any snapshot references them; expire snapshots first. ([Iceberg — Expire Snapshots](https://iceberg.apache.org/docs/latest/maintenance/#expire-snapshots))
10. **C** — Cache is a targeted optimization, not a default; one-shot use or blocking pushdown makes it a net loss. ([Spark — Caching Data In Memory](https://spark.apache.org/docs/latest/sql-performance-tuning.html#caching-data-in-memory))
