# Module 03 References

## Specifications
- [Apache Parquet — File Format](https://parquet.apache.org/docs/file-format/) — row groups, column chunks, page layout, footer.
- [Apache Parquet — Nested Encoding](https://parquet.apache.org/docs/file-format/nested-encoding/) — definition and repetition levels, worked examples.
- [Apache Parquet — Metadata and Statistics](https://parquet.apache.org/docs/file-format/metadata/) — per-column min/max/null stats used by predicate pushdown.
- [Parquet Thrift definitions (parquet.thrift)](https://github.com/apache/parquet-format/blob/master/src/main/thrift/parquet.thrift) — canonical on-disk structures.
- [Dremel: Interactive Analysis of Web-Scale Datasets](https://research.google/pubs/pub36632/) — Melnik et al., origin of the repetition/definition level encoding Parquet uses.
- [Apache Avro 1.11.1 Specification — Schema Resolution](https://avro.apache.org/docs/1.11.1/specification/#schema-resolution) — Avro's name-plus-alias matching and compatibility rules.

## Iceberg docs
- [Iceberg — Table Spec](https://iceberg.apache.org/spec/) — field IDs, snapshots, manifest layout.
- [Iceberg — Schema Evolution](https://iceberg.apache.org/docs/latest/evolution/#schema-evolution) — safe vs unsafe changes, type promotion matrix.
- [Iceberg — Partitioning and Hidden Partitioning](https://iceberg.apache.org/docs/latest/partitioning/) — how partition transforms interact with column stats.

## Query engines
- [Trino — UNNEST in SELECT](https://trino.io/docs/current/sql/select.html#unnest) — flattening arrays to rows.
- [Trino — Row and Array type operators](https://trino.io/docs/current/functions/array.html) — struct/dot access, array functions.

## Book
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 4 — schema-on-read vs schema-on-write, evolution formats.
