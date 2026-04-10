# Module 05: Streaming Concepts — Event Time, Windows, Semantics, CDC (6h)

> GAP module — no sibling source. Written from *Designing Data-Intensive Applications* Ch. 11, the Kafka docs, and the Debezium architecture docs. Deliberately conceptual: this course treats streaming as literacy, not craft, because **90%+ of real pipelines are batch** (see `UNIFIED_COURSE_PLAN.md:L67`).

## Learning goals
- Distinguish **event time** from **processing time** and explain why the difference matters
- Name the three standard window types — tumbling, sliding, session — and give one use case for each
- Explain **watermarks** and how a streaming system decides to emit a window result in the presence of late data
- Contrast **at-most-once**, **at-least-once**, and **exactly-once** delivery semantics and identify the requirements for each
- Sketch the Kafka producer / topic / partition / consumer-group mental model
- Describe **Change Data Capture** (CDC) at the level of the Debezium architecture
- Defend a batch-first default: articulate when streaming is actually required vs. when it is a "cool" choice that adds operational burden

## Prerequisites
- [`../02_etl_elt_patterns/`](../02_etl_elt_patterns/) — ETL/ELT vocabulary and idempotency
- [`../03_distributed_systems/`](../03_distributed_systems/) — partitioning and replication basics

## Reading order
1. This README
2. *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — Stream Processing
3. [Kafka — Introduction](https://kafka.apache.org/documentation/#introduction)
4. [Debezium — Architecture](https://debezium.io/documentation/reference/stable/architecture.html)
5. [`quiz.md`](quiz.md)

## Concepts

### Event time vs. processing time
An event has two clocks. **Event time** is when the thing actually happened at the source (a user tapped a button at `10:00:03.214`). **Processing time** is when the stream processor sees the event (which may be seconds, minutes, or hours later, depending on network and batching). Windowing by processing time is easy but wrong: late events fall into the wrong bucket, and replay produces different results than live execution. Windowing by event time is correct but forces the system to cope with out-of-order delivery and late arrivals.
Ref: *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — Reasoning About Time.

A production rule of thumb: if anybody will ever ask "how many events happened in the hour 14:00–15:00?", you need event-time windows. Any answer based on processing time is meaningless after the first retry.

### Windows: tumbling, sliding, session
A **window** is a finite slice of an infinite stream. The three standard shapes are:

- **Tumbling** — fixed-size, non-overlapping, contiguous buckets (e.g., "count events per 1-minute bucket"). Each event belongs to exactly one window.
- **Sliding (hopping)** — fixed-size windows that overlap at a fixed hop (e.g., "5-minute window, advanced every 1 minute"). Each event belongs to multiple windows.
- **Session** — variable-size windows bounded by an **inactivity gap** (e.g., "user activity separated by more than 30 minutes is a new session"). Window length is data-dependent.

Tumbling is the default for periodic metrics. Sliding gives smoother moving-average curves. Session windows are the right tool for user-activity analytics.
Ref: *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — Types of Windows.

### Watermarks and late data
Because events arrive out of order, the processor cannot know when a window is "complete". A **watermark** is a heuristic assertion: *"I believe I have now seen all events with event time ≤ T."* When the watermark passes a window's end, the window is closed and its result is emitted. Events arriving after the watermark has passed are **late data** and can be handled in three ways: drop them, route them to a side output, or re-emit an updated window result.
Ref: *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — Stream Joins and Fault Tolerance (watermark discussion).

There is no correct watermark — it is a trade-off between **latency** (emit results sooner, risk under-counting) and **completeness** (wait longer, accept staler results). Pick your side knowingly.

### Delivery semantics: at-most-once, at-least-once, exactly-once
Three levels describe how many times a message may be processed end-to-end:

- **At-most-once** — fire and forget. The producer does not retry; a dropped message is lost. Simple, lowest latency, acceptable only when missing data is cheaper than duplicated data (e.g., some metrics).
- **At-least-once** — the producer retries until an acknowledgement arrives. Messages may be **duplicated** on retry. The consumer must be **idempotent**, i.e., safe to apply the same message twice without changing the result.
- **Exactly-once** — each message affects the downstream state exactly once. In practice this is at-least-once delivery combined with idempotent consumers *or* a transactional protocol between producer, broker, and consumer that atomically commits both the consumer offset and the downstream write.

Kafka supports **idempotent producers** (dedup by producer ID + sequence number) and **transactional writes** across topics and consumer offsets, which together give exactly-once semantics *within* Kafka. Exactly-once to an **external** sink (a Postgres table, a REST API) is only true if that sink is idempotent or participates in the transaction.
Ref: *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — Fault Tolerance; [Kafka — Semantics](https://kafka.apache.org/documentation/#semantics).

### Kafka: the partition / consumer-group mental model
Kafka organizes messages into **topics**. A topic is partitioned into one or more **partitions**; each partition is a totally ordered, append-only log stored on one or more brokers. **Producers** append records to a partition (by key hash, by round-robin, or explicitly). **Consumers** read records in offset order.

A **consumer group** is a set of consumers cooperating on one topic: Kafka assigns each partition to exactly one consumer in the group, so scaling out = adding consumers up to the number of partitions. Ordering is guaranteed **within a partition**, never across partitions. Two practical consequences:

1. The partition count bounds your parallelism — pick it with future scale in mind, because repartitioning is painful.
2. If ordering matters per key (e.g., per `user_id`), the producer must hash-partition by that key so all records for the key land on the same partition.

Ref: [Kafka — Introduction](https://kafka.apache.org/documentation/#introduction) (sections: "Topics and Logs", "Distribution", "Consumers").

### Change Data Capture (CDC)
**Change Data Capture** is the technique of turning inserts, updates, and deletes on a source database into an event stream, typically by reading the database's write-ahead log (WAL / binlog / redo log). The dominant open-source implementation is **Debezium**, which runs as a set of Kafka Connect source connectors — one per database kind (Postgres, MySQL, SQL Server, MongoDB, etc.). Each connector tails the source's log, reconstructs row-level change events, and publishes them to Kafka topics (one topic per table by default).

Debezium's architecture, as documented on their site, has three moving pieces:
1. The **source database** with its transaction log enabled (e.g., Postgres logical replication slot).
2. The **Debezium connector** running inside Kafka Connect, which reads the log and emits change events.
3. **Kafka** as the durable buffer, feeding downstream consumers (a warehouse loader, a cache invalidator, a search indexer).

Because Debezium reads the log — not the live tables — it produces a complete, ordered history of changes with no load on the source query path. That property is what makes CDC the correct pattern for replicating an OLTP database into a lakehouse, as opposed to periodic `SELECT * WHERE updated_at > ?` batch pulls (which miss deletes and intermediate states).
Ref: [Debezium — Architecture](https://debezium.io/documentation/reference/stable/architecture.html); glossary entry at `references/glossary.md:L54-L55`.

### When streaming is actually needed
Streaming has real operational cost: you must run brokers, reason about out-of-order events, pick watermarks, handle late data, and debug systems that never stop. The honest question is: **what decision is being made on the result, and how fast does it need to arrive?**

- **Fraud scoring on a payment** — a decision is made in the next 200 ms. Streaming is required.
- **Real-time inventory for flash sales** — minutes matter. Streaming or micro-batch.
- **Daily executive dashboard** — hours are fine. Batch.
- **Month-end finance reporting** — days are fine. Batch, full reload if needed.
- **"We want a live dashboard because it's cool"** — no decision depends on sub-minute freshness. Batch.

The UNIFIED_COURSE_PLAN positions this explicitly: "Batch vs. streaming: when each matters, 90%+ of real work is batch" (`UNIFIED_COURSE_PLAN.md:L67`). This module teaches streaming literacy — enough to read a Kafka topic, reason about event time, review a CDC design — without pretending a learner's first pipeline should be a Flink job.

When a streaming pipeline is genuinely required, the typical industry stack is **Debezium → Kafka → Spark Structured Streaming / Flink → sink** (with the sink usually being either a low-latency serving store or a lakehouse table updated in micro-batches). Most of the "real time" you see in dashboards is in fact micro-batch at 1–5 minute cadence.

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_05_streaming_read` (Phase 4) | Run a single-broker Kafka, publish and consume a topic, inspect partitions | 60m | covered in Phase 4 · Kafka module |

> This module is conceptual. Hands-on Kafka and CDC labs live in Phase 4, where the full-stack compose from `../dataeng/` is introduced.

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Hourly counts differ between live and replayed runs | Windowing by processing time instead of event time | Switch to event-time windows with an explicit watermark policy | *DDIA*, Kleppmann, Ch. 11 |
| Out-of-order events are silently dropped | Watermark policy is too aggressive | Widen the allowed lateness or route late events to a side output | *DDIA*, Kleppmann, Ch. 11 |
| Duplicate rows appear in the downstream table after a retry | Consumer is not idempotent; delivery is at-least-once | Make the sink idempotent (upsert by primary key) or use Kafka transactions end-to-end | [Kafka — Semantics](https://kafka.apache.org/documentation/#semantics) |
| Adding consumers does not increase throughput | Topic has fewer partitions than consumers in the group | Increase the partition count (plan ahead — it's disruptive) | [Kafka — Introduction](https://kafka.apache.org/documentation/#introduction) |
| CDC replica drifts from source after a schema change | Connector not configured to handle DDL / schema evolution | Enable schema history topic and test the change in a staging connector | [Debezium — Architecture](https://debezium.io/documentation/reference/stable/architecture.html) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Define event time and processing time and give an example where they diverge
- [ ] Pick tumbling, sliding, or session windows for a given analytics question
- [ ] Explain a watermark in one sentence and name the latency/completeness trade-off
- [ ] Rank at-most-once, at-least-once, and exactly-once by operational cost and data safety
- [ ] Draw a Kafka topic with three partitions and a consumer group of two, and assign partitions
- [ ] Describe how Debezium produces change events without querying the source tables
- [ ] Take a proposed "real-time" pipeline and argue whether batch would suffice
