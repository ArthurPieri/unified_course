# References — 01_minio_iceberg_hms

## Apache Iceberg

- Iceberg table spec (overview + specification): https://iceberg.apache.org/spec/
- Iceberg catalogs concept: https://iceberg.apache.org/concepts/catalog/
- Iceberg Hive catalog: https://iceberg.apache.org/docs/latest/hive/
- Iceberg Spark configuration: https://iceberg.apache.org/docs/latest/spark-configuration/
- Iceberg maintenance — expire snapshots, compaction: https://iceberg.apache.org/docs/latest/maintenance/
- Iceberg releases (version matrix): https://github.com/apache/iceberg/releases

## MinIO

- MinIO S3 API compatibility: https://min.io/docs/minio/linux/developers/s3-compatible-cloud-storage.html
- MinIO object management concepts: https://min.io/docs/minio/linux/administration/object-management.html
- mc CLI reference: https://min.io/docs/minio/linux/reference/minio-mc.html
- `mc alias`: https://min.io/docs/minio/linux/reference/minio-mc/mc-alias.html
- `mc mb` (make bucket): https://min.io/docs/minio/linux/reference/minio-mc/mc-mb.html
- `mc ls`: https://min.io/docs/minio/linux/reference/minio-mc/mc-ls.html
- MinIO health probe: https://min.io/docs/minio/linux/operations/monitoring/healthcheck-probe.html
- MinIO releases: https://github.com/minio/minio/releases

## Hive Metastore

- Hive downloads + release notes: https://hive.apache.org/general/downloads/
- Metastore administration (Hive wiki): https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+Administration
- Metastore 3.0 administration (Thrift service, schematool): https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+3.0+Administration
- Apache Hive Docker image: https://hub.docker.com/r/apache/hive

## Hadoop S3A

- Hadoop S3A 3.3.4 configuration: https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html
- hadoop-aws 3.3.4 on Maven Central: https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws/3.3.4

## Trino (used by the lab)

- Trino Iceberg connector: https://trino.io/docs/current/connector/iceberg.html
- Trino Iceberg connector — time travel: https://trino.io/docs/current/connector/iceberg.html#time-travel-queries
- Trino Iceberg connector — expire_snapshots: https://trino.io/docs/current/connector/iceberg.html#expire-snapshots
- Trino CLI: https://trino.io/docs/current/client/cli.html
- Trino container install: https://trino.io/docs/current/installation/containers.html

## Compose sources (local)

- `../compose/full-stack/docker-compose.yml:L26-L44` — MinIO service block (image pin, ports, healthcheck).
- `../compose/full-stack/docker-compose.yml:L71-L98` — HMS service block (JDBC wiring, depends_on, healthcheck).
- `../compose/full-stack/docker-compose.yml:L101-L125` — Trino service block (catalog mount, depends_on HMS healthy).
- `../00_stack_overview/README.md` — topology, S3A gotchas, jar matrix.

## Books

- *Designing Data-Intensive Applications*, Kleppmann, Ch. 3 — storage engines and log-structured data (framing for object-store-backed tables).

## Course-internal

- `../../UNIFIED_COURSE_PLAN.md` — Phase 3 scope.
- `../../references/sibling_sources.md` — reuse mapping for this module.
