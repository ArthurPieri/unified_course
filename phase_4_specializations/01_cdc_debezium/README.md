# Module 01: Change Data Capture with Debezium (8h)

> CDC is the bridge between OLTP truth and the lakehouse. Query-based polling can miss deletes and lies about intermediate states; log-based CDC reads the database's own write-ahead log and reconstructs every row mutation in order. Debezium is the open-source implementation that plugs Postgres, MySQL, SQL Server, MongoDB, and Oracle into Kafka.

## Learning goals
- Explain why log-based CDC strictly dominates query-based CDC for correctness
- Describe Debezium's source-connector → Kafka Connect → topic → sink pipeline
- Configure Postgres logical replication (`wal_level`, slots, publications) for a Debezium source
- Distinguish the snapshot and streaming phases of a Debezium connector
- Apply the MERGE INTO pattern to land CDC events in an Apache Iceberg table
- Reason about tombstones, schema changes, and exactly-once delivery in a CDC pipeline

## Prerequisites
- [../../phase_1_foundations/05_sql_postgres/](../../phase_1_foundations/05_sql_postgres/) — Postgres basics, WAL concept
- [../../phase_3_core_tools/01_minio_iceberg_hms/](../../phase_3_core_tools/01_minio_iceberg_hms/) — Iceberg tables on MinIO
- [../../phase_3_core_tools/02_trino/](../../phase_3_core_tools/02_trino/) — running Trino with the Iceberg catalog
- [../02_kafka_hands_on/](../02_kafka_hands_on/) (concurrent is fine) — topics, partitions, consumer groups

## Reading order
1. This README
2. [labs/lab_L4a_cdc_pipeline/README.md](labs/lab_L4a_cdc_pipeline/README.md)
3. [quiz.md](quiz.md)

## Concepts

### Query-based vs log-based CDC
Query-based CDC repeatedly runs `SELECT * WHERE updated_at > :high_watermark`. It needs every table to carry a trustworthy `updated_at`, it cannot see deletes (the row is simply gone), and it loses intermediate updates that happened between two polls. Log-based CDC instead reads the database's transaction log — the same log the database itself uses to crash-recover and to feed replicas — so every insert, update, and delete is captured in commit order with before/after images. Debezium is built entirely around this principle, and its architecture page states the design goal explicitly: stream row-level changes "as they occur" from the source database's log.
Ref: [Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html) · *Designing Data-Intensive Applications*, Kleppmann, Ch. 11

### Debezium topology: source connector → Kafka Connect → Kafka → sink
A Debezium source connector runs inside **Kafka Connect**, a worker process that manages connector lifecycle, offset storage, and REST configuration. The source connector tails the database log, converts each change into a structured event with a `before`, `after`, `source`, and `op` field, and publishes to a Kafka topic — typically one topic per captured table. A **sink connector** (also Kafka Connect) or any consumer (Spark, Trino, Flink, a Python script) reads those topics and writes to the analytical target. Single Message Transforms (SMTs) can mutate events in-flight — drop PII columns, rename fields, unwrap the envelope, or route between topics — without a separate stream processor.
Ref: [Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html) · [Kafka Connect — transforms](https://kafka.apache.org/documentation/#connect_transforms)

### Postgres logical replication: `wal_level`, slots, publications
The Postgres connector reads from a **logical replication slot**. To enable this you must set `wal_level = logical` in `postgresql.conf` (a server restart is required) and grant the connector's role `REPLICATION` plus `SELECT` on the captured tables. Debezium then creates a replication slot that holds WAL segments until the connector has consumed them — an abandoned slot is how you fill a production disk. A **publication** is the Postgres object that declares which tables stream through logical decoding; Debezium can auto-create one or consume an existing publication. The connector documentation lists these as hard prerequisites.
Ref: [Debezium PostgreSQL connector — server configuration](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-server-configuration) · [Debezium PostgreSQL connector — replication slots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-replication-slots)

### Snapshot phase and streaming phase
When a connector starts against a table it has never seen, it runs a **consistent snapshot**: it takes a repeatable-read view, emits a synthetic `r` (read) event for every existing row, and records the WAL position where the snapshot began. Once the snapshot finishes it switches to the **streaming phase** and replays every change from that recorded position forward. The two phases together give you "load and follow" semantics from a single connector config. Debezium also supports incremental snapshots for re-syncing individual tables without stopping the stream.
Ref: [Debezium PostgreSQL connector — snapshots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-snapshots)

### Schema changes and DDL
When the source table's schema evolves, Debezium emits a new change event whose embedded schema reflects the new columns. The PostgreSQL connector publishes schema-change messages to a dedicated schema-history topic so the connector can recover its view of DDL across restarts. Downstream consumers that use a schema registry (Avro, Protobuf, JSON Schema) get forward/backward-compatible evolution for free; consumers that parse raw JSON must handle new or missing fields themselves.
Ref: [Debezium PostgreSQL connector — schema history](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-schema-history-topic)

### Tombstones and deletes
A Debezium delete event carries `op=d`, the `before` image of the deleted row, and a `null` `after`. Immediately after the delete event, the connector emits a **tombstone** — a message with the same key and a `null` value — so Kafka's log compaction knows to eventually drop that key entirely. Sinks that materialize current-state tables must treat tombstones as "remove this row"; sinks that want an append-only audit log should disable tombstones (`tombstones.on.delete=false`) and keep every event forever.
Ref: [Debezium PostgreSQL connector — delete events and tombstones](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-delete-events)

### Landing CDC into Iceberg with MERGE INTO
Iceberg supports row-level operations via `MERGE INTO`, which is the clean way to apply a batch of CDC events to a current-state table. Treat the Kafka topic as a micro-batch source: read a window of events, group by primary key keeping the latest `op` per key, then run `MERGE INTO target t USING changes c ON t.id = c.id WHEN MATCHED AND c.op = 'd' THEN DELETE WHEN MATCHED THEN UPDATE SET ... WHEN NOT MATCHED AND c.op <> 'd' THEN INSERT ...`. Because Iceberg writes snapshots, every merge produces a new snapshot you can time-travel to — the audit history is free.
Ref: [Iceberg MERGE INTO](https://iceberg.apache.org/docs/latest/spark-writes/#merge-into) · [Iceberg — row-level deletes](https://iceberg.apache.org/spec/#row-level-deletes)

### Exactly-once delivery in a CDC pipeline
Kafka itself offers exactly-once semantics via idempotent producers and transactions, and Debezium connectors participate in Kafka Connect's exactly-once source support introduced in Connect 3.3. End-to-end exactly-once also requires the sink to be transactional or idempotent — for Iceberg this means making the `MERGE` keyed on the primary key so re-applying the same batch is a no-op. In practice most teams aim for "at-least-once plus idempotent sink" because it is dramatically simpler to operate.
Ref: [Kafka Connect — exactly-once source support (KIP-618)](https://kafka.apache.org/documentation/#connect_exactlyoncesource) · *Designing Data-Intensive Applications*, Kleppmann, Ch. 11

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L4a_cdc_pipeline` | Capture Postgres changes via Debezium → Kafka → Iceberg using `MERGE INTO` in Trino | 120m | [labs/lab_L4a_cdc_pipeline/](labs/lab_L4a_cdc_pipeline/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Connector starts, then no events appear | `wal_level` is still `replica` | Set `wal_level=logical` in `postgresql.conf` and restart the server | [PG connector — server config](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-server-configuration) |
| Postgres disk fills up | Orphaned replication slot retains WAL | `SELECT pg_drop_replication_slot('<slot>')` after deleting the connector | [PG connector — replication slots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-replication-slots) |
| Deletes do not propagate to Iceberg | Sink ignores tombstones | Handle `op=d` explicitly in MERGE; do not filter null-value records | [PG connector — delete events](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-delete-events) |
| Duplicate rows after connector restart | At-least-once + non-idempotent sink | Key MERGE on the primary key; upstream, enable Connect exactly-once source | [Kafka Connect — exactly-once](https://kafka.apache.org/documentation/#connect_exactlyoncesource) |
| Schema drift breaks consumers | Raw JSON consumers not tolerant to new columns | Use a schema registry or enable an Unwrap SMT with explicit field projection | [Kafka Connect — transforms](https://kafka.apache.org/documentation/#connect_transforms) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Name two concrete failure modes of query-based CDC that log-based CDC fixes
- [ ] Configure `wal_level`, a role with `REPLICATION`, and a publication for a Debezium Postgres source
- [ ] Register a Debezium PostgreSQL connector via the Kafka Connect REST API
- [ ] Write a `MERGE INTO` statement that applies inserts, updates, and deletes from a CDC staging table
- [ ] Explain what a tombstone is and why log compaction depends on it
