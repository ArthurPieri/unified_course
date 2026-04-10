# Module 03 Quiz — Semi-structured and Nested Data

Eight multiple-choice questions. Answer key at the bottom.

---

**1.** A query reads one column out of a 200-column table with 10 billion rows. Which Parquet feature most directly reduces bytes read from disk?

A. Snappy compression of the whole file
B. Column chunks inside row groups let readers fetch only the requested column
C. The Thrift footer
D. Dictionary encoding of string values

**2.** In Parquet's nested encoding, what does the **repetition level** of a value tell you?

A. How many times the value has been updated
B. Which ancestor repeated field a new list element starts at
C. How deeply the value is nested in structs
D. Whether the value is null

**3.** Given the schema `required int64 id; optional group c { optional binary email; }`, what is the max definition level of `c.email`?

A. 0
B. 1
C. 2
D. 3

**4.** Which evolution change is **not** safe under Iceberg's rules?

A. Rename `customer_name` to `name`
B. Add a nullable `region` column
C. Promote `int` to `long`
D. Narrow `long` to `int`

**5.** Why can Iceberg rename a column without rewriting any data files?

A. It rewrites files lazily in the background
B. Parquet files store column names as comments only
C. Iceberg matches columns by stable field ID, not by name
D. Hive Metastore caches the old name

**6.** When is **schema-on-read** the appropriate choice?

A. The gold reporting layer consumed by BI tools
B. A raw landing zone where anything may arrive and be inspected later
C. A dimensional model with enforced foreign keys
D. A Kafka topic with a published Avro contract

**7.** A workload frequently filters `WHERE items.sku = 'X'` on a nested array column. Which storage design best exploits predicate pushdown?

A. Keep items nested; rely on UNNEST at query time
B. Store items as a JSON string column
C. Flatten items into a child table partitioned/sorted by `sku`
D. Drop the items column and join from the source system

**8.** In Trino, which statement correctly turns `orders.items` (array of struct) into row-level data for joining?

A. `SELECT items.* FROM orders`
B. `SELECT o.id, i.sku FROM orders o CROSS JOIN UNNEST(o.items) AS i(sku, qty)`
C. `SELECT EXPLODE(items) FROM orders`
D. `SELECT o.id, FLATTEN(o.items) FROM orders o`

---

## Answer key

1. **B** — columnar layout is the primary reason a single-column scan is cheap; compression and dictionary encoding help but are secondary. Ref: Parquet File Format.
2. **B** — repetition level marks where a new element of a repeated field begins. Ref: Parquet Nested Encoding.
3. **C** — one optional group + one optional leaf = max definition level 2. Ref: Parquet Nested Encoding.
4. **D** — narrowing is explicitly unsafe; widening, rename, add-nullable are safe. Ref: Iceberg Schema Evolution.
5. **C** — Iceberg assigns stable field IDs and Parquet reads by ID. Ref: Iceberg Spec / Schema Evolution.
6. **B** — landing zones benefit from deferred interpretation; downstream layers should be schema-on-write. Ref: DDIA Ch. 4.
7. **C** — flattening + sort/partition lets row-group statistics prune by `sku`; UNNEST at query time cannot. Ref: Parquet Metadata, Iceberg Partitioning.
8. **B** — `CROSS JOIN UNNEST(array) AS alias(col, ...)` is the Trino syntax. Ref: Trino UNNEST docs.
