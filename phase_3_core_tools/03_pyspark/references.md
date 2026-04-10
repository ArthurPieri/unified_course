# References — Module 03: PySpark on the Lakehouse

Primary-doc only (GAP module, no sibling reuse). Versions match the Phase 3 compose: Spark 3.5.3, Iceberg 1.5.2, Hadoop 3.3.4.

## Apache Spark 3.5.3

- [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/3.5.3/sql-programming-guide.html) — lazy evaluation, Catalyst, DataFrame API overview.
- [PySpark Quickstart: DataFrame](https://spark.apache.org/docs/3.5.3/api/python/getting_started/quickstart_df.html) — introductory `SparkSession` + DataFrame ops.
- [PySpark — DataFrame API reference](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/dataframe.html) — `read`, `write`, `writeTo`, `createOrReplaceTempView`.
- [PySpark SQL Functions — broadcast](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/api/pyspark.sql.functions.broadcast.html) — broadcast join hint.
- [Spark Configuration — Application Properties](https://spark.apache.org/docs/3.5.3/configuration.html#application-properties) — driver/executor memory, `spark.sql.*`, `spark.hadoop.*`.
- [Submitting Applications](https://spark.apache.org/docs/3.5.3/submitting-applications.html) — `spark-submit`, `--packages`, `--conf`.
- [Spark SQL — Parquet partition discovery](https://spark.apache.org/docs/3.5.3/sql-data-sources-parquet.html#partition-discovery) — `partitionBy` and directory layout.
- [Spark Tuning Guide — Memory Tuning](https://spark.apache.org/docs/3.5.3/tuning.html#memory-tuning) — OOM triage.

## Apache Iceberg 1.5.2

- [Iceberg — Spark Configuration](https://iceberg.apache.org/docs/1.5.2/spark-configuration/) — `spark.sql.catalog.*`, Scala 2.12/2.13 runtime artifacts.
- [Iceberg — Spark DDL](https://iceberg.apache.org/docs/1.5.2/spark-ddl/) — `CREATE TABLE`, `CREATE SCHEMA`.
- [Iceberg — Spark Writes](https://iceberg.apache.org/docs/1.5.2/spark-writes/) — `writeTo`, append vs overwrite, MERGE.
- [Iceberg — Spark Queries](https://iceberg.apache.org/docs/1.5.2/spark-queries/) — reading Iceberg tables, time travel.
- [Iceberg — Hive catalog](https://iceberg.apache.org/docs/1.5.2/hive/) — HMS as Iceberg catalog backend.

## Hadoop 3.3.4 (S3A)

- [Hadoop-AWS module — Hadoop 3.3.4](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html) — S3A endpoint, path-style access, credentials, paired SDK version.

## Trino (for verification step)

- [Trino — Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) — catalog config, HMS wiring, `SELECT` against Iceberg tables.
- [Trino — Use cases / overview](https://trino.io/docs/current/overview/use-cases.html) — interactive SQL positioning (Spark-vs-Trino boundary).

## Local sibling files (for infra context, not content reuse)

- `../00_stack_overview/README.md` — Spark-Iceberg jar gotchas section (version matrix rationale).
- `../compose/full-stack/docker-compose.yml` — Spark service block with the exact `--packages` and `--conf` flags this module cites.
