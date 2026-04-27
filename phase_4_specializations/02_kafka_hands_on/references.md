# References — 02_kafka_hands_on

## Primary docs (kafka.apache.org)
- [Kafka introduction](https://kafka.apache.org/documentation/#introduction) — topics, partitions, consumers, use cases
- [Kafka design — replication](https://kafka.apache.org/documentation/#replication) — leaders, followers, ISR, `min.insync.replicas`
- [Kafka design — message delivery semantics](https://kafka.apache.org/documentation/#semantics) — at-most/at-least/exactly-once
- [Kafka design — log compaction](https://kafka.apache.org/documentation/#compaction) — key-based retention, tombstones
- [Kafka — KRaft](https://kafka.apache.org/documentation/#kraft) — controller quorum, no ZooKeeper
- [Producer configs](https://kafka.apache.org/documentation/#producerconfigs) — `acks`, `enable.idempotence`, `linger.ms`, `batch.size`, `transactional.id`
- [Consumer configs](https://kafka.apache.org/documentation/#consumerconfigs) — `group.id`, `enable.auto.commit`, `max.poll.interval.ms`, `max.poll.records`
- [Topic configs](https://kafka.apache.org/documentation/#topicconfigs) — `cleanup.policy`, `retention.ms`, `min.insync.replicas`
- [Kafka quickstart](https://kafka.apache.org/quickstart) — topic CLI, console producer/consumer

## Primary docs (kafka-python)
- [kafka-python — usage](https://kafka-python.readthedocs.io/en/master/usage.html) — `KafkaProducer`, `KafkaConsumer` examples
- [kafka-python — KafkaProducer API](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html)
- [kafka-python — KafkaConsumer API](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html)

## Books
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — "Stream Processing" (log-based vs AMQP-style brokers, partitioning, delivery semantics)

## Managed-service parallel
- [Amazon MSK — What is Amazon MSK?](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html) — Amazon MSK overview, Kafka concepts recap, MSK vs Kinesis decision matrix (managed parallel to the OSS stack in this module).
