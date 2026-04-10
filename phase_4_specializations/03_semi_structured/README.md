# Module 03: Semi-structured and Nested Data (6h)

## Learning goals
- Explain why columnar formats (Parquet) outperform row/text formats (JSON, XML, CSV) for analytical queries, with concrete reasons tied to the Parquet file layout.
- Read and reason about Parquet **repetition** and **definition levels** well enough to interpret a nested schema's encoding.
- Distinguish **schema-on-read** from **schema-on-write** and pick the right one per pipeline stage.
- Classify schema changes (add, drop, rename, type promotion) as **safe** or **breaking** under Iceberg's evolution rules.
- Choose between keeping data **nested** versus **flattening** (UNNEST, STRUCT access) based on the query pattern, not taste.

## Prerequisites
- `../../phase_3_core_tools/01_minio_iceberg_hms/` (Iceberg table basics)
- `../../phase_3_core_tools/02_trino/` (Trino SQL, UNNEST syntax)
- `../../phase_2_core_domain/03_file_formats/` if present

## Reading order
1. This README
2. `quiz.md`

## Concepts

### Text and row formats vs Parquet
JSON, XML, and CSV are row-oriented text. A query that reads one column (`SELECT sum(amount)`) still has to parse every byte of every row — there is no per-column access, no per-column compression, and no statistics. Parquet is a **columnar** format: values for one column are stored contiguously in a **column chunk**, inside a **row group**, with per-column encoding (dictionary, RLE, bit-packing) and per-column statistics (min/max/null count) in the footer. Readers skip row groups whose statistics exclude the predicate and read only the requested columns.
Ref: [Apache Parquet — File Format](https://parquet.apache.org/docs/file-format/) · [Parquet Thrift definitions](https://github.com/apache/parquet-format/blob/master/src/main/thrift/parquet.thrift)

### Nested data: repetition and definition levels
Parquet encodes nested structures from the Dremel paper using two small integers per value: a **definition level** (how many of the optional/repeated fields in the path are actually present) and a **repetition level** (at which repeated field in the path a new list element starts). A required field needs neither; an optional field needs definition levels up to its max; a repeated field needs both. Together they losslessly reconstruct the original record from the flat column.
Ref: [Parquet — Nested Encoding](https://parquet.apache.org/docs/file-format/nested-encoding/) · [Dremel paper](https://research.google/pubs/pub36632/)

Worked example schema:
```
message Order {
  required int64 id;
  optional group customer {
    optional binary email (UTF8);
  }
  repeated group items {
    required binary sku (UTF8);
    required int32 qty;
  }
}
```
For `items.sku`, max repetition level = 1 (one repeated ancestor), max definition level = 2 (one repeated + one required below it). An order with two items yields two values with repetition levels `0, 1`; an order with zero items yields one null placeholder with definition level below max.

### Schema-on-read vs schema-on-write
**Schema-on-write** (Iceberg, Parquet with a fixed schema, relational tables) validates structure at ingest — bad rows fail fast, query engines trust the types. **Schema-on-read** (raw JSON in object storage, Hive text tables) defers interpretation to query time — ingest is flexible but every reader re-parses and re-validates, and silent drift is common.
Ref: [Iceberg — Table Spec](https://iceberg.apache.org/spec/) · *Designing Data-Intensive Applications*, Kleppmann, Ch. 4

Practical rule: keep the **landing zone** schema-on-read (append anything, debug later) and make every downstream layer schema-on-write. Contracts belong where humans query, not where machines dump.

### Schema evolution under Iceberg
Iceberg assigns every column a stable **field ID** in the schema, and Parquet files are read by ID not by name. That property is what lets rename be free and reorder be free. The [Iceberg schema evolution docs](https://iceberg.apache.org/docs/latest/evolution/#schema-evolution) list exactly what is safe:

| Change | Safe? | Notes |
|---|---|---|
| Add a new column (nullable) | Yes | Old files return null for the new ID |
| Add a column to a nested struct | Yes | Same mechanism |
| Drop a column | Yes | Field ID retired; old files ignore it |
| Rename a column | Yes | Name in schema changes, field ID unchanged |
| Reorder columns | Yes | Order is metadata, not file layout |
| Promote `int` to `long` | Yes | Widening only |
| Promote `float` to `double` | Yes | Widening only |
| Promote `decimal(P,S)` → `decimal(P',S)` where `P' >= P` | Yes | Precision widening, scale fixed |
| Narrow a type (long→int, double→float) | **No** | Data loss risk |
| Change type across families (string↔int) | **No** | Not defined |

Ref: [Iceberg — Schema Evolution](https://iceberg.apache.org/docs/latest/evolution/#schema-evolution)

Avro, by contrast, matches fields by **name plus aliases** and has its own compatibility matrix (backward, forward, full). If a pipeline mixes Avro-on-Kafka with Iceberg-on-S3, you maintain two evolution contracts, not one.
Ref: [Avro 1.11 Spec — Schema Resolution](https://avro.apache.org/docs/1.11.1/specification/#schema-resolution)

### Flattening: UNNEST and STRUCT access
Trino (and Spark SQL) lets you read nested fields two ways. Dot/bracket access projects a sub-field without materializing the parent: `SELECT customer.email FROM orders`. `UNNEST` turns an array into rows so you can join, aggregate, or filter at element granularity:
```sql
SELECT o.id, i.sku, i.qty
FROM orders o
CROSS JOIN UNNEST(o.items) AS i(sku, qty);
```
Ref: [Trino — UNNEST](https://trino.io/docs/current/sql/select.html#unnest)

### When to keep nested vs flatten
Query patterns drive the choice. If most queries touch the parent record as a whole and the array has bounded cardinality, keep it nested — Parquet stores it efficiently and you avoid a join. If queries filter or aggregate across array elements (`WHERE item.sku = ?`), pre-flatten into a child table so predicate pushdown and min/max stats actually help; an UNNEST at query time cannot use column statistics on inner fields as effectively as a flat table can.
Ref: [Parquet — Column Chunks and Statistics](https://parquet.apache.org/docs/file-format/metadata/) · [Iceberg — Partitioning](https://iceberg.apache.org/docs/latest/partitioning/)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| (none in this module) | Practice is embedded in the Phase 3 Trino/Iceberg labs | — | — |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Rename breaks downstream reads | Table engine matches by name, not ID (Hive text, Avro without alias) | Use Iceberg, or add Avro alias | [Iceberg Evolution](https://iceberg.apache.org/docs/latest/evolution/#schema-evolution) |
| `SELECT col` returns nulls after schema change | Old files written before column existed | Expected — Iceberg returns null for absent field IDs | [Iceberg Spec](https://iceberg.apache.org/spec/) |
| Slow `WHERE items.sku = 'X'` on nested array | No column stats on inner field at row-group level | Flatten items into child table, partition/sort by sku | [Parquet Metadata](https://parquet.apache.org/docs/file-format/metadata/) |
| Type promotion rejected | Attempted narrowing (long→int) | Not allowed; add a new column and backfill | [Iceberg Evolution](https://iceberg.apache.org/docs/latest/evolution/#schema-evolution) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Name three reasons Parquet beats CSV for an analytical scan, each tied to the file format.
- [ ] Given a schema with one required, one optional, and one repeated field, state the max repetition and definition levels.
- [ ] Classify `rename`, `add nullable`, `drop`, and `int→long` as safe or unsafe under Iceberg.
- [ ] Decide nested vs flattened storage for a given query workload and justify it with predicate pushdown.
