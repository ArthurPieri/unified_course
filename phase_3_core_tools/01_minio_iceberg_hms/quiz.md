# Quiz — 01_minio_iceberg_hms

10 multiple-choice questions. One correct answer each. Answers and citations at the bottom.

---

**1. Which component in the Phase 3 lakehouse stack is responsible for resolving a table identifier (`db.table`) to the URI of the current `metadata.json` file?**

A. MinIO
B. Trino
C. Hive Metastore
D. The Iceberg manifest list

---

**2. You start a fresh Spark session against MinIO and every S3A call fails at DNS lookup with a hostname like `warehouse.minio:9000`. Which single setting fixes it?**

A. `spark.hadoop.fs.s3a.connection.ssl.enabled=false`
B. `spark.hadoop.fs.s3a.path.style.access=true`
C. `spark.hadoop.fs.s3a.endpoint.region=us-east-1`
D. `spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem`

---

**3. In the Iceberg on-disk layout, what is the correct read order from the table root down to a data file?**

A. manifest list → metadata.json → manifest → data file
B. metadata.json → manifest list → manifest → data file
C. metadata.json → manifest → manifest list → data file
D. manifest → metadata.json → manifest list → data file

---

**4. Why does an Iceberg table still need an external catalog, even though all schema and snapshot information is stored in `metadata.json` on the object store?**

A. Because Parquet files do not carry column statistics.
B. Because the catalog is where column-level access control is enforced.
C. Because nothing inside the Iceberg tree records "which metadata.json is current"; the catalog holds that pointer so commits can be atomic.
D. Because HMS is required by the Parquet specification.

---

**5. Which TCP port does the Hive Metastore Thrift service listen on by default, as used by the `apache/hive:4.0.1` image in the course stack?**

A. 5432
B. 8080
C. 9000
D. 9083

---

**6. How does Iceberg achieve atomic commits on top of an object store that has no multi-object transactions?**

A. It writes all data files inside a single S3 multipart upload.
B. It acquires a row-level lock in MinIO before each write.
C. It stages new data and metadata, then asks the catalog to compare-and-set its metadata pointer from the old version to the new one.
D. It relies on S3 strong consistency to order writes by wall-clock timestamp.

---

**7. Which of the following is a valid Trino time-travel query against an Iceberg table?**

A. `SELECT * FROM t AS OF SNAPSHOT 12345;`
B. `SELECT * FROM t FOR VERSION AS OF 12345;`
C. `SELECT * FROM t USING SNAPSHOT 12345;`
D. `SELECT * FROM t WITH HISTORY = 12345;`

---

**8. You never run `expire_snapshots` on a busy Iceberg table. What is the direct consequence?**

A. Time-travel queries break because the snapshot log overflows.
B. Data files referenced only by old snapshots accumulate in the object store and are never deleted, so storage grows without bound.
C. The table's schema drifts from the catalog.
D. Trino refuses to plan queries against the table.

---

**9. Your HMS container boot-loops with `schematool` errors on a brand-new environment. Which root cause matches the symptom?**

A. The Iceberg Spark runtime jar is missing from the HMS classpath.
B. Trino started before HMS and corrupted the metastore database.
C. `metastore-db` (Postgres) was not yet accepting connections, or a partial schema exists in its volume.
D. MinIO returned a 403 on the warehouse bucket during HMS startup.

---

**10. In the course full-stack compose, which command line tool is the canonical way to create the warehouse bucket in MinIO before the first `CREATE TABLE`?**

A. `aws s3 mb s3://warehouse` from the host
B. `mc mb local/warehouse` after `mc alias set`
C. `docker exec lh_hms hive -e 'CREATE BUCKET warehouse'`
D. `curl -X PUT http://localhost:9000/warehouse` with no headers

---

## Answer key

1. **C** — HMS is the catalog; it stores the pointer to the current `metadata.json` for each table. Ref: [Iceberg Hive catalog](https://iceberg.apache.org/docs/latest/hive/), [Iceberg catalogs concept](https://iceberg.apache.org/concepts/catalog/).

2. **B** — MinIO only supports path-style S3 URLs for custom endpoints; without `path.style.access=true` S3A builds a virtual-hosted hostname that cannot be resolved. Ref: [Hadoop S3A configuration](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html#General_S3A_Client_configuration), `../00_stack_overview/README.md` (S3A block).

3. **B** — Reads walk `metadata.json` → manifest list → manifest files → data files. Ref: [Iceberg table spec — Overview](https://iceberg.apache.org/spec/#overview).

4. **C** — The catalog is the only place that records which `metadata.json` is current, which is what makes atomic compare-and-set commits possible. Ref: [Iceberg catalogs concept](https://iceberg.apache.org/concepts/catalog/), [Iceberg spec — Commit](https://iceberg.apache.org/spec/#commit).

5. **D** — Hive Metastore Thrift listens on `9083`; this is mirrored in the compose block at `../../../../dataeng/docker-compose.yml:L62-L88` and in [Hive Metastore administration](https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+Administration).

6. **C** — Atomic commit is a catalog-side compare-and-set swap of the current metadata pointer. Ref: [Iceberg spec — Commit](https://iceberg.apache.org/spec/#commit).

7. **B** — Trino exposes Iceberg time travel as `FOR VERSION AS OF` or `FOR TIMESTAMP AS OF`. Ref: [Trino Iceberg connector — time travel](https://trino.io/docs/current/connector/iceberg.html#time-travel-queries).

8. **B** — Expired snapshots are what authorise deletion of orphaned data/manifest files; without expiry, storage grows monotonically. Ref: [Iceberg maintenance — expire snapshots](https://iceberg.apache.org/docs/latest/maintenance/#expire-snapshots).

9. **C** — HMS needs its backing Postgres healthy and schema-clean on first boot; the compose `depends_on: metastore-db: condition: service_healthy` exists for exactly this reason. Ref: `../../../../dataeng/docker-compose.yml:L62-L88`, [Hive Metastore 3.0 administration](https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+3.0+Administration).

10. **B** — `mc` is MinIO's canonical CLI; `mc alias set` then `mc mb local/warehouse` creates the bucket against the service in the compose network. Ref: [mc CLI reference](https://min.io/docs/minio/linux/reference/minio-mc.html), [`mc mb`](https://min.io/docs/minio/linux/reference/minio-mc/mc-mb.html).
