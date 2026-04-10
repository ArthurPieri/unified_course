# Appendix A — References

Citations for [README.md](README.md), grouped by type.

## Books

- *The Data Warehouse Toolkit* (3rd ed.), Ralph Kimball & Margy Ross, Wiley 2013 — Ch. 1 (dimensional modeling primer, four-step design), Ch. 2 (techniques reference), Ch. 3 (retail case study, bus matrix), Ch. 5 (Slowly Changing Dimensions).
- *Building the Data Warehouse* (4th ed.), W. H. Inmon, Wiley 2005 — Ch. 1 (evolution of decision-support), Ch. 2 (Corporate Information Factory), Ch. 3 (3NF enterprise layer).
- *Building a Scalable Data Warehouse with Data Vault 2.0*, Dan Linstedt & Michael Olschimke, Morgan Kaufmann 2015 — Ch. 1–2 (hub/link/satellite object types).
- *Designing Data-Intensive Applications*, Martin Kleppmann, O'Reilly 2017 — Ch. 3 (storage engines), Ch. 4 (encoding, schema-on-read vs schema-on-write), Ch. 10 (batch processing), Ch. 11 (stream processing, Lambda/Kappa context).
- *Fundamentals of Data Engineering*, Joe Reis & Matt Housley, O'Reilly 2022 — whole-lifecycle framing.

## Specifications

- [Apache Iceberg table spec](https://iceberg.apache.org/spec/) — snapshots, manifests, ACID commits.
- [Delta Lake protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md) — table format commit protocol.

## Official documentation

- [Databricks — Medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion) — Bronze/Silver/Gold pattern.
- [Apache Iceberg documentation](https://iceberg.apache.org/docs/latest/) — concurrent writer commit semantics.
- [Apache Kafka — Log compaction](https://kafka.apache.org/documentation/#compaction) — key-based retention used by Kappa-style replay.
- [Apache Kafka — Message delivery semantics](https://kafka.apache.org/documentation/#semantics) — at-most-once, at-least-once, exactly-once.

## Canonical articles

- Zhamak Dehghani, *Data Mesh Principles and Logical Architecture* — [martinfowler.com/articles/data-mesh-principles.html](https://martinfowler.com/articles/data-mesh-principles.html).
