# Module 03: PySpark on the Lakehouse (8h)

> **GAP module.** No sibling PySpark source exists in `../dataeng/` (confirmed via `references/sibling_sources.md` — row: "Phase 3 · 03_pyspark → GAP"). The `../azure_certified/labs/02-spark-transformations.ipynb` is Databricks-tied notebook infra and is not reused. Content below is written from primary docs only: `spark.apache.org/docs/3.5.3/` and `iceberg.apache.org/docs/1.5.2/`, per `docs/REUSE_POLICY.md`.

## Learning goals

- Start a `SparkSession` wired to the Phase 3 Hive Metastore Iceberg catalog and MinIO over S3A.
- Explain the Scala-2.12 / `hadoop-aws:3.3.4` / `aws-java-sdk-bundle:1.12.262` version trio and diagnose a mismatch from the stack trace.
- Read Parquet from `s3a://` into a DataFrame and write it to an Iceberg table via `write.format("iceberg")`.
- Choose between `spark-submit`, the PySpark shell, and a notebook for a given task.
- State one rule of thumb for when to reach for Spark instead of Trino.

## Prerequisites

- `../00_stack_overview/` (especially the "Spark-Iceberg jar gotchas" section)
- `../01_minio_iceberg_hms/` (HMS + MinIO + Iceberg concepts)
- `../02_trino/` (you will SELECT the lab output from Trino)

## Reading order

1. This README
2. `labs/lab_L3e_pyspark_nyc_taxi/README.md`
3. `quiz.md`

## Concepts

### Why Spark for data engineering

Spark is a distributed DataFrame engine: one program runs across many executors, each holding a partition of the data. The DataFrame API is **lazy** — transformations (`filter`, `select`, `groupBy`) build a logical plan, and nothing runs until an action (`count`, `write`, `show`) triggers it. The **Catalyst optimizer** rewrites that plan (predicate pushdown, column pruning, constant folding), and **whole-stage code generation** compiles the physical plan into JVM bytecode to cut per-row overhead. You do not need to know the internals to use Spark, but knowing the plan is lazy prevents surprising re-computation.
Ref: [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/3.5.3/sql-programming-guide.html), [PySpark Quickstart: DataFrame](https://spark.apache.org/docs/3.5.3/api/python/getting_started/quickstart_df.html).

### Building a SparkSession for the lakehouse

In the Phase 3 compose, the `spark` service launches with `--packages` that pull the Iceberg runtime and `hadoop-aws` jars, plus Spark conf flags that register the `lakehouse` catalog. In Python code inside a `spark-submit` job, you still create a `SparkSession` with `SparkSession.builder.appName("...").getOrCreate()`; the session inherits the conf passed on the command line. The catalog block looks like:

```
spark.sql.extensions                            = org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
spark.sql.catalog.lakehouse                     = org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.lakehouse.type                = hive
spark.sql.catalog.lakehouse.uri                 = thrift://hive-metastore:9083
spark.sql.catalog.lakehouse.warehouse           = s3a://lakehouse/
spark.hadoop.fs.s3a.endpoint                    = http://minio:9000
spark.hadoop.fs.s3a.path.style.access           = true
spark.hadoop.fs.s3a.access.key                  = <minio user>
spark.hadoop.fs.s3a.secret.key                  = <minio pass>
```

`lakehouse` is an arbitrary catalog name; tables are then addressed as `lakehouse.<db>.<table>`.
Ref: [Iceberg — Spark Configuration](https://iceberg.apache.org/docs/1.5.2/spark-configuration/), [Spark Configuration — Application Properties](https://spark.apache.org/docs/3.5.3/configuration.html#application-properties), [Hadoop-AWS S3A configuration](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html#General_S3A_Client_configuration).

### The jar version trap

Three jars must line up, and every one has a common failure mode. `iceberg-spark-runtime-3.5_2.12:1.5.2` is the Iceberg runtime compiled for Spark 3.5 on Scala **2.12**. The `apache/spark:3.5.3` image is the 2.12 build, so `_2.12` is correct; the `_2.13` artifact will raise `NoClassDefFoundError` or `NoSuchMethodError` the first time the catalog extension loads. `hadoop-aws:3.3.4` must equal the Hadoop version Spark 3.5.x was compiled against — mismatching to `3.3.6` breaks internal APIs inside `S3AFileSystem.initialize`. `aws-java-sdk-bundle:1.12.262` is the exact SDK version listed on the `hadoop-aws:3.3.4` dependency page; bumping only the SDK tends to produce `NoSuchMethodError: com.amazonaws.services.s3.model...`. Pin all three together, upgrade them together.
Refs: [Iceberg — Spark Configuration](https://iceberg.apache.org/docs/1.5.2/spark-configuration/), [Hadoop-AWS 3.3.4 module docs](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html), `../00_stack_overview/README.md` (Spark-Iceberg jar gotchas section).

### Core DataFrame operations

Reading Parquet from MinIO is one call: `df = spark.read.parquet("s3a://lakehouse/raw/yellow_tripdata_2024-01.parquet")`. Writing an Iceberg table is one call: `df.writeTo("lakehouse.nyc.trips_hourly").createOrReplace()` (DataFrameWriterV2 API, preferred for catalog tables) or `df.write.format("iceberg").mode("append").save("lakehouse.nyc.trips_hourly")`. To mix SQL and DataFrame, register a temp view with `df.createOrReplaceTempView("trips")` and then `spark.sql("SELECT ... FROM trips")` returns a new DataFrame. Iceberg DDL (`CREATE TABLE`, `MERGE INTO`, `DELETE FROM`) also runs via `spark.sql(...)` once the catalog extensions are loaded.
Refs: [PySpark — DataFrame API](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/dataframe.html), [Iceberg — Spark Writes](https://iceberg.apache.org/docs/1.5.2/spark-writes/), [Iceberg — Spark DDL](https://iceberg.apache.org/docs/1.5.2/spark-ddl/), [Iceberg — Spark Queries](https://iceberg.apache.org/docs/1.5.2/spark-queries/).

### Partitioning and broadcast joins

`df.write.partitionBy("pickup_date")` tells Spark to write one file set per date, which limits per-query scan. This is the Spark-level partitioning and is distinct from Iceberg's hidden partitioning (covered in Phase 4). A **broadcast join** tells Spark to ship the smaller table to every executor instead of shuffling both sides: `from pyspark.sql.functions import broadcast; large.join(broadcast(small), "key")`. Use it when the small side fits in driver/executor memory (tens of MB). Deeper tuning — skew handling, AQE, file sizing — is Phase 4.
Refs: [Spark SQL Guide — Partitioning](https://spark.apache.org/docs/3.5.3/sql-data-sources-parquet.html#partition-discovery), [Spark SQL Functions — broadcast](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/api/pyspark.sql.functions.broadcast.html).

### spark-submit, shell, notebook

`spark-submit your_job.py` is the production entry point: Spark wires the packages and confs, starts a driver, runs your script to completion, and exits. The **PySpark shell** (`pyspark`) gives you an interactive REPL with a live `spark` session — good for exploration, not for reproducible work. A **notebook** (Jupyter with a PySpark kernel) is a middle ground; the Phase 3 compose does not ship one, and the module stays command-line only. In the lab below, you run `docker compose exec spark spark-submit ...` against the running `spark` service.
Ref: [Submitting Applications](https://spark.apache.org/docs/3.5.3/submitting-applications.html).

### Spark vs Trino

Reach for **Trino** when the query is interactive SQL over well-shaped tables: a BI dashboard, an ad-hoc `SELECT`, a dbt model. Reach for **Spark** when the work is heavy ETL, when you need Python UDFs, when joins span tens of GB and require shuffle-aware execution, or when you write back with MERGE semantics over a whole partition. The Phase 3 compose runs both so you can feel the difference: the same `trips_hourly` table in the lab below is written by Spark and read by Trino.
Refs: [Spark SQL Guide](https://spark.apache.org/docs/3.5.3/sql-programming-guide.html), [Trino overview](https://trino.io/docs/current/overview/use-cases.html).

## Labs

| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L3e_pyspark_nyc_taxi` | spark-submit a PySpark job that reads NYC taxi Parquet from MinIO, writes a per-hour Iceberg table, and SELECTs it from Trino | 60m | [labs/lab_L3e_pyspark_nyc_taxi/](labs/lab_L3e_pyspark_nyc_taxi/) |

## Common failures

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `NoClassDefFoundError` from `IcebergSparkSessionExtensions` | Scala 2.13 artifact on a 2.12 Spark image | Use `iceberg-spark-runtime-3.5_2.12:1.5.2` | [Iceberg Spark Config](https://iceberg.apache.org/docs/1.5.2/spark-configuration/) |
| `NoSuchMethodError` in `S3AFileSystem.initialize` | `hadoop-aws` version ≠ Spark's bundled Hadoop | Pin `hadoop-aws:3.3.4` with Spark 3.5.3 | [Hadoop-AWS 3.3.4](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html) |
| `NoSuchMethodError: com.amazonaws.services.s3.model...` | SDK upgraded without matching `hadoop-aws` | Pin `aws-java-sdk-bundle:1.12.262` with `hadoop-aws:3.3.4` | [Hadoop-AWS 3.3.4](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html) |
| S3A resolves `http://bucket.minio:9000/...` and DNS fails | Missing virtual-host override | `spark.hadoop.fs.s3a.path.style.access=true` | [Hadoop S3A config](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html#General_S3A_Client_configuration) |
| `UnknownHostException: s3.amazonaws.com` | Endpoint not overridden | `spark.hadoop.fs.s3a.endpoint=http://minio:9000` | [Hadoop S3A config](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html) |
| `Table not found: lakehouse.nyc.trips_hourly` in Trino after Spark write | Trino `iceberg` catalog points at a different HMS, or namespace not created | Verify both engines use `thrift://hive-metastore:9083`; `CREATE SCHEMA IF NOT EXISTS lakehouse.nyc` first | [Iceberg Hive catalog](https://iceberg.apache.org/docs/1.5.2/hive/) |

## References

See [references.md](./references.md).

## Checkpoint

Before moving on, you can:

- [ ] Build a `SparkSession` that can read `s3a://lakehouse/...` and write to `lakehouse.<db>.<tbl>`.
- [ ] Recite the three pinned jar versions and the failure mode each one guards against.
- [ ] Run `spark-submit` against the Phase 3 compose, confirm the Iceberg write via a Trino `SELECT`, and explain each conf flag the job depends on.
- [ ] State one scenario where Spark is the right tool and one where Trino is.
