# Module 05: Streaming Concepts — References

## Canonical book
- *Designing Data-Intensive Applications*, Martin Kleppmann, O'Reilly 2017 — **Ch. 11 Stream Processing**
  - Reasoning about time (event time vs. processing time)
  - Types of windows (tumbling, sliding/hopping, session)
  - Watermarks and late data
  - Fault tolerance and exactly-once semantics
  - Stream joins

## Kafka docs (kafka.apache.org)
- [Kafka — Introduction](https://kafka.apache.org/documentation/#introduction) — topics, partitions, producers, consumers, consumer groups
- [Kafka — Design](https://kafka.apache.org/documentation/#design) — log structure, replication, distribution
- [Kafka — Semantics](https://kafka.apache.org/documentation/#semantics) — at-most-once, at-least-once, exactly-once; idempotent producers; transactions
- [Kafka Connect](https://kafka.apache.org/documentation/#connect) — source/sink connector framework that Debezium plugs into

## Debezium docs (debezium.io)
- [Debezium — Architecture](https://debezium.io/documentation/reference/stable/architecture.html) — connector model, Kafka Connect, source-database log tailing
- [Debezium — Connectors](https://debezium.io/documentation/reference/stable/connectors/index.html) — per-database connector index (Postgres, MySQL, SQL Server, MongoDB, etc.)

## Cross-course index
- `references/books.md:L16` — DDIA Ch. 11 entry
- `references/docs.md:L49-L51` — Debezium and Kafka doc entries
- `references/glossary.md:L53-L58` — CDC and Kafka glossary entries
- `UNIFIED_COURSE_PLAN.md:L67` — "90%+ of real work is batch" positioning
- `UNIFIED_COURSE_PLAN.md:L185` — batch vs. micro-batch vs. streaming latency bands
- `UNIFIED_COURSE_PLAN.md:L212` — delivery semantics and event streaming fundamentals scope
