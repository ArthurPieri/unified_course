# Quiz — 01_cdc_debezium

Ten multiple-choice questions. Answers at the bottom.

---

**1.** Which concrete failure mode of query-based CDC does log-based CDC fix?

A. It cannot join two tables
B. It cannot observe row deletes or intermediate updates between polls
C. It requires a primary key
D. It cannot run on replicas

**2.** To run a Debezium PostgreSQL source connector, `postgresql.conf` must set:

A. `wal_level = minimal`
B. `wal_level = replica`
C. `wal_level = logical`
D. `archive_mode = on`

**3.** A Debezium replication slot that is never advanced will:

A. Silently be garbage-collected after 24h
B. Hold WAL segments on the Postgres server until disk fills
C. Auto-delete when the connector task stops
D. Be replaced by the next slot Debezium creates

**4.** In a Debezium change event, what does `op = 'd'` with `after = null` indicate?

A. A schema change
B. A snapshot read
C. A delete, and the next record on that key is typically a tombstone
D. A heartbeat

**5.** Which Kafka feature relies on tombstone records?

A. Exactly-once producer
B. Log compaction, to eventually drop keys marked as deleted
C. Consumer group rebalance
D. ISR shrink

**6.** During a Debezium initial snapshot, the connector emits events with `op`:

A. `c` (create) for every row
B. `r` (read) for every existing row, then switches to `c/u/d` in streaming phase
C. `s` (snapshot) only
D. None — snapshots are silent

**7.** The cleanest way to land Debezium events into an Iceberg current-state table is:

A. `INSERT OVERWRITE` the whole table every batch
B. `MERGE INTO target USING changes ON PK WHEN MATCHED ... WHEN NOT MATCHED ...`
C. `DELETE FROM target; INSERT ...`
D. `COPY` from a CSV

**8.** A Single Message Transform (SMT) in Kafka Connect runs:

A. As a separate Spark job
B. Inline inside the connector task, on each record, before it lands in Kafka (source) or sink
C. Only on the sink side
D. Only for Avro payloads

**9.** Why is end-to-end exactly-once CDC hard in practice?

A. Kafka cannot deliver exactly-once
B. The source connector must participate in transactions AND the sink must be transactional or idempotent — both ends have to cooperate
C. Debezium does not support it at all
D. It requires a proprietary registry

**10.** Where does Debezium record DDL events so a connector can recover its table schema across restarts?

A. In the snapshot
B. In a dedicated schema-history topic
C. In the connector's worker config file
D. In the Postgres `pg_catalog`

---

## Answer key

1. **B** — Polling misses intermediate states and cannot see a row that was deleted between polls. [Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html)
2. **C** — Logical decoding requires `wal_level = logical`; `replica` is insufficient. [PG connector — server config](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-server-configuration)
3. **B** — An unconsumed slot pins WAL on disk. This is the number-one Debezium production incident. [PG connector — replication slots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-replication-slots)
4. **C** — `op=d` is a delete; Debezium then emits a tombstone (null value) on the same key. [PG connector — delete events](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-delete-events)
5. **B** — Log compaction uses a null-value record to finally drop the key. [PG connector — delete events](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-delete-events)
6. **B** — Snapshots use `op=r` (read); streaming uses `c/u/d`. [PG connector — snapshots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-snapshots)
7. **B** — `MERGE INTO` is the documented upsert path in Iceberg. [Iceberg MERGE INTO](https://iceberg.apache.org/docs/latest/spark-writes/#merge-into)
8. **B** — SMTs are inline per-record transforms inside the Connect task. [Kafka Connect transforms](https://kafka.apache.org/documentation/#connect_transforms)
9. **B** — Both endpoints must cooperate; Kafka alone is not enough. [Kafka Connect — exactly-once source](https://kafka.apache.org/documentation/#connect_exactlyoncesource)
10. **B** — The schema-history topic is the durable DDL record. [PG connector — schema history](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-schema-history-topic)
