# References — Module 05: Performance Tuning

## Primary docs — Trino
- [Trino — EXPLAIN ANALYZE](https://trino.io/docs/current/sql/explain-analyze.html) — runs the statement and reports distributed plan with wall-clock and CPU cost per operator.
- [Trino — EXPLAIN](https://trino.io/docs/current/sql/explain.html) — logical and distributed plan without execution.
- [Trino — Hive connector: performance](https://trino.io/docs/current/connector/hive.html#performance) — predicate pushdown, partition pruning, columnar reader behavior.
- [Trino — General properties (tuning)](https://trino.io/docs/current/admin/properties-general.html) — memory, task, and query tuning knobs.
- [Trino — Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) — `ALTER TABLE ... EXECUTE optimize`, partition spec, metadata tables.

## Primary docs — Spark
- [Spark SQL performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html) — AQE, broadcast join, shuffle partitions, caching, skew join.
- [Spark tuning guide](https://spark.apache.org/docs/latest/tuning.html) — memory, serialization, level of parallelism, data locality.
- [Spark — Adaptive Query Execution](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution) — coalescing partitions, dynamic join strategy, skew join; default-on in 3.2+.
- [Spark — Broadcast Hint for SQL Queries](https://spark.apache.org/docs/latest/sql-performance-tuning.html#broadcast-hint-for-sql-queries) — `BROADCAST` hint and `autoBroadcastJoinThreshold`.
- [Spark — Caching Data In Memory](https://spark.apache.org/docs/latest/sql-performance-tuning.html#caching-data-in-memory) — when cache helps and when it hurts.

## Primary docs — Iceberg
- [Iceberg — Maintenance](https://iceberg.apache.org/docs/latest/maintenance/) — compact data files, expire snapshots, remove orphan files, rewrite manifests.
- [Iceberg — Spark procedures](https://iceberg.apache.org/docs/latest/spark-procedures/) — `rewrite_data_files`, `expire_snapshots`, `rewrite_manifests`.
- [Iceberg — Partitioning](https://iceberg.apache.org/docs/latest/partitioning/) — hidden partitioning, partition transforms (`days`, `bucket`, `truncate`).
- [Iceberg — Table spec: partition specs](https://iceberg.apache.org/spec/#partition-specs) — formal spec of partition transforms and evolution.
- [Iceberg — Configuration](https://iceberg.apache.org/docs/latest/configuration/) — `write.target-file-size-bytes` default (512 MB) and related write knobs.

## Primary docs — formats
- [Apache Parquet — file format specification](https://parquet.apache.org/docs/file-format/) — row groups, column chunks, page statistics, predicate pushdown enablers.

## Sibling sources
- `../../references/glossary.md:L49-L50` — Shuffle entry citing Spark performance tuning.
- `../../references/sibling_sources.md` — Phase 4 · 05 mapping.

## Books
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 3 — column-oriented storage, compression, and vectorized execution motivation.
- *Fundamentals of Data Engineering*, Reis & Housley — query optimization and physical data layout chapter.
