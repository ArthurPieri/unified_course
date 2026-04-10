# Quiz — Module 03: PySpark on the Lakehouse

10 multiple-choice questions. Answer key at the bottom. Every answer is grounded in the module README or a linked primary doc.

---

**Q1.** In the Phase 3 compose, why is `iceberg-spark-runtime-3.5_2.12:1.5.2` used instead of the `_2.13` artifact?

- A. The `_2.13` artifact is only published for Spark 4.x.
- B. The `apache/spark:3.5.3` image is the Scala 2.12 build, and the Iceberg runtime's Scala suffix must match.
- C. Scala 2.13 drops `DataFrame` support.
- D. Iceberg 1.5.2 is only compiled against Scala 2.12.

**Q2.** You swap `hadoop-aws:3.3.4` for `hadoop-aws:3.3.6` and leave Spark at 3.5.3. What is the most likely failure?

- A. `ClassNotFoundException: org.apache.iceberg.spark.SparkCatalog` at startup.
- B. `NoSuchMethodError` deep inside `S3AFileSystem.initialize`.
- C. Silent data corruption on writes.
- D. Spark refuses to start because the package name changed.

**Q3.** Which Spark conf is **required** for S3A to talk to MinIO but **not** needed for real AWS S3?

- A. `spark.hadoop.fs.s3a.access.key`
- B. `spark.hadoop.fs.s3a.impl`
- C. `spark.hadoop.fs.s3a.path.style.access=true`
- D. `spark.sql.extensions`

**Q4.** Spark DataFrame transformations are described as "lazy." What does that mean in practice?

- A. Each transformation immediately writes a checkpoint to disk.
- B. Transformations build a logical plan; no execution runs until an action triggers it.
- C. Only the first transformation runs; subsequent ones are skipped.
- D. The DataFrame evaluates transformations in background threads.

**Q5.** Which of these is an **action** (not a transformation)?

- A. `df.filter("amount > 0")`
- B. `df.select("pickup_hour")`
- C. `df.groupBy("pickup_hour")`
- D. `df.count()`

**Q6.** In a PySpark job that needs the Iceberg catalog, which config registers the catalog extensions?

- A. `spark.sql.catalog.lakehouse.type=hive`
- B. `spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions`
- C. `spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem`
- D. `spark.sql.catalog.lakehouse.warehouse=s3a://lakehouse/`

**Q7.** You have a 200 GB fact table and a 20 MB dimension table you want to join. Which hint is most appropriate?

- A. `dimension.repartition(200)` before the join.
- B. `broadcast(dimension)` in the join expression.
- C. `.cache()` on the fact table.
- D. `.coalesce(1)` on the fact table.

**Q8.** For a given workload, which choice is the better fit for **Spark** (rather than Trino)?

- A. An interactive BI dashboard refreshing every 30 seconds.
- B. An ad-hoc analyst `SELECT ... LIMIT 100`.
- C. A nightly ETL job with a Python UDF and a 50 GB shuffle join.
- D. A dbt model that materializes a small aggregate.

**Q9.** Which is the recommended way to run a reproducible PySpark job against the Phase 3 `spark` service?

- A. Paste code into the `pyspark` REPL each run.
- B. `docker compose exec spark spark-submit /opt/spark/work-dir/your_job.py`.
- C. Open a Jupyter kernel inside the Trino container.
- D. Copy the code into `docker-compose.yml` as an `entrypoint`.

**Q10.** After your Spark job writes `lakehouse.nyc.trips_hourly`, Trino returns `Table not found`. What should you check first?

- A. Whether Spark's executor memory is below 2g.
- B. Whether Trino's `iceberg` catalog points at the same `thrift://hive-metastore:9083` and whether the `nyc` schema was created.
- C. Whether the Parquet file has more than 100 row groups.
- D. Whether the MinIO bucket has versioning enabled.

---

## Answer key

| Q | Answer | Why |
|---|---|---|
| 1 | B | The runtime's Scala suffix must match the Spark build's Scala version; `apache/spark:3.5.3` is the 2.12 build. See [Iceberg Spark Configuration](https://iceberg.apache.org/docs/1.5.2/spark-configuration/). |
| 2 | B | Internal Hadoop APIs shift between minor versions; `S3AFileSystem.initialize` is the usual crash site. See [Hadoop-AWS 3.3.4](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html) and `../00_stack_overview/README.md`. |
| 3 | C | MinIO does not serve virtual-host style; path-style access is MinIO-specific. See [Hadoop S3A config](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html#General_S3A_Client_configuration). |
| 4 | B | Transformations build a logical plan; execution happens on an action. See [Spark SQL Guide](https://spark.apache.org/docs/3.5.3/sql-programming-guide.html). |
| 5 | D | `count()` is an action; `filter`, `select`, `groupBy` are transformations. See [PySpark DataFrame reference](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/dataframe.html). |
| 6 | B | `spark.sql.extensions=...IcebergSparkSessionExtensions` registers the catalog DDL extensions. See [Iceberg Spark Configuration](https://iceberg.apache.org/docs/1.5.2/spark-configuration/). |
| 7 | B | A 20 MB dimension fits for broadcast; it avoids shuffling the 200 GB side. See [pyspark.sql.functions.broadcast](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/api/pyspark.sql.functions.broadcast.html). |
| 8 | C | Heavy ETL with a Python UDF and a big shuffle is Spark territory; interactive SQL is Trino's. See [Spark SQL Guide](https://spark.apache.org/docs/3.5.3/sql-programming-guide.html) and [Trino use cases](https://trino.io/docs/current/overview/use-cases.html). |
| 9 | B | `spark-submit` is the reproducible entry point; the compose mounts `./notebooks` to `/opt/spark/work-dir`. See [Submitting Applications](https://spark.apache.org/docs/3.5.3/submitting-applications.html). |
| 10 | B | Table-not-found across engines is almost always a catalog-pointing or missing-namespace problem. See [Iceberg Hive catalog](https://iceberg.apache.org/docs/1.5.2/hive/) and [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html). |
