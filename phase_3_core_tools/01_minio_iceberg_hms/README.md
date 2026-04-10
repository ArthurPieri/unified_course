# Module 01: MinIO + Iceberg + Hive Metastore (6h)

> The three pieces that make a lakehouse a lakehouse: an object store for bytes, a table format for transactional tables on top of files, and a catalog that tells engines where the tables live. This module wires those three together against the stack defined in `../compose/full-stack/docker-compose.yml` and builds the mental model you need before adding Trino, Spark, or dbt on top.

## Learning goals
- Name the three layers of the lakehouse (object store, table format, catalog) and state which responsibility each one owns.
- Configure an S3A client for MinIO: endpoint override, path-style access, and credentials.
- Read the Iceberg metadata chain (`metadata.json` → manifest list → manifest files → data files) in a live bucket and explain what each file carries.
- Explain why an Iceberg table still needs an external catalog, and what HMS stores on its behalf.
- Run time-travel queries with `VERSION AS OF` / `TIMESTAMP AS OF` and expire snapshots.
- Diagnose the four most common bring-up failures (wrong S3 endpoint, missing bucket, Scala-version mismatch, HMS schema not initialised).

## Prerequisites
- `../../phase_1_foundations/04_docker/` — Compose services, healthchecks, `.env` secrets.
- `../00_stack_overview/` — topology, Spark/Iceberg jar matrix, S3A gotchas.
- `../../phase_2_core_domain/06_lakehouse_bridge/` — Parquet + Iceberg concepts at the file level.

## Reading order
1. This README
2. [labs/lab_L3a_stack_up/README.md](labs/lab_L3a_stack_up/README.md)
3. [quiz.md](quiz.md)

## Concepts

### The three-layer lakehouse
A lakehouse separates three concerns that monolithic warehouses fuse together. The **object store** (MinIO here, S3 in production) holds immutable byte sequences under keys; it knows nothing about schemas or transactions. The **table format** (Apache Iceberg) is a specification that layers a tree of JSON and Avro metadata on top of Parquet data files so that a set of objects becomes a table with schema, partitioning, snapshots, and ACID semantics. The **catalog** (Hive Metastore) is a small service that resolves a table identifier (`db.table`) to the current root metadata file and lets multiple engines agree on what "current" means. Ref: [Iceberg table spec — Overview](https://iceberg.apache.org/spec/), [Iceberg Hive catalog](https://iceberg.apache.org/docs/latest/hive/), `../00_stack_overview/README.md`.

### MinIO as an S3 endpoint
MinIO implements the Amazon S3 API so any S3 client — the AWS SDK, `mc`, Hadoop S3A, the Iceberg `S3FileIO` — can talk to it by overriding the endpoint. Ref: [MinIO S3 API compatibility](https://min.io/docs/minio/linux/developers/s3-compatible-cloud-storage.html). The service block we use is pinned at `../../../../dataeng/docker-compose.yml:L26-L43` and mirrored at `../compose/full-stack/docker-compose.yml:L26-L44`: console on `:9001`, S3 API on `:9000`, a healthcheck hitting `/minio/health/live` (Ref: [MinIO healthcheck probe](https://min.io/docs/minio/linux/operations/monitoring/healthcheck-probe.html)). The `mc` CLI is the canonical admin tool — `mc alias set`, `mc mb`, `mc ls`, `mc cp` — and is how we create buckets and inspect objects in the lab. Ref: [mc CLI reference](https://min.io/docs/minio/linux/reference/minio-mc.html).

### Path-style vs virtual-hosted S3 access
Real S3 supports two URL forms: virtual-hosted (`https://bucket.s3.amazonaws.com/key`) and path-style (`https://s3.amazonaws.com/bucket/key`). MinIO only supports the path-style form for custom endpoints, because there is no wildcard DNS to resolve `bucket.minio`. Every S3A client therefore needs `fs.s3a.path.style.access=true` plus `fs.s3a.endpoint=http://minio:9000` plus credentials, or the bucket lookup fails at DNS time before any S3 request is made. Ref: [Hadoop S3A configuration](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html#General_S3A_Client_configuration), `../00_stack_overview/README.md` (S3A block).

### Iceberg metadata layout
Iceberg's on-disk layout is a tree, and every write produces a new root. At the top sits **`metadata.json`** — the table metadata file — which records schema, partition spec, snapshot history, and a pointer to the current snapshot. Each **snapshot** points to a **manifest list** (Avro), which lists **manifest files** (also Avro), each of which lists **data files** (Parquet/ORC/Avro) with their statistics and partition values. A read walks root → manifest list → manifests → data files, prunes by partition and column stats, and only then opens Parquet. A write produces new data files, new manifests, a new manifest list, and a new `metadata.json`; the commit is a single atomic swap of the catalog's pointer to the new metadata file. Ref: [Iceberg table spec — Overview](https://iceberg.apache.org/spec/#overview), [Iceberg spec — Specification](https://iceberg.apache.org/spec/#specification).

### Why Iceberg still needs a catalog
Nothing in the Iceberg tree tells you "where is the current metadata.json?". That pointer lives outside the tree, in a catalog. Without a catalog, two writers racing against the same table cannot agree on which `metadata.json` is the latest, and atomic commits become impossible. Iceberg supports several catalog implementations (REST, JDBC, Hive, Glue, Nessie); we use **Hive Metastore** because it is the reference catalog that every engine in Phase 3 already speaks. Ref: [Iceberg catalogs](https://iceberg.apache.org/concepts/catalog/), [Iceberg Hive catalog](https://iceberg.apache.org/docs/latest/hive/).

### Hive Metastore as a registry
HMS is a Thrift service — by default on TCP `9083` — backed by a relational database (Postgres in our stack). It stores namespaces (`databases`), tables, and for Iceberg tables the URI of the current metadata pointer; it does not store column data. The service must have its schema initialised in the backing DB before it accepts connections; the `apache/hive:4.0.1` image runs `schematool` on first start when `SERVICE_NAME=metastore`. Ref: [Hive Metastore administration](https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+Administration), [Hive Metastore admin — Thrift service](https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+3.0+Administration). The service block in our stack at `../../../../dataeng/docker-compose.yml:L62-L88` wires HMS to `metastore-db` via JDBC and waits for both `metastore-db` and `minio` to be healthy before starting.

### ACID via atomic pointer swap
Iceberg gets ACID on an object store that has none by making the catalog's metadata pointer the single linearisation point. A writer stages new data files and new metadata, then asks the catalog to swap the current pointer from the old `metadata.json` to the new one using an atomic compare-and-set against the previous version. If two writers try to swap from the same base version, one succeeds and the other retries against the new base. Ref: [Iceberg spec — Commit](https://iceberg.apache.org/spec/#commit), *Designing Data-Intensive Applications*, Kleppmann, Ch. 3 (for the object-storage framing).

### Time travel
Because each snapshot is immutable and the history is recorded in `metadata.json`, any past snapshot is still queryable until it is expired. Trino and Spark expose this as `SELECT ... FROM t FOR VERSION AS OF <snapshot-id>` and `FOR TIMESTAMP AS OF <ts>`. Ref: [Trino Iceberg connector — time travel](https://trino.io/docs/current/connector/iceberg.html#time-travel-queries), [Iceberg spec — Snapshots](https://iceberg.apache.org/spec/#snapshots-and-snapshot-log).

### Snapshot expiry
Snapshots are retained forever by default, so every insert/update adds garbage that can never be collected. The `expire_snapshots` procedure drops snapshots older than a retention window and deletes the data and manifest files that no live snapshot references. Run it on a schedule or your bucket grows monotonically. Ref: [Iceberg — maintenance, expireSnapshots](https://iceberg.apache.org/docs/latest/maintenance/#expire-snapshots), [Trino Iceberg — expire_snapshots](https://trino.io/docs/current/connector/iceberg.html#expire-snapshots).

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L3a_stack_up` | Bring up MinIO + HMS + Trino, create a warehouse bucket, register a namespace, CREATE/INSERT/SELECT an Iceberg table, inspect the metadata tree in MinIO, tear down | 60m | [labs/lab_L3a_stack_up/](labs/lab_L3a_stack_up/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| S3A resolves `http://warehouse.minio:9000/...` and fails DNS | `fs.s3a.path.style.access` not set | Set `path.style.access=true` and keep the endpoint override | [Hadoop S3A](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html#General_S3A_Client_configuration) |
| `CREATE TABLE` fails with `Bucket warehouse does not exist` | Warehouse bucket was never created in MinIO | `mc mb local/warehouse` before the first CREATE | [mc CLI](https://min.io/docs/minio/linux/reference/minio-mc.html) |
| `NoClassDefFoundError` at Iceberg extension load | Scala 2.12 Spark image paired with `_2.13` Iceberg runtime | Use `iceberg-spark-runtime-3.5_2.12` with the 2.12 Spark image | [Iceberg Spark config](https://iceberg.apache.org/docs/latest/spark-configuration/) |
| HMS container boot-loops `schematool` | Postgres not ready when HMS started, or volume had partial schema | Wait for `metastore-db` healthy; on a reset, `docker compose down -v` and restart | `../../../../dataeng/docker-compose.yml:L62-L88` |
| Trino `iceberg` catalog: `Failed to connect to HMS` | HMS still in `starting`; `start_period` not elapsed | Wait until `docker compose ps` shows HMS `healthy`; read HMS logs | [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Draw the three layers (object store / table format / catalog) and name the service that implements each in our stack.
- [ ] Walk the Iceberg metadata tree from `metadata.json` to a data file and explain what each hop carries.
- [ ] Configure a fresh S3A client to talk to MinIO without re-reading the docs.
- [ ] Explain how Iceberg achieves atomic commits on an eventually-consistent object store.
- [ ] Run a time-travel query and an `expire_snapshots` call, and say which files get deleted.
