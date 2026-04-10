# Module 03: Distributed Systems for Data Engineers (8h)

> GAP module — no sibling source exists. Written from *Designing Data-Intensive Applications*, Kleppmann (primary) plus canonical tool docs. Scope is intentionally practitioner-level: the parts of distributed-systems theory a data engineer hits when operating a lakehouse, not a graduate course.

## Learning goals
- State the CAP theorem precisely and explain why partition-tolerance is non-negotiable in practice
- Rank the common consistency models (linearizable, sequential, causal, eventual) from strongest to weakest and give an example system for each
- Compare single-leader, multi-leader, and leaderless replication, and name one failure mode of each
- Contrast hash and range partitioning and explain what "rebalancing" costs
- Explain at overview level why distributed transactions (2PC) are brittle and what consensus protocols (Paxos, Raft) solve
- Identify three concrete situations a data engineer hits replica lag, stale reads, or split-brain in a lakehouse or warehouse

## Prerequisites
- [../../phase_1_foundations/02_networking/README.md](../../phase_1_foundations/02_networking/README.md)
- [../01_data_modeling/README.md](../01_data_modeling/README.md)

## Reading order
1. This README
2. *Designing Data-Intensive Applications*, Kleppmann, Ch. 5, Ch. 6, Ch. 9 (the spine of this module)
3. `quiz.md`

## Concepts

### Why a data engineer needs this
Every distributed store a data engineer touches — Kafka, Iceberg catalogs backed by a metastore, Trino workers, Spark executors, Postgres replicas, S3-compatible object storage — is a distributed system. The questions "why did my read miss the row I just wrote?", "why did two writers both succeed and produce inconsistent state?", and "why is my backfill idempotent on paper but not in practice?" all trace back to replication, partitioning, and consistency decisions. You do not need to implement Raft, but you need enough vocabulary to read tool docs accurately and to debug production incidents.

### CAP theorem
The CAP theorem states that in a network that can partition (drop or delay messages arbitrarily), a distributed store cannot simultaneously provide **C**onsistency (every read sees the most recent write) and **A**vailability (every request receives a non-error response) — it must drop one when a partition occurs (*DDIA, Kleppmann, Ch. 9*; [glossary entry](../../references/glossary.md#distributed-systems)). Because real networks *do* partition (NIC failures, switch failures, asymmetric routing), partition-tolerance is not a choice you get to make; the real trade-off is **CP vs. AP** during a partition. A CP system refuses writes on the minority side rather than diverge; an AP system accepts writes on both sides and reconciles later.

CAP is commonly misread as a three-way knob; it is not. Outside of partitions, systems can (and do) provide both C and A. The theorem only constrains behavior *during* a partition.

### Consistency models — a hierarchy
Ordered from strongest to weakest (*DDIA, Kleppmann, Ch. 9*):

- **Linearizable** — every operation appears to take effect atomically at some point between its start and end, and all clients see a single, global real-time order. Example: a single-leader Postgres primary, or a Raft-backed metadata store. The most expensive guarantee; impossible to provide under a network partition without sacrificing availability.
- **Sequential** — all clients see operations in the same order, but that order need not match real time. Weaker than linearizable.
- **Causal** — if A happened-before B (B was written after reading A), every client sees A before B. Concurrent writes can be reordered. This is the strongest consistency you can get while remaining available under partitions.
- **Eventual** — replicas converge to the same state if no new writes arrive; intermediate reads may be stale, out-of-order, or monotonically regressing. Example: S3-compatible object stores historically, and leaderless DynamoDB-style systems under default settings. See the [glossary entry](../../references/glossary.md#distributed-systems) and *DDIA, Kleppmann, Ch. 5*.

Practitioner rule of thumb: if a system promises "eventual consistency," assume reads can return any value ever written until the system tells you otherwise.

### Replication strategies
Replication keeps a copy of data on multiple nodes to survive node failure and serve reads closer to clients (*DDIA, Kleppmann, Ch. 5*):

- **Single-leader** (a.k.a. primary/replica, master/slave). All writes go to one leader; the leader streams its change log to followers. Postgres streaming replication is the canonical example ([PostgreSQL docs](https://www.postgresql.org/docs/current/warm-standby.html)). Simple mental model; failure mode: **replica lag** — a read routed to a follower can miss a just-committed write — and **failover complexity** during leader loss.
- **Multi-leader**. Writes accepted at multiple leaders, each of which replicates to the others. Useful for multi-region active-active. Failure mode: **write-write conflicts** on the same row at different leaders, which must be resolved by last-writer-wins (lossy), CRDTs, or application merge logic (*DDIA, Ch. 5*).
- **Leaderless** (a.k.a. Dynamo-style). Clients write to several replicas in parallel; a read quorum + write quorum overlap guarantees the read sees the latest write (R + W > N). Failure mode: **sloppy quorums** and hinted handoffs can still return stale reads after network partitions, and the system relies on read-repair + anti-entropy to converge (*DDIA, Ch. 5*).

For a data engineer, the common concrete symptom is **replica lag on a read replica used for analytics**: your dashboard sums a column right after a producer writes a new row, and the sum is one row short for a few seconds. The fix is either to route reads to the leader, to wait for a read-your-writes marker, or to accept the staleness explicitly.

### Partitioning (sharding)
Partitioning splits a dataset across nodes so that each node owns a subset (*DDIA, Kleppmann, Ch. 6*). Two dominant strategies:

- **Range partitioning**. Keys are assigned to contiguous ranges (e.g., `A–F`, `G–M`). Preserves order, so range scans are cheap. Hotspotting is the main risk: if the key is `created_at`, today's partition gets every write.
- **Hash partitioning**. Keys are hashed, and the hash space is split across nodes. Spreads load evenly, at the cost of making range scans touch every partition. Kafka topic partitioning, DynamoDB partition keys, and many Iceberg partition specs use this.

**Rebalancing** — moving partitions when nodes are added or removed — is the operation that determines whether a system can grow without downtime. Naive `hash(key) mod N` requires re-hashing every row when N changes; production systems use **consistent hashing** or a **fixed number of virtual partitions** decoupled from physical nodes to limit the data movement per rebalance (*DDIA, Ch. 6*). Kafka assigns partitions to brokers via a controller rather than rehashing ([Kafka documentation](https://kafka.apache.org/documentation/#basic_ops_cluster_expansion)).

### Distributed transactions, 2PC, and consensus
A **distributed transaction** commits atomically across multiple nodes or services. **Two-Phase Commit (2PC)** is the classical protocol: a coordinator asks every participant to "prepare" (vote yes/no after durably logging), then sends "commit" or "abort" based on the unanimous vote. 2PC is correct but brittle: if the coordinator crashes between the prepare and commit phases, participants are stuck holding locks until it recovers — the **blocking problem** (*DDIA, Kleppmann, Ch. 9*).

**Consensus protocols** — Paxos, Raft, Zab, Viewstamped Replication — solve a more fundamental problem: get a group of nodes to agree on a single value (and, by extension, on an ordered log of values) despite failures. They are used to replicate metadata stores, elect leaders, and back strongly-consistent coordination services. Raft was designed to be more understandable than Paxos and is widely deployed in production (etcd, Consul, CockroachDB, TiKV). For this course, the practitioner take is: whenever a tool says "we use Raft/etcd/ZooKeeper for coordination," that component is the linearizable core of an otherwise eventually-consistent system, and losing quorum on it halts writes.

### Why this matters for operating a lakehouse
Three concrete places this theory hits a data engineer:

1. **Writing to distributed stores.** Iceberg commits to an object store + catalog pair. The catalog (HMS, Nessie, REST catalog) is the linearizable point; concurrent writers race on its swap ([Iceberg spec](https://iceberg.apache.org/spec/)). Understanding that two writers to the same table serialize through the catalog explains commit retries and isolation-level errors.
2. **Debugging replica lag.** A dashboard on a Postgres read replica misses the row an upstream service just wrote. Not a bug — it is the advertised behavior of single-leader async replication ([PostgreSQL docs](https://www.postgresql.org/docs/current/warm-standby.html); *DDIA, Ch. 5*).
3. **Kafka consumer offsets.** A consumer group rebalance can reassign partitions mid-flight; correct processing requires idempotent writes keyed on `(partition, offset)` because at-least-once delivery means the same record may be handed out twice during rebalance ([Kafka documentation](https://kafka.apache.org/documentation/)).

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_03_replica_lag_postgres` | Observe and measure replica lag on a two-node Postgres compose | 45m | built in Phase 3 |
| `lab_03_kafka_rebalance` | Trigger a consumer-group rebalance and observe duplicate delivery | 45m | built in Phase 4 · Kafka |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Read-after-write returns stale data | Read routed to an async follower | Route critical reads to leader, or wait for LSN/commit-marker | *DDIA, Ch. 5*; [PostgreSQL streaming replication](https://www.postgresql.org/docs/current/warm-standby.html) |
| Two concurrent Iceberg writers, one fails with a commit conflict | Catalog is the serialization point; the loser must retry on the latest snapshot | Use the engine's built-in retry loop; do not bypass the catalog | [Iceberg spec](https://iceberg.apache.org/spec/) |
| Kafka consumer processes the same record twice | At-least-once delivery + rebalance redelivery | Idempotent sink keyed on `(topic, partition, offset)` | [Kafka documentation](https://kafka.apache.org/documentation/) |
| Cluster halts on metadata writes when one node is down | Lost quorum on the Raft/ZooKeeper-backed coordinator | Restore quorum; plan odd-numbered coordinator counts | *DDIA, Ch. 9* |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] State CAP in one sentence and explain why it is a "during partition" constraint
- [ ] Rank linearizable, sequential, causal, eventual from strongest to weakest
- [ ] Name one failure mode each for single-leader, multi-leader, and leaderless replication
- [ ] Explain the difference between hash and range partitioning and what rebalancing costs
- [ ] Explain at a whiteboard level why 2PC is blocking and what problem Raft solves
- [ ] Point to the linearizable core of your lakehouse (the catalog) and explain why writes serialize through it
