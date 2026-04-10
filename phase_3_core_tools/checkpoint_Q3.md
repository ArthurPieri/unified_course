# Phase 3 — Checkpoint Q3 (20 questions)

Draws evenly from all eight Phase 3 modules (00–07). Pass = 16/20. Below that, re-read the module the answer key cites.

---

**Q1.** In the Phase 3 full-stack topology, which service holds the URI of an Iceberg table's current `metadata.json` file?

A) MinIO
B) Trino
C) Hive Metastore (backed by Postgres)
D) Dagster

---

**Q2.** Spark 3.5.3 on the `apache/spark:3.5.3` image is built against Scala 2.12 and Hadoop 3.3.4. The correct Iceberg runtime + `hadoop-aws` + `aws-java-sdk-bundle` trio is:

A) `iceberg-spark-runtime-3.5_2.13:1.5.2`, `hadoop-aws:3.3.6`, `aws-java-sdk-bundle:1.12.500`
B) `iceberg-spark-runtime-3.5_2.12:1.5.2`, `hadoop-aws:3.3.4`, `aws-java-sdk-bundle:1.12.262`
C) `iceberg-spark-runtime-3.4_2.12:1.4.0`, `hadoop-aws:3.3.4`, `aws-java-sdk-bundle:1.12.262`
D) `iceberg-spark-runtime-3.5_2.12:1.5.2`, `hadoop-aws:3.3.6`, `aws-java-sdk-bundle:1.12.262`

---

**Q3.** Which two S3A settings are required to talk to MinIO but are NOT needed for real AWS S3 over a default endpoint?

A) `fs.s3a.access.key` and `fs.s3a.secret.key`
B) `fs.s3a.endpoint` and `fs.s3a.path.style.access=true`
C) `fs.s3a.impl` and `fs.s3a.connection.ssl.enabled`
D) `fs.s3a.endpoint.region` and `fs.s3a.fast.upload`

---

**Q4.** Which sentence best describes MinIO's relationship to Amazon S3?

A) MinIO is an S3 client that forwards requests to AWS.
B) MinIO is an S3-compatible object store that implements the same HTTP API, so any S3 client can talk to it by overriding the endpoint.
C) MinIO replaces S3 by implementing a different protocol that is incompatible on purpose.
D) MinIO only supports the S3 Glacier subset of the API.

---

**Q5.** The correct Iceberg read order from the table root down to Parquet data files is:

A) manifest list → `metadata.json` → manifest → data file
B) `metadata.json` → manifest → manifest list → data file
C) `metadata.json` → manifest list → manifest → data file
D) manifest → data file → manifest list → `metadata.json`

---

**Q6.** Iceberg still needs an external catalog (HMS, REST, JDBC, Glue, ...) because:

A) Parquet files do not carry schemas.
B) Nothing inside the Iceberg metadata tree records "which `metadata.json` is current"; the catalog holds that pointer and is what makes commits atomic via compare-and-set.
C) MinIO cannot list a prefix without an external index.
D) The Iceberg spec requires HMS specifically.

---

**Q7.** Trino is best described as:

A) A columnar database that stores its own tables on local disk.
B) A distributed, share-nothing, in-memory SQL query engine that reads external tables through connectors and owns no storage of its own.
C) A batch ETL engine tuned for multi-hour jobs with on-disk shuffle.
D) A catalog service backed by Postgres.

---

**Q8.** `EXPLAIN ANALYZE` in Trino differs from `EXPLAIN` in that it:

A) Returns only the logical plan.
B) Executes the query and annotates each plan node with wall time, CPU time, and actual row counts.
C) Requires superuser privileges.
D) Caches the result for the next call.

---

**Q9.** A single Trino query joins `iceberg.silver.trips` with `postgres.public.zones`. This feature is called:

A) Materialized views
B) Query federation across connectors
C) Cross-catalog caching
D) Schema stitching

---

**Q10.** In the Phase 3 compose, the Spark service registers a catalog named `lakehouse` via:

A) `spark.sql.catalog.lakehouse=org.apache.iceberg.spark.SparkCatalog` with `type=hive` and `uri=thrift://hive-metastore:9083`
B) `spark.sql.warehouse.dir=s3a://lakehouse/`
C) A `CREATE CATALOG` SQL statement on startup
D) A Postgres JDBC URL in `.env`

---

**Q11.** Reach for PySpark over Trino when the workload is:

A) An interactive BI dashboard query over a small gold table.
B) A one-line `SELECT count(*)` over a Parquet file.
C) A heavy ETL transform needing Python UDFs, wide shuffles, or `MERGE INTO` rewrites of large Iceberg partitions.
D) A `CREATE VIEW` on top of an existing table.

---

**Q12.** In dlt, a `@dlt.resource` is:

A) A connection string for a destination.
B) A Python generator function that yields records for one logical table, decorated with dispositions, primary key, and column hints.
C) A YAML file that declares a source.
D) A synonym for "pipeline".

---

**Q13.** A dlt `dlt.sources.incremental("updated_at")` cursor stores its high-water-mark state in:

A) Only in memory for the lifetime of the process.
B) A local file under `~/.dlt/pipelines/<name>/` and in the destination's `_dlt_pipeline_state` table, so re-runs are idempotent.
C) An in-process SQLite database in the current directory.
D) The source system itself.

---

**Q14.** In a dbt project, `ref('stg_trips')` inside a downstream model does which of the following?

A) Imports the upstream model's SQL at parse time.
B) Creates a dependency edge in the DAG and compiles to the current environment's fully qualified table name for `stg_trips`.
C) Runs the upstream model synchronously.
D) Opens a cursor against the upstream table.

---

**Q15.** With `dbt-trino`, the default materialization for an Iceberg model can be set via a project-level config such that running `dbt run` writes a physical table in the Iceberg catalog. The materialization keyword for that is:

A) `view`
B) `ephemeral`
C) `table` (or `incremental` for append-only updates)
D) `snapshot`

---

**Q16.** A Dagster **software-defined asset** differs from an Airflow **task** because:

A) Assets are GPU-accelerated.
B) An asset declares the data object it produces (plus its upstream asset dependencies), so the DAG is derived from data lineage rather than written as task-to-task edges.
C) Assets cannot be scheduled.
D) Tasks run on Kubernetes and assets do not.

---

**Q17.** In Dagster, a **resource** and an **IO manager** are used to:

A) Configure UI themes.
B) Inject shared infrastructure (database connections, S3 clients) into assets, and to centralise how an asset's output is persisted and loaded between steps.
C) Throttle the number of concurrent runs.
D) Replace the dagster-daemon.

---

**Q18.** In Metabase, caching is configured and keyed by:

A) User ID only.
B) Instance / database / question-dashboard TTLs, keyed on the exact rendered SQL plus its parameter values; Metabase does not invalidate on upstream writes.
C) Automatic invalidation on any dbt run.
D) A single global on/off switch.

---

**Q19.** An analyst group should query the `gold` schema through the GUI builder but must not write raw SQL. In Metabase you set:

A) Collection permission to `view`
B) Data permission `No self-service` on the whole database
C) **Native query** permission to `No` for that group on the `iceberg` database (while leaving data access allowed)
D) Block the analyst's IP at the load balancer

---

**Q20.** You query `SELECT * FROM iceberg.silver.trips FOR VERSION AS OF 9127310812398` in Trino. This works because:

A) Trino keeps an internal history of every table it has ever read.
B) Each Iceberg snapshot is immutable and recorded in `metadata.json`; the Iceberg connector resolves the snapshot id and reads that specific snapshot's manifest list until the snapshot is expired.
C) HMS stores a copy of every prior row version.
D) MinIO versioning is on.

---

## Answers

| # | Ans | Source module | Primary citation |
|---|---|---|---|
| 1 | C | 00_stack_overview | [Iceberg Hive catalog](https://iceberg.apache.org/docs/latest/hive/) |
| 2 | B | 00_stack_overview | [Iceberg Spark configuration](https://iceberg.apache.org/docs/latest/spark-configuration/); [Hadoop-AWS 3.3.4](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html) |
| 3 | B | 00_stack_overview | [Hadoop S3A configuration](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html#General_S3A_Client_configuration) |
| 4 | B | 01_minio_iceberg_hms | [MinIO S3 API compatibility](https://min.io/docs/minio/linux/developers/s3-compatible-cloud-storage.html) |
| 5 | C | 01_minio_iceberg_hms | [Iceberg table spec — Overview](https://iceberg.apache.org/spec/#overview) |
| 6 | B | 01_minio_iceberg_hms | [Iceberg catalogs](https://iceberg.apache.org/concepts/catalog/); [Iceberg spec — Commit](https://iceberg.apache.org/spec/#commit) |
| 7 | B | 02_trino | [Trino concepts](https://trino.io/docs/current/overview/concepts.html); [Trino overview](https://trino.io/docs/current/overview/use-cases.html) |
| 8 | B | 02_trino | [Trino — EXPLAIN ANALYZE](https://trino.io/docs/current/sql/explain-analyze.html) |
| 9 | B | 02_trino | [Trino connectors](https://trino.io/docs/current/connector.html) |
| 10 | A | 03_pyspark | [Iceberg Spark configuration](https://iceberg.apache.org/docs/latest/spark-configuration/) |
| 11 | C | 03_pyspark | [Spark SQL guide](https://spark.apache.org/docs/3.5.3/sql-programming-guide.html); [Trino use cases](https://trino.io/docs/current/overview/use-cases.html) |
| 12 | B | 04_dlt | [dlt — Sources and resources](https://dlthub.com/docs/general-usage/source) |
| 13 | B | 04_dlt | [dlt — Incremental loading](https://dlthub.com/docs/general-usage/incremental-loading); [dlt — Pipeline state](https://dlthub.com/docs/general-usage/state) |
| 14 | B | 05_dbt | [dbt — `ref` function](https://docs.getdbt.com/reference/dbt-jinja-functions/ref) |
| 15 | C | 05_dbt | [dbt — Materializations](https://docs.getdbt.com/docs/build/materializations); [dbt-trino setup](https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup) |
| 16 | B | 06_dagster | [Dagster — Software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets) |
| 17 | B | 06_dagster | [Dagster — Resources](https://docs.dagster.io/concepts/resources); [Dagster — IO managers](https://docs.dagster.io/concepts/io-management/io-managers) |
| 18 | B | 07_metabase | [Metabase — Caching query results](https://www.metabase.com/docs/latest/configuring-metabase/caching) |
| 19 | C | 07_metabase | [Metabase — Data permissions](https://www.metabase.com/docs/latest/permissions/data) |
| 20 | B | 01_minio_iceberg_hms / 02_trino | [Trino Iceberg connector — time travel](https://trino.io/docs/current/connector/iceberg.html#time-travel-queries); [Iceberg spec — Snapshots](https://iceberg.apache.org/spec/#snapshots-and-snapshot-log) |
