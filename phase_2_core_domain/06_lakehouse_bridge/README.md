# Module 06: Lakehouse Bridge — MinIO + DuckDB + Parquet (6h)

> Phase 2 closes by bridging abstract concepts (distributed storage, columnar formats, ACID tables) to the real tooling that Phase 3 will deploy (MinIO, Iceberg, Hive Metastore, Trino, Spark). This module keeps the footprint small: one container (MinIO), one in-process engine (DuckDB), one file format (Parquet). You write Parquet to object storage over the S3 API, read it back through `s3://` URLs, and understand *why* each piece is there before Phase 3 puts them behind a catalog.

## Learning goals
- Explain the three ingredients of a lakehouse (object storage, open file format, table format) and name one concrete implementation of each.
- Justify columnar storage for analytics in terms of projection and compression, citing the Parquet format spec.
- Use the S3 API against a local MinIO instance, including path-style access and the `s3_endpoint` override.
- Load the DuckDB `httpfs` extension, configure S3 credentials, and `COPY` a result set to `s3://bucket/file.parquet`.
- Query a Parquet object on MinIO directly from DuckDB without a metastore, and describe what Phase 3 adds on top (Iceberg + HMS + Trino).
- Identify why DuckDB is the right Phase 2 bridge tool (in-process, no server, native Parquet + httpfs).

## Prerequisites
- `phase_2_core_domain/01_data_modeling/` (dimensional vs. 3NF context)
- `phase_2_core_domain/03_distributed_systems/` (replication, object storage mental model)
- `phase_2_core_domain/05_streaming_concepts/` (row-oriented vs. columnar tradeoffs)
- Docker Engine installed and running; `duckdb` CLI ≥ 1.1 on PATH.

## Reading order
1. This README
2. `labs/lab_L2b_minio_duckdb/README.md`
3. `quiz.md`

## Concepts

### What is a lakehouse
A lakehouse is the composition of three layers: (1) an **object store** that holds bytes addressed by key, (2) an **open columnar file format** like Parquet that describes how those bytes encode a table, and (3) an **open table format** like Apache Iceberg that tracks which files belong to a table and provides ACID commits, schema evolution, and snapshots. Strip any layer and you lose a property: no object store → no cheap durable storage; no open format → vendor lock-in; no table format → no atomicity, no time travel.
Ref: [Iceberg table spec](https://iceberg.apache.org/spec/) · [Apache Parquet format specification](https://parquet.apache.org/docs/file-format/)

### Why Parquet is columnar
Parquet stores a table as row groups, and inside each row group it lays out values **by column** into column chunks built of pages. The spec states the format is designed to "support very efficient compression and encoding schemes" by exploiting per-column type homogeneity, and that projection queries can skip non-referenced columns entirely when reading. Analytics queries typically touch a small subset of columns over many rows, so columnar layout wins on both I/O (less bytes read) and CPU (better compression ratios, vectorizable decoding).
Ref: [Apache Parquet format — motivation and layout](https://parquet.apache.org/docs/file-format/)

### Object storage mental model
Object stores expose a flat namespace of **buckets** containing **objects** keyed by string. Keys may contain `/`, which tooling interprets as a **prefix** hierarchy, but there are no real directories — listing is a prefix scan. An object is written whole (PUT), replaced whole, or deleted; there is no in-place append. Two URL conventions exist: **virtual-hosted-style** (`https://<bucket>.s3.amazonaws.com/<key>`) and **path-style** (`https://s3.amazonaws.com/<bucket>/<key>`). Local S3-compatible servers like MinIO require path-style because they cannot wildcard-resolve DNS for arbitrary bucket subdomains by default.
Ref: [MinIO Object Management](https://min.io/docs/minio/linux/administration/object-management.html) · [MinIO — access via S3 clients](https://min.io/docs/minio/linux/integrations/aws-cli-with-minio.html)

### S3 API compatibility and MinIO
MinIO implements the Amazon S3 REST API so that any S3 client — `aws s3`, `mc`, boto3, DuckDB httpfs — can talk to it with only an endpoint and credentials changed. The MinIO docs describe the server as "API compatible with the Amazon S3 cloud storage service", which is why Phase 2 can stand up a local lake with one container and still use the same SDK calls Phase 5 will use against AWS.
Ref: [MinIO — Object Storage for AI](https://min.io/docs/minio/linux/index.html)

### Why DuckDB is the right bridge tool
DuckDB is an **in-process** OLAP database: the entire engine runs inside the caller's process, no server, no daemon, no network port. Its `httpfs` extension speaks HTTP, HTTPS, and S3, letting `SELECT ... FROM 's3://bucket/file.parquet'` and `COPY ... TO 's3://...'` work directly once S3 settings are configured with `SET s3_endpoint=...`, `SET s3_url_style='path'`, and access-key settings. For Phase 2 that means you can demonstrate lakehouse read/write mechanics without provisioning a Spark cluster, a metastore, or a query gateway — you learn the storage plumbing in isolation.
Ref: [DuckDB — httpfs extension (S3 API Support)](https://duckdb.org/docs/extensions/httpfs/s3api) · [DuckDB glossary entry](../../references/glossary.md)

### Writing Parquet from DuckDB
`COPY (query) TO 'path' (FORMAT PARQUET)` writes the result of a query to a Parquet file. When `path` starts with `s3://` and httpfs is loaded, the file goes to the configured S3 endpoint. The `PARTITION_BY` option writes a Hive-style partitioned layout (`s3://bucket/table/col=val/file.parquet`), which Phase 3 tools (Trino, Spark, Iceberg) can discover.
Ref: [DuckDB — COPY statement and Parquet writing](https://duckdb.org/docs/sql/statements/copy) · [DuckDB — Parquet files](https://duckdb.org/docs/data/parquet/overview)

### What Phase 3 adds (Iceberg + HMS + Trino)
In Phase 3 the same MinIO bucket sits behind an **Apache Iceberg** table format (metadata files + manifests tracked by the Iceberg spec), a **Hive Metastore** (HMS) that stores the pointer to the current table metadata, and **Trino** / **Spark** engines that read through the catalog instead of directly addressing Parquet files. The Phase 3 compose stack composes exactly these services; the MinIO block you use in this lab is the same one Phase 3 depends on.
Ref: [Iceberg — Getting started](https://iceberg.apache.org/docs/latest/) · [MinIO — documentation root](https://min.io/docs/minio/linux/index.html)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L2b_minio_duckdb` | Stand up MinIO, write 10k-row Parquet via DuckDB, query it back over `s3://` | 60–90m | [labs/lab_L2b_minio_duckdb/](labs/lab_L2b_minio_duckdb/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `HTTP 400 InvalidRequest` on `COPY TO s3://...` | Virtual-hosted-style URL against MinIO | `SET s3_url_style='path';` | [DuckDB httpfs S3 API](https://duckdb.org/docs/extensions/httpfs/s3api) |
| `IO Error: Connection refused` | `s3_endpoint` includes scheme (`http://`) or is missing host:port | Set bare `host:port`, then `SET s3_use_ssl=false;` | [DuckDB httpfs S3 API](https://duckdb.org/docs/extensions/httpfs/s3api) |
| `NoSuchBucket` | Bucket not created before COPY | Create with `mc mb` or MinIO console first | [MinIO mc reference](https://min.io/docs/minio/linux/reference/minio-mc.html) |
| `httpfs extension not loaded` | `INSTALL httpfs;` only installs; you must also `LOAD httpfs;` each session | Run both | [DuckDB extension loading](https://duckdb.org/docs/extensions/overview) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Name the three layers of a lakehouse and give an open-source implementation of each.
- [ ] Explain in one sentence why a columnar layout helps a `SELECT avg(price) FROM trades` query.
- [ ] Write and read a Parquet file on MinIO from DuckDB using only `httpfs` and `COPY`.
- [ ] Describe what Hive Metastore + Iceberg add on top of the MinIO+Parquet setup you just built.
