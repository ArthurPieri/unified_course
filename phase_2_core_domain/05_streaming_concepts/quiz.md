# Module 05: Streaming Concepts — Exit Quiz

8 multiple-choice questions. Pass mark: 7/8. Answers with primary-source citations at the bottom.

---

**Q1.** A user taps a button at `10:00:03` and the event arrives at the stream processor at `10:04:17` after a mobile-network delay. Which statement is correct?

A. Both timestamps are "processing time"
B. `10:00:03` is event time; `10:04:17` is processing time
C. `10:00:03` is processing time; `10:04:17` is event time
D. They are only different if Kafka is unavailable

---

**Q2.** You need "count of events per 1-minute bucket, non-overlapping". Which window type is that?

A. Sliding (hopping)
B. Session
C. Tumbling
D. Global

---

**Q3.** A **watermark** in a stream processor is best described as...

A. A signature that prevents tampering with events
B. An assertion that all events with event time ≤ T have probably been seen, used to decide when to emit a window's result
C. A hard deadline after which the pipeline restarts
D. A Kafka partition boundary

---

**Q4.** Your consumer writes every incoming Kafka message to a REST API that is not idempotent. The pipeline is configured for at-least-once delivery. What is the most likely operational bug?

A. Messages will be lost
B. Messages may be delivered to the API more than once, creating duplicate side effects
C. The broker will crash
D. The consumer will skip every second message

---

**Q5.** A Kafka topic has 4 partitions. A consumer group has 6 consumers subscribed to it. What happens?

A. All 6 consumers read all 4 partitions in parallel
B. Kafka assigns each partition to exactly one consumer in the group; 2 consumers sit idle
C. The extra consumers read from a shadow topic
D. Kafka rejects the subscription

---

**Q6.** Which statement about Debezium is correct?

A. Debezium runs scheduled `SELECT * FROM table WHERE updated_at > ?` queries against the source database
B. Debezium is a standalone broker that replaces Kafka
C. Debezium is a set of Kafka Connect source connectors that read the source database's write-ahead log and publish row-level change events to Kafka topics
D. Debezium only works with MongoDB

---

**Q7.** To guarantee **exactly-once** end-to-end from Kafka to an external Postgres table, which of the following is the cleanest approach in practice?

A. Enable at-most-once on the producer
B. Make the Postgres write idempotent (upsert by primary key) so at-least-once delivery plus retries produce the same final state
C. Turn off consumer offsets entirely
D. Use a single consumer with no group id

---

**Q8.** For a daily executive dashboard that refreshes every morning at 07:00, which paradigm is the correct default?

A. Sub-second streaming with Flink
B. Batch — hours of latency are fine, and streaming adds operational cost without improving the decision
C. Micro-batch every 10 seconds
D. CDC with exactly-once semantics

---

## Answer key

1. **B** — Event time is when the thing happened at the source; processing time is when the processor sees it. Ref: *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — Reasoning About Time
2. **C** — Tumbling windows are fixed-size, non-overlapping, and contiguous. Ref: *DDIA*, Kleppmann, Ch. 11 — Types of Windows
3. **B** — A watermark is a heuristic "all events with event time ≤ T have probably been seen" that drives window emission. Ref: *DDIA*, Kleppmann, Ch. 11 — Fault Tolerance / watermarks
4. **B** — At-least-once + non-idempotent sink = duplicate side effects on retry. Ref: [Kafka — Semantics](https://kafka.apache.org/documentation/#semantics); *DDIA*, Ch. 11 — Fault Tolerance
5. **B** — Kafka assigns each partition to exactly one consumer in a group; extra consumers stay idle. Ref: [Kafka — Introduction](https://kafka.apache.org/documentation/#introduction) (Consumers)
6. **C** — Debezium is a set of Kafka Connect source connectors that tail the source's transaction log. Ref: [Debezium — Architecture](https://debezium.io/documentation/reference/stable/architecture.html)
7. **B** — An idempotent sink (upsert by primary key) turns at-least-once into effectively exactly-once at the state level. Ref: [Kafka — Semantics](https://kafka.apache.org/documentation/#semantics); *DDIA*, Ch. 11 — Fault Tolerance
8. **B** — Batch is the correct default; streaming is only justified when a decision depends on sub-minute freshness. Ref: `UNIFIED_COURSE_PLAN.md:L67` ("90%+ of real work is batch")
