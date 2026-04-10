# Module 02: Kafka Hands-On (8h)

> Kafka is the default durable log under most streaming systems — CDC, event sourcing, microservice integration, metrics fan-out. You need enough Kafka to reason about partitions, consumer groups, delivery semantics, and retention before you trust it with a pipeline. This module is deliberately hands-on: theory only where theory changes the command you type.

## Learning goals
- Describe Kafka's topic/partition/replication model and what the ISR guarantees
- Choose `acks`, idempotence, and batching settings for a producer against latency/throughput/durability targets
- Explain consumer groups, partition assignment, and the offset-commit lifecycle
- Compare at-most-once, at-least-once, and exactly-once delivery and name the config that enables each
- Distinguish time-based retention from log compaction and pick the right one per topic
- Stand up a KRaft-mode Kafka with no ZooKeeper and run a Python producer/consumer against it
- State two scenarios where Kafka is the wrong tool

## Prerequisites
- [../../phase_1_foundations/04_docker/](../../phase_1_foundations/04_docker/) — Compose, healthchecks
- [../../phase_1_foundations/03_python/](../../phase_1_foundations/03_python/) — venv, pip, running scripts

## Reading order
1. This README
2. [labs/lab_L4d_kafka_windowed/README.md](labs/lab_L4d_kafka_windowed/README.md)
3. [quiz.md](quiz.md)

## Concepts

### Topics, partitions, replication factor, ISR
A **topic** is a named, append-only log partitioned across brokers. Each **partition** is an ordered, immutable sequence — order is guaranteed only within a partition, never across partitions. **Replication factor** is how many brokers hold a copy of each partition; one is the leader, the rest are followers. The **in-sync replica set (ISR)** is the subset of followers currently caught up to the leader. Kafka only acknowledges a write as durable once the configured `min.insync.replicas` of the ISR have the record, which is why a replication factor of 3 with `min.insync.replicas=2` is the canonical production setting: it tolerates one broker loss without data loss or a write outage.
Ref: [Kafka design — replication](https://kafka.apache.org/documentation/#replication) · [Kafka docs — min.insync.replicas](https://kafka.apache.org/documentation/#topicconfigs_min.insync.replicas)

### Producers: `acks`, idempotence, batching
The producer's `acks` setting controls durability. `acks=0` fire-and-forget, no guarantee; `acks=1` waits for the leader only, data can be lost if the leader dies before replicating; `acks=all` waits for all in-sync replicas and is the only safe setting for data you cannot lose. Enabling `enable.idempotence=true` makes the producer attach a producer ID and sequence number per partition so the broker deduplicates retries — you get no duplicates on retry within a single producer session, at zero throughput cost. Batching (`linger.ms`, `batch.size`) amortizes network and compression overhead: a non-zero `linger.ms` trades a few milliseconds of latency for a large throughput gain.
Ref: [Kafka producer configs — acks](https://kafka.apache.org/documentation/#producerconfigs_acks) · [Kafka producer configs — enable.idempotence](https://kafka.apache.org/documentation/#producerconfigs_enable.idempotence)

### Consumer groups, offsets, commits, rebalance
A **consumer group** is a set of consumers sharing a `group.id`; Kafka assigns each partition to exactly one consumer in the group, so adding consumers (up to the partition count) scales throughput linearly. Each consumer tracks the next offset to read and periodically **commits** it to the internal `__consumer_offsets` topic. With `enable.auto.commit=true` commits happen on a timer — simple, but you can lose messages if processing crashes between commit and handling. Manual `commitSync()` after processing gives at-least-once. A **rebalance** is triggered when group membership changes; during a rebalance the group briefly stops consuming while partitions are reassigned.
Ref: [Kafka intro — consumers](https://kafka.apache.org/documentation/#intro_consumers) · [Kafka consumer configs — enable.auto.commit](https://kafka.apache.org/documentation/#consumerconfigs_enable.auto.commit)

### Delivery semantics: at-most / at-least / exactly-once
**At-most-once**: commit offset before processing. A crash after commit loses the record. `enable.auto.commit=true` with short commit interval approximates this. **At-least-once**: process first, then commit. A crash between processing and commit re-delivers the record, so the downstream must be idempotent. This is the default target. **Exactly-once** inside Kafka requires the idempotent producer plus transactions (`transactional.id`, `initTransactions`, `beginTransaction`, `sendOffsetsToTransaction`, `commitTransaction`) so producing output records and committing input offsets happen in one atomic commit. End-to-end exactly-once additionally needs the sink system to cooperate.
Ref: [Kafka design — message delivery semantics](https://kafka.apache.org/documentation/#semantics) · [Kafka producer configs — transactional.id](https://kafka.apache.org/documentation/#producerconfigs_transactional.id)

### Retention: time-based vs log-compacted
Every topic has a cleanup policy. The default `delete` policy drops segments older than `retention.ms` (or `retention.bytes`), which is what you want for event streams. The `compact` policy keeps **only the latest value per key** forever — older values for the same key are eventually removed by a background compaction thread. Compaction is what makes Kafka usable as a current-state store for CDC and config topics; tombstones (null values) are the signal to drop a key entirely. You can combine both with `cleanup.policy=compact,delete`.
Ref: [Kafka design — log compaction](https://kafka.apache.org/documentation/#compaction) · [Kafka topic configs — cleanup.policy](https://kafka.apache.org/documentation/#topicconfigs_cleanup.policy)

### KRaft: Kafka without ZooKeeper
KRaft replaces the ZooKeeper dependency with a Raft-based quorum of Kafka controller nodes that store metadata directly in Kafka's own log. Production Kafka has been fully supported on KRaft since 3.3 and ZooKeeper mode is removed in 4.0. Practically this means one fewer service in the Compose file, faster failover, and higher metadata throughput. Every new lab in this course uses KRaft.
Ref: [Kafka — KRaft](https://kafka.apache.org/documentation/#kraft)

### When Kafka is the wrong answer
Kafka is excellent for high-throughput, durable, ordered logs with many consumers. It is a poor fit when you need per-message TTL, complex per-message routing, priority queues, ack-per-message with redelivery, or low-volume (< a few events/sec) integrations — a traditional broker (RabbitMQ, SQS) or even a database table is simpler. It is also the wrong answer if you need a single writer with strict global ordering across millions of keys; partitioning forces you to shard on a key. *DDIA* Ch. 11 discusses the trade-offs between log-based and traditional message brokers in detail.
Ref: [Kafka intro — use cases](https://kafka.apache.org/documentation/#uses) · *Designing Data-Intensive Applications*, Kleppmann, Ch. 11

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L4d_kafka_windowed` | Python producer emits click events; consumer aggregates counts per minute in tumbling windows | 90m | [labs/lab_L4d_kafka_windowed/](labs/lab_L4d_kafka_windowed/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Producer reports `NotEnoughReplicasException` | `min.insync.replicas` not satisfied | Bring replicas back into ISR or lower the setting for non-critical topics | [Kafka replication](https://kafka.apache.org/documentation/#replication) |
| Consumer stuck in repeated rebalance | Processing time per batch exceeds `max.poll.interval.ms` | Increase the interval or reduce `max.poll.records` | [consumer configs — max.poll.interval.ms](https://kafka.apache.org/documentation/#consumerconfigs_max.poll.interval.ms) |
| Messages appear duplicated after retry | Producer idempotence off | Set `enable.idempotence=true` | [producer configs — enable.idempotence](https://kafka.apache.org/documentation/#producerconfigs_enable.idempotence) |
| Compacted topic keeps growing | Tombstones never produced for deletes | Emit a null value on the key to retire it | [log compaction](https://kafka.apache.org/documentation/#compaction) |
| `kafka-python` hangs on `producer.send()` | Advertised listener unreachable from the client | Fix `KAFKA_ADVERTISED_LISTENERS` to a hostname the client can resolve | [kafka-python usage](https://kafka-python.readthedocs.io/en/master/usage.html) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Explain what `acks=all` + `min.insync.replicas=2` with RF=3 tolerates and does not tolerate
- [ ] Describe the offset-commit lifecycle and the difference between auto- and manual commits
- [ ] Name the producer config that enables idempotence and the one that opens a transaction
- [ ] Pick `delete` vs `compact` given a workload description
- [ ] Write a `kafka-python` producer and consumer against a KRaft-mode broker
- [ ] Give two scenarios where you would choose RabbitMQ or SQS over Kafka
