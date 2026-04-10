# Quiz — 03 Distributed Systems

10 multiple-choice questions. Pick the single best answer. Answer key with source citations at the bottom.

---

**Q1.** The CAP theorem says that during a network partition, a distributed store must choose between:
- A. Consistency and availability
- B. Consistency and partition-tolerance
- C. Availability and partition-tolerance
- D. Latency and throughput

**Q2.** Why is "partition-tolerance" not really a choice in CAP?
- A. Every distributed database is legally required to be partition-tolerant
- B. Real networks can and do partition (link loss, switch failures), so partition-tolerance is a precondition, not an option
- C. Because the CAP paper says so without justification
- D. Because TCP guarantees no partitions

**Q3.** Rank the following consistency models from strongest to weakest:
- A. Eventual → Causal → Sequential → Linearizable
- B. Linearizable → Sequential → Causal → Eventual
- C. Causal → Linearizable → Sequential → Eventual
- D. Sequential → Linearizable → Causal → Eventual

**Q4.** A Postgres read replica uses asynchronous streaming replication. A client writes to the primary and immediately reads from the replica. What is the expected behavior?
- A. The read always returns the new row — replicas are synchronous by default
- B. The read may return stale data for a brief window — this is replica lag
- C. The read always fails until the replica catches up
- D. Postgres never replicates writes asynchronously

**Q5.** Which replication strategy is most prone to write-write conflicts on the same row?
- A. Single-leader
- B. Multi-leader
- C. Leaderless with R + W > N
- D. No-replication

**Q6.** Hash partitioning vs. range partitioning: which statement is correct?
- A. Hash partitioning makes range scans cheap; range partitioning balances load evenly
- B. Hash partitioning spreads load evenly but makes range scans touch every partition; range partitioning preserves order but can hotspot on time-series keys
- C. Both are identical in practice
- D. Only range partitioning supports rebalancing

**Q7.** Why do production systems use consistent hashing or a fixed number of virtual partitions instead of `hash(key) mod N`?
- A. It is required by the SQL standard
- B. `mod N` requires re-hashing and moving every row whenever the node count N changes
- C. Virtual partitions are faster to hash
- D. Consistent hashing provides linearizability for free

**Q8.** The main weakness of Two-Phase Commit (2PC) is:
- A. It cannot handle more than two participants
- B. If the coordinator fails between prepare and commit, participants are blocked holding locks until it recovers
- C. It requires a leaderless replication layer
- D. It cannot guarantee atomicity

**Q9.** What problem do consensus protocols like Paxos and Raft solve?
- A. Partitioning data across nodes by hash
- B. Getting a group of nodes to agree on a single ordered log of values despite failures
- C. Compressing data at rest
- D. Replacing transaction logs in OLTP databases

**Q10.** Two concurrent Spark jobs try to append to the same Iceberg table. One gets a commit conflict. Why?
- A. Iceberg is not ACID
- B. The catalog serializes commits as an atomic snapshot swap, so a losing writer must retry against the latest snapshot
- C. Spark does not support concurrent writes ever
- D. Object storage overwrites files on write

---

## Answer key

| Q | Answer | Source |
|---|---|---|
| 1 | A | *DDIA, Kleppmann, Ch. 9*; [glossary](../../references/glossary.md#distributed-systems) |
| 2 | B | *DDIA, Kleppmann, Ch. 9* |
| 3 | B | *DDIA, Kleppmann, Ch. 9* |
| 4 | B | *DDIA, Kleppmann, Ch. 5*; [PostgreSQL streaming replication](https://www.postgresql.org/docs/current/warm-standby.html) |
| 5 | B | *DDIA, Kleppmann, Ch. 5* |
| 6 | B | *DDIA, Kleppmann, Ch. 6* |
| 7 | B | *DDIA, Kleppmann, Ch. 6* |
| 8 | B | *DDIA, Kleppmann, Ch. 9* |
| 9 | B | *DDIA, Kleppmann, Ch. 9* (Raft/Paxos cited by name only per `references/sibling_sources.md` GAP note) |
| 10 | B | [Apache Iceberg spec](https://iceberg.apache.org/spec/); *DDIA, Kleppmann, Ch. 7* |
