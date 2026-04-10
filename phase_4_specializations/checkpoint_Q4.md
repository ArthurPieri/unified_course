# Checkpoint — Phase 4: Specializations (20 MCQ)

Covers modules 01–06: CDC/Debezium, Kafka hands-on, semi-structured data, security & governance, performance tuning, observability.

Answer key with primary-source citations at the bottom under `## Answers`.

---

**Q1.** What does Debezium's Change Data Capture architecture rely on at the source database?

A. Periodic `SELECT * FROM t` polling.
B. The database's write-ahead / transaction log, read through a connector.
C. Triggers inserted on every monitored table.
D. A file export from a nightly `pg_dump`.

---

**Q2.** In Debezium, which record fields describe the row state before and after a change event?

A. `old_row` / `new_row`
B. `before` / `after`
C. `source` / `target`
D. `pre` / `post`

---

**Q3.** A Kafka producer must guarantee that a burst of retries does not produce duplicate messages on a single partition. Which producer setting enables this?

A. `acks=0`
B. `enable.idempotence=true`
C. `compression.type=zstd`
D. `linger.ms=1000`

---

**Q4.** What is the effect of `acks=all` on a Kafka producer, per the Kafka producer docs?

A. The leader writes locally and returns immediately, ignoring replicas.
B. The producer waits for the leader and all in-sync replicas to acknowledge the write before considering it successful.
C. The producer sends asynchronously without acknowledgement.
D. The producer fans out to every broker including non-replicas.

---

**Q5.** A Kafka topic has 12 partitions and a consumer group with 4 consumers. How many partitions does each consumer read, assuming the default assignor and a stable group?

A. 12 (each consumer reads all partitions)
B. 3 (partitions are divided across consumers)
C. 1 (only one consumer is active)
D. 0 (consumers must be equal in count to partitions)

---

**Q6.** Which JSON feature makes flattening to a relational schema non-trivial and motivates semi-structured handling in analytics engines?

A. UTF-8 encoding.
B. Nested arrays and objects with variable depth and optional fields.
C. Integer precision.
D. Whitespace sensitivity.

---

**Q7.** In Trino, which data type is used to store JSON payloads as opaque values, and which function extracts a nested field by JSONPath?

A. `TEXT` / `REGEXP_EXTRACT`
B. `JSON` / `json_extract` (or `json_query`) with a JSONPath expression
C. `VARBINARY` / `from_utf8`
D. `MAP<K,V>` / `element_at`

---

**Q8.** Which Iceberg feature lets you evolve a table's schema without rewriting existing data files, as stated in the Iceberg docs?

A. Manifest vacuum.
B. Schema evolution via unique column IDs tracked in metadata.
C. Snapshot rollback.
D. Table format v1 compatibility mode.

---

**Q9.** Column-level security in Trino is typically implemented by which mechanism, according to the Trino security docs?

A. Editing the Parquet file's column chunks to zero out values.
B. A system access control plugin or connector-level rules that apply row filters and column masks.
C. Creating a separate table per role.
D. Disabling the column in the catalog XML.

---

**Q10.** Which principle is central to governance frameworks like GDPR's purpose limitation and data-minimization requirements?

A. Collect as much data as possible for future analytics.
B. Collect and retain only the data necessary for a declared, lawful purpose.
C. Store PII only in object storage.
D. Encrypt everything at rest and consider governance done.

---

**Q11.** In Trino, which statement is the correct tool to attribute wall time to specific plan operators by running the query and measuring it?

A. `EXPLAIN (TYPE LOGICAL)`
B. `EXPLAIN ANALYZE`
C. `SHOW STATS`
D. `DESCRIBE`

---

**Q12.** Spark Adaptive Query Execution (AQE) provides which three runtime optimizations?

A. Vectorization, whole-stage codegen, Tungsten.
B. Coalescing shuffle partitions, dynamically switching join strategies, dynamic skew-join handling.
C. Predicate pushdown, partition pruning, bloom filtering.
D. Broadcast join, sort-merge join, hash join.

---

**Q13.** What is the Iceberg default value for `write.target-file-size-bytes`?

A. 1 MB
B. 64 MB
C. 512 MB
D. 5 GB

---

**Q14.** You ran `CALL iceberg.system.rewrite_data_files(...)` to compact tiny files, and total object-store usage did not drop. What is the correct next step?

A. Run `expire_snapshots` so snapshots that still reference the old files are dropped and the old files can be removed.
B. Delete files manually with `mc rm`.
C. Re-create the table.
D. Rebuild the Hive metastore.

---

**Q15.** Spark decides to use a broadcast hash join when the smaller side is under which configurable threshold?

A. `spark.sql.autoBroadcastJoinThreshold` (default ~10 MB).
B. `spark.sql.shuffle.partitions`.
C. `spark.executor.memory`.
D. `spark.sql.adaptive.enabled`.

---

**Q16.** Which statement best describes the Prometheus scrape model?

A. Clients push events over gRPC.
B. Prometheus pulls metrics from targets over HTTP on a configurable interval; a scrape failure is itself a signal.
C. Targets stream metrics over a persistent websocket.
D. Prometheus reads metrics from shared log files.

---

**Q17.** Which Prometheus metric type is the right choice for a value that can go up *or* down, such as a queue depth or a memory usage figure?

A. Counter
B. Gauge
C. Histogram
D. Summary

---

**Q18.** Per Google's SRE book Chapter 6, alerts should primarily fire on:

A. Any cause (CPU hot, pod restart).
B. Symptoms users experience (latency, errors, freshness), backed by SLIs/SLOs.
C. Every ERROR log line.
D. Capacity forecasts only.

---

**Q19.** Which of the following is a *data-pipeline-specific* signal that generic service monitoring typically misses?

A. HTTP request rate on the Grafana UI.
B. The freshness (staleness) of the target table relative to the source event time.
C. TCP retransmit count on the worker.
D. JVM GC pause duration on the orchestrator.

---

**Q20.** Which four quantities does Google SRE book Chapter 6 list as the "four golden signals" for monitoring user-facing systems?

A. CPU, memory, disk, network.
B. Latency, traffic, errors, saturation.
C. Rate, errors, duration, uptime.
D. Utilization, saturation, errors, queue depth.

---

## Answers

1. **B** — Debezium reads the DB transaction log via source-specific connectors. ([Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html))
2. **B** — `before` / `after` are the canonical change-event fields in Debezium envelopes. ([Debezium — Data change events](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-create-events))
3. **B** — `enable.idempotence=true` deduplicates retries on a partition. ([Kafka producer configs](https://kafka.apache.org/documentation/#producerconfigs_enable.idempotence))
4. **B** — `acks=all` waits for leader + all in-sync replicas. ([Kafka producer configs — acks](https://kafka.apache.org/documentation/#producerconfigs_acks))
5. **B** — 12 partitions ÷ 4 consumers = 3 each, under the default assignor. ([Kafka — Consumer groups](https://kafka.apache.org/documentation/#intro_consumers))
6. **B** — Nested arrays/objects with variable depth make relational flattening non-trivial. ([JSON — RFC 8259](https://datatracker.ietf.org/doc/html/rfc8259))
7. **B** — Trino has a native `JSON` type and `json_extract` / `json_query` functions. ([Trino — JSON functions](https://trino.io/docs/current/functions/json.html))
8. **B** — Iceberg tracks unique column IDs; schema evolution is a first-class feature. ([Iceberg — Schema evolution](https://iceberg.apache.org/docs/latest/evolution/))
9. **B** — Access control plugins and connector rules enforce column/row security in Trino. ([Trino — Security](https://trino.io/docs/current/security.html))
10. **B** — Purpose limitation + data minimization: only what is needed for a declared purpose. ([GDPR Art. 5](https://gdpr-info.eu/art-5-gdpr/))
11. **B** — `EXPLAIN ANALYZE` runs the query and reports per-operator cost. ([Trino — EXPLAIN ANALYZE](https://trino.io/docs/current/sql/explain-analyze.html))
12. **B** — AQE: coalesce partitions, dynamic join strategy, dynamic skew handling. ([Spark — AQE](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution))
13. **C** — 512 MB default. ([Iceberg — Configuration](https://iceberg.apache.org/docs/latest/configuration/))
14. **A** — Old snapshots pin old files; expire them to reclaim storage. ([Iceberg — Expire Snapshots](https://iceberg.apache.org/docs/latest/maintenance/#expire-snapshots))
15. **A** — `spark.sql.autoBroadcastJoinThreshold` governs automatic broadcast. ([Spark — Broadcast Hint](https://spark.apache.org/docs/latest/sql-performance-tuning.html#broadcast-hint-for-sql-queries))
16. **B** — Pull model; scrape failures are themselves observable. ([Prometheus — Overview](https://prometheus.io/docs/introduction/overview/))
17. **B** — Gauge for values that go up or down. ([Prometheus — Metric types](https://prometheus.io/docs/concepts/metric_types/))
18. **B** — Symptoms, not causes. ([SRE Book Ch. 6 — Symptoms vs. Causes](https://sre.google/sre-book/monitoring-distributed-systems/#symptoms-versus-causes))
19. **B** — Table freshness vs. source event time is a pipeline SLI generic monitoring misses. ([Dagster — Freshness checks](https://docs.dagster.io/concepts/assets/asset-checks))
20. **B** — Latency, traffic, errors, saturation. ([SRE Book Ch. 6 — The four golden signals](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals))
