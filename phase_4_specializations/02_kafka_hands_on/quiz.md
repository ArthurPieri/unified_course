# Quiz — 02_kafka_hands_on

Ten multiple-choice questions. Answers at the bottom.

---

**1.** Kafka guarantees message order:

A. Across the entire topic
B. Only within a single partition
C. Only when `acks=all`
D. Only in KRaft mode

**2.** You set RF=3 and `min.insync.replicas=2` with producer `acks=all`. The cluster tolerates:

A. Two broker losses without data loss or write outage
B. One broker loss without data loss or write outage
C. Zero broker losses
D. Any number of broker losses

**3.** Which producer setting is the cheapest win against duplicate records on retry?

A. `acks=0`
B. `enable.idempotence=true`
C. `linger.ms=0`
D. `compression.type=none`

**4.** A consumer in group `g1` reads from a 6-partition topic. You start a second consumer in `g1`. What happens?

A. Both read every message
B. The group rebalances so each consumer owns 3 partitions
C. The second consumer is rejected
D. Nothing until you restart the first

**5.** `enable.auto.commit=true` with short interval approximates which delivery mode?

A. Exactly-once
B. At-most-once
C. At-least-once
D. None — it is a debug setting

**6.** You want a topic that keeps only the latest value per key forever. Set:

A. `cleanup.policy=delete`, `retention.ms=-1`
B. `cleanup.policy=compact`
C. `acks=all`
D. `log.flush.interval.messages=1`

**7.** A tombstone record in a compacted topic is:

A. A record with a null key
B. A record with a null value, signaling the key should eventually be removed
C. A special admin message
D. A rejected record

**8.** KRaft replaces which external dependency?

A. Kafka Connect
B. Schema Registry
C. ZooKeeper
D. Kafka Streams

**9.** Consumer group is stuck in a rebalance loop. Most likely cause:

A. `acks=all` on the producer
B. Processing a single poll batch takes longer than `max.poll.interval.ms`
C. `enable.idempotence` is off
D. Topic has only one partition

**10.** Which workload is Kafka the wrong tool for?

A. High-throughput append-only event log with many independent consumers
B. CDC fan-out to a lakehouse
C. Per-message TTL and priority-queue semantics for a small job queue
D. Metric stream aggregation

---

## Answer key

1. **B** — Order is per-partition; cross-partition order is not guaranteed. [Kafka intro](https://kafka.apache.org/documentation/#intro_topics)
2. **B** — RF=3 + `min.insync.replicas=2` tolerates one broker loss with `acks=all` still satisfying both durability and availability. [Kafka replication](https://kafka.apache.org/documentation/#replication)
3. **B** — Idempotence deduplicates retries at no throughput cost. [enable.idempotence](https://kafka.apache.org/documentation/#producerconfigs_enable.idempotence)
4. **B** — Group members share partitions, one partition per consumer. [Kafka intro — consumers](https://kafka.apache.org/documentation/#intro_consumers)
5. **B** — Committing before processing loses messages on crash. [delivery semantics](https://kafka.apache.org/documentation/#semantics)
6. **B** — `compact` is log compaction, retaining latest value per key. [log compaction](https://kafka.apache.org/documentation/#compaction)
7. **B** — Null value on a key is the tombstone signal. [log compaction](https://kafka.apache.org/documentation/#compaction)
8. **C** — KRaft removes ZooKeeper. [KRaft](https://kafka.apache.org/documentation/#kraft)
9. **B** — Exceeding `max.poll.interval.ms` causes the consumer to be evicted, triggering rebalance. [max.poll.interval.ms](https://kafka.apache.org/documentation/#consumerconfigs_max.poll.interval.ms)
10. **C** — Kafka does not do per-message TTL or priority queues; a traditional broker is better. [Kafka use cases](https://kafka.apache.org/documentation/#uses)
