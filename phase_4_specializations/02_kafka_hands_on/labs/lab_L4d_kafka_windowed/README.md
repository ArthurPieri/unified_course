# Lab L4d: Kafka Tumbling-Window Aggregation in Python

## Goal
Run a KRaft-mode Kafka broker locally, produce JSON click events from a Python script, and aggregate them into per-minute tumbling windows in a second Python consumer — without Kafka Streams, just `kafka-python` and a dict.

## Prerequisites
- Docker + Compose v2
- Python 3.11+ with a venv
- `pip install kafka-python==2.0.2`

## Setup

`docker-compose.yml` (single-node KRaft, no ZooKeeper):

```yaml
services:
  kafka:
    image: apache/kafka:3.8.0
    ports: ["9092:9092"]
    environment:
      KAFKA_PROCESS_ROLES: "broker,controller"
      KAFKA_NODE_ID: "1"
      KAFKA_CONTROLLER_QUORUM_VOTERS: "1@kafka:9093"
      KAFKA_LISTENERS: "PLAINTEXT://:9092,CONTROLLER://:9093"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://localhost:9092"
      KAFKA_CONTROLLER_LISTENER_NAMES: "CONTROLLER"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT"
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: "1"
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: "1"
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: "1"
```

Ref: [Kafka — KRaft](https://kafka.apache.org/documentation/#kraft).

`producer.py`:

```python
import json, random, time
from datetime import datetime, timezone
from kafka import KafkaProducer

p = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode(),
    key_serializer=lambda k: k.encode(),
    acks="all",
    enable_idempotence=True,
    linger_ms=50,
)
users = [f"u{i}" for i in range(20)]
pages = ["/", "/pricing", "/docs", "/signup"]
try:
    while True:
        evt = {
            "user": random.choice(users),
            "page": random.choice(pages),
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        p.send("clicks", key=evt["user"], value=evt)
        time.sleep(0.05)
except KeyboardInterrupt:
    p.flush()
```

Ref: [kafka-python — KafkaProducer](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html).

`consumer.py`:

```python
import json, time
from collections import defaultdict
from datetime import datetime
from kafka import KafkaConsumer

c = KafkaConsumer(
    "clicks",
    bootstrap_servers="localhost:9092",
    group_id="click-agg",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda b: json.loads(b.decode()),
)

buckets: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
last_flush = time.time()

for msg in c:
    ts = datetime.fromisoformat(msg.value["ts"])
    bucket = ts.strftime("%Y-%m-%dT%H:%M")
    buckets[bucket][msg.value["page"]] += 1
    if time.time() - last_flush >= 60:
        closed = sorted(buckets)[:-1]  # keep current minute open
        for b in closed:
            print(f"[{b}] {dict(buckets.pop(b))}")
        c.commit()
        last_flush = time.time()
```

Manual `commit()` after printing a closed window gives at-least-once with the dict as an idempotent aggregator within a run. Ref: [kafka-python — KafkaConsumer](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html) · [delivery semantics](https://kafka.apache.org/documentation/#semantics).

## Steps

1. Start Kafka and create the topic with 3 partitions.
   ```bash
   docker compose up -d
   docker exec -it $(docker compose ps -q kafka) \
     /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
     --create --topic clicks --partitions 3 --replication-factor 1
   ```

2. Run the producer in one terminal, the consumer in another.
   ```bash
   python producer.py     # leave running ~2 min
   python consumer.py     # in a second terminal
   ```

3. Observe per-minute output from the consumer:
   ```
   [2026-04-10T14:32] {'/': 512, '/pricing': 498, '/docs': 503, '/signup': 487}
   [2026-04-10T14:33] {'/': 530, '/pricing': 487, '/docs': 511, '/signup': 472}
   ```

## Verify
- [ ] `kafka-topics.sh --describe --topic clicks` shows 3 partitions
- [ ] Producer runs without errors and `p.flush()` returns cleanly on Ctrl-C
- [ ] Consumer prints one summary per closed minute
- [ ] Counts per window are in the low thousands (producer emits ~20 events/sec × 60s)
- [ ] Restarting the consumer with the same `group_id` resumes from the last committed offset, not the beginning

## Cleanup
```bash
docker compose down -v
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `NoBrokersAvailable` | Client cannot reach `localhost:9092`; confirm `KAFKA_ADVERTISED_LISTENERS` matches the client host |
| Consumer prints nothing for > 1 min | Producer may not be running; check with `kafka-console-consumer.sh --topic clicks --from-beginning` |
| Offsets reset on every run | `enable_auto_commit=False` but you never call `c.commit()` — commit after each flush |
| Messages ordered oddly | Order is per-partition; group by `(partition, offset)` if strict order matters |

## Stretch goals
- Swap `kafka-python` for `confluent-kafka-python` (`pip install confluent-kafka`) and benchmark throughput by counting messages/sec over 60 seconds. The librdkafka-backed client is typically several times faster. Ref: [kafka-python — usage](https://kafka-python.readthedocs.io/en/master/usage.html).
- Add a second consumer in the same `group_id` and watch the rebalance logs — each consumer should end up with ~1.5 partitions on average.

## References
See `../../references.md` (module-level).
