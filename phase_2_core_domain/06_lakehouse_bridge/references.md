# References — Module 06: Lakehouse Bridge

## Primary docs
- [Apache Parquet — file format specification](https://parquet.apache.org/docs/file-format/) — columnar layout, row groups, column chunks, pages, encoding goals.
- [Apache Iceberg — table spec](https://iceberg.apache.org/spec/) — open table format: metadata, manifests, snapshots, ACID commits. Phase 3 context.
- [Apache Iceberg — Getting started](https://iceberg.apache.org/docs/latest/) — mention-only for the Phase 3 bridge.
- [DuckDB — httpfs extension (S3 API Support)](https://duckdb.org/docs/extensions/httpfs/s3api) — `s3_endpoint`, `s3_url_style`, `s3_use_ssl`, `s3_access_key_id`, `s3_secret_access_key`; reading/writing `s3://` URLs.
- [DuckDB — COPY statement](https://duckdb.org/docs/sql/statements/copy) — `COPY (query) TO 'path' (FORMAT PARQUET, PARTITION_BY (...))`.
- [DuckDB — Parquet files](https://duckdb.org/docs/data/parquet/overview) — reading and writing Parquet, predicate/projection pushdown.
- [DuckDB — Extensions overview](https://duckdb.org/docs/extensions/overview) — `INSTALL` vs `LOAD` semantics.
- [DuckDB — docs root](https://duckdb.org/docs/) — in-process OLAP engine description.
- [MinIO — documentation root](https://min.io/docs/minio/linux/index.html) — S3 API compatibility statement.
- [MinIO — object management](https://min.io/docs/minio/linux/administration/object-management.html) — buckets, prefixes, object lifecycle.
- [MinIO — mc client reference](https://min.io/docs/minio/linux/reference/minio-mc.html) — `mc alias set`, `mc mb`.
- [MinIO — using AWS CLI with MinIO](https://min.io/docs/minio/linux/integrations/aws-cli-with-minio.html) — path-style endpoint configuration for S3 clients.

## Compose patterns (based on the companion lakehouse project)
- Canonical MinIO service block this module's compose file is adapted from (image pin, console port, env vars, healthcheck pattern). See [MinIO — documentation root](https://min.io/docs/minio/linux/index.html).
- `../../references/glossary.md` — entries for Parquet, Iceberg, Lakehouse, DuckDB.
- `../../references/sibling_sources.md:L192` — sibling mapping for Phase 2 · 06_lakehouse_bridge → duckdb.org/docs.

## Books
- *Fundamentals of Data Engineering*, Reis & Housley — lakehouse architecture chapter (storage abstraction, open formats).
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 3 — column-oriented storage motivation.
