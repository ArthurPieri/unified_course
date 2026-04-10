# Quiz — Module 06: Lakehouse Bridge

8 multiple-choice questions. Answer key at the bottom.

---

**Q1.** Which three layers, in order, compose a lakehouse?

A. Relational engine, SQL parser, buffer pool
B. Object storage, open file format, open table format
C. Block storage, row format, foreign-key constraints
D. Message broker, stream processor, sink

---

**Q2.** Why does Parquet's columnar layout benefit a query like `SELECT avg(price) FROM trades`?

A. It stores data pre-sorted by `price`, making averages O(1).
B. Columns are stored together, so the reader can skip non-referenced columns and decompress homogeneous-type data efficiently.
C. Parquet always keeps the entire file in memory, so column access is random.
D. The Parquet spec mandates one file per column.

---

**Q3.** In the S3 URL conventions, which style does MinIO require by default for local deployments, and which DuckDB setting enforces it?

A. Virtual-hosted-style; `SET s3_url_style='virtual';`
B. Path-style; `SET s3_url_style='path';`
C. Either works identically; no setting needed.
D. gRPC-style; `SET s3_protocol='grpc';`

---

**Q4.** You run `COPY (SELECT * FROM t) TO 's3://bkt/t.parquet' (FORMAT PARQUET);` in DuckDB and get `IO Error: Connection refused`. Which single fix is most likely correct?

A. Rebuild DuckDB from source.
B. Set `s3_endpoint` to `host:port` without a scheme, and `SET s3_use_ssl=false;` for local HTTP MinIO.
C. Use `FORMAT CSV` instead.
D. Add `PARTITION_BY (id)` to the COPY statement.

---

**Q5.** Which statement about DuckDB best explains why it is the right Phase 2 bridge tool?

A. It runs as a distributed cluster, matching Phase 3's Trino topology.
B. It is an in-process OLAP engine requiring no server, and its `httpfs` extension reads Parquet directly from S3-compatible endpoints.
C. It replaces the need for Iceberg in production.
D. It is a row-oriented OLTP store optimized for writes.

---

**Q6.** What does Apache Iceberg add on top of "MinIO + Parquet files"?

A. Compression for Parquet.
B. A fourth file format for row-oriented data.
C. An open table format: atomic commits, schema evolution, snapshots, and a manifest of which files belong to the table.
D. An S3-compatible API.

---

**Q7.** In the DuckDB httpfs extension, which two commands must both run in a session to use S3 URLs, given the extension is already installed?

A. `INSTALL httpfs;` then `ENABLE httpfs;`
B. `LOAD httpfs;` then `SET s3_region='us-east-1';` only
C. `INSTALL httpfs;` is sufficient across all sessions
D. `LOAD httpfs;` then configure `s3_endpoint` / credentials via `SET`

---

**Q8.** Which Phase 3 components are *not* present in this module's minimal lab, and what role do they add?

A. Hive Metastore and Iceberg/Trino — they add a catalog and a query engine that read through table metadata instead of raw file paths.
B. PostgreSQL and Kafka — they add OLTP and streaming.
C. Airflow and dbt — they add scheduling and transformation.
D. Prometheus and Grafana — they add metrics and dashboards.

---

## Answer key

1. **B** — Object storage + open file format + open table format. See module §"What is a lakehouse".
2. **B** — Columnar layout enables projection pushdown and per-column compression (Parquet spec, "file format" page).
3. **B** — MinIO requires path-style; DuckDB exposes `s3_url_style='path'` (DuckDB httpfs S3 API docs).
4. **B** — `s3_endpoint` is bare `host:port`; disable SSL for local HTTP MinIO (DuckDB httpfs S3 API docs).
5. **B** — In-process OLAP + httpfs S3 support (DuckDB docs).
6. **C** — Iceberg is an open *table* format adding ACID, snapshots, schema evolution on top of file formats (Iceberg spec).
7. **D** — `LOAD httpfs;` is per-session; then configure `s3_endpoint` and credentials via `SET` (DuckDB extensions + httpfs docs).
8. **A** — HMS + Iceberg + Trino/Spark are the Phase 3 additions the module explicitly points forward to.
