# References — 01_cdc_debezium

## Primary docs (debezium.io)
- [Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html) — source connector, Connect, topics, sink, SMTs
- [Debezium PostgreSQL connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html) — full connector reference
- [PG connector — server configuration](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-server-configuration) — `wal_level=logical`, roles, publications
- [PG connector — replication slots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-replication-slots) — slot lifecycle, disk-fill hazard
- [PG connector — snapshots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-snapshots) — initial and incremental snapshot modes
- [PG connector — schema history topic](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-schema-history-topic) — DDL tracking
- [PG connector — delete events and tombstones](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-delete-events)
- [Debezium transformations — Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html) — outbox pattern
- [Debezium transformations — New Record State Extraction](https://debezium.io/documentation/reference/stable/transformations/event-flattening.html) — unwrap SMT

## Primary docs (kafka.apache.org)
- [Kafka Connect overview](https://kafka.apache.org/documentation/#connect) — workers, connectors, tasks, offsets
- [Kafka Connect — transforms (SMTs)](https://kafka.apache.org/documentation/#connect_transforms) — in-flight event mutation
- [Kafka Connect — exactly-once source support](https://kafka.apache.org/documentation/#connect_exactlyoncesource) — KIP-618 semantics
- [Kafka Connect REST API](https://kafka.apache.org/documentation/#connect_rest) — `POST /connectors`, `GET /connectors/<name>/status`

## Primary docs (iceberg.apache.org)
- [Iceberg — MERGE INTO (Spark)](https://iceberg.apache.org/docs/latest/spark-writes/#merge-into) — upsert pattern for CDC sinks
- [Iceberg spec — row-level deletes](https://iceberg.apache.org/spec/#row-level-deletes) — equality and position delete files
- [Iceberg — time travel](https://iceberg.apache.org/docs/latest/spark-queries/#time-travel) — `FOR VERSION AS OF <snapshot>`

## Primary docs (postgresql.org)
- [PostgreSQL — Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html) — publications and subscriptions
- [PostgreSQL — `wal_level`](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-LEVEL) — required setting for logical decoding
- [PostgreSQL — `CREATE PUBLICATION`](https://www.postgresql.org/docs/current/sql-createpublication.html)

## Books
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — "Stream Processing" (change-capture, log compaction, exactly-once)

## Managed-service parallel
- [Amazon MSK — What is Amazon MSK?](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html) — MSK + MSK Connect with Debezium as a managed parallel to the OSS stack in this module.
