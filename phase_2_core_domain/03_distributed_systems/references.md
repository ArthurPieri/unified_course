# References — 03 Distributed Systems

GAP module — primary source is *Designing Data-Intensive Applications*, Kleppmann. No sibling-dir content reused (see `references/sibling_sources.md` Content gaps table: "Phase 2 · 03_distributed_systems → *Kleppmann DDIA Ch. 5, 6, 9*").

## Books (primary)
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 5 — Replication (single-leader, multi-leader, leaderless; replication lag; quorums)
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 6 — Partitioning (hash vs. range; rebalancing; secondary indexes)
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 7 — Transactions (isolation levels, atomicity) — background for distributed transactions
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 9 — Consistency and consensus (linearizability, CAP, 2PC, Paxos/Raft at overview level)
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — Stream processing (context for Kafka at-least-once delivery and consumer rebalances)

## Consensus protocol papers (cited by name only per sibling_sources.md GAP note)
- Raft consensus protocol — "In Search of an Understandable Consensus Algorithm" (Ongaro & Ousterhout)
- Paxos — "The Part-Time Parliament" (Lamport); "Paxos Made Simple" (Lamport)

## Official docs
- [PostgreSQL streaming replication / warm standby](https://www.postgresql.org/docs/current/warm-standby.html) — canonical single-leader async replication
- [PostgreSQL logical replication](https://www.postgresql.org/docs/current/logical-replication.html) — row-level replication used by CDC
- [Apache Kafka documentation](https://kafka.apache.org/documentation/) — partition replication, consumer groups, rebalancing semantics
- [Kafka cluster expansion](https://kafka.apache.org/documentation/#basic_ops_cluster_expansion) — partition reassignment (rebalancing in practice)
- [Apache Iceberg spec](https://iceberg.apache.org/spec/) — catalog-mediated atomic snapshot commits (the linearizable core of a lakehouse)
- [Apache Iceberg docs](https://iceberg.apache.org/docs/latest/) — concurrent-writer commit semantics
- [Trino documentation](https://trino.io/docs/current/) — distributed SQL engine; coordinator/worker model
- [Apache Spark documentation](https://spark.apache.org/docs/latest/) — driver/executor model; shuffle is the distributed-systems stress point

## Central course references
- [../../references/books.md](../../references/books.md) — DDIA chapter map
- [../../references/glossary.md](../../references/glossary.md) — CAP theorem, eventual consistency entries
- [../../references/sibling_sources.md](../../references/sibling_sources.md) — GAP designation for this module
- [../../references/docs.md](../../references/docs.md)
