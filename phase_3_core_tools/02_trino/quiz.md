# Quiz — 02_trino

Ten multiple-choice questions. Answers at the bottom.

---

**1.** Which statement best describes Trino?

A. A columnar database with its own storage format
B. A distributed SQL query engine that reads from external sources via connectors and owns no storage
C. A batch ETL framework built on top of Spark
D. A metadata service like Hive Metastore

**2.** In the Phase 3 compose, the `trino` service runs as both coordinator and worker. Which two properties make that possible?

A. `coordinator=true` and `discovery.uri=http://worker:8080`
B. `coordinator=true` and `node-scheduler.include-coordinator=true`
C. `worker=true` and `coordinator=false`
D. `http-server.http.port=8080` alone is sufficient

**3.** Trino identifiers are three-part. What does `iceberg.silver.trips` mean?

A. database.schema.table
B. server.database.table
C. catalog.schema.table (catalog = a configured connector instance)
D. connector.catalog.table

**4.** The `iceberg` catalog is configured in `iceberg.properties` with `iceberg.catalog.type=hive_metastore` and `hive.metastore.uri=thrift://hive-metastore:9083`. What role does HMS play for Trino here?

A. It stores Iceberg data files
B. It resolves a table name to the current `metadata.json` location for the Iceberg connector
C. It authenticates Trino users
D. It caches query results

**5.** Which is a legitimate, supported use of Trino's connector model that Spark SQL cannot do as naturally?

A. Reading a Parquet file from the local disk
B. Running a `JOIN` across `iceberg.silver.trips` and `postgres.public.zones` in a single SQL statement
C. Training an ML model on an Iceberg table
D. Writing a 10 TB shuffle-heavy ETL job

**6.** You run `EXPLAIN ANALYZE` on a slow `JOIN` and see one stage with a `RemoteExchange` feeding a `HashJoin`, and that stage has 95% of the wall time. What does this tell you?

A. The table scan is the bottleneck
B. The shuffle + join stage dominates runtime; investigate that stage (skew, join strategy, build side size)
C. The coordinator is overloaded
D. HMS is slow

**7.** Where in the Trino Web UI at `:8080` do you look first when a query hangs with stages showing 0 input rows?

A. The cluster overview graph only
B. The query detail → stage view, to see which stage is blocked on splits (usually a connector issue: HMS down, S3 creds wrong)
C. The JVM thread dump
D. The audit log

**8.** What are Trino resource groups?

A. A way to configure connector plugins
B. Linux cgroups for Trino workers
C. A coordinator-side admission-control policy defining concurrency, queueing, and sharing across groups of queries
D. A JDBC-only feature

**9.** Which workload is a better fit for Trino than for Spark?

A. A nightly Python job rewriting a 5 TB Iceberg partition with heavy UDFs
B. An ML training pipeline over raw Parquet
C. Ad-hoc SQL over existing Iceberg tables for a BI dashboard, with interactive latency expectations
D. Streaming Kafka ingestion with exactly-once semantics

**10.** `SET SESSION iceberg.compression_codec = 'ZSTD'` is accepted, but `SET SESSION compression_codec = 'ZSTD'` is rejected. Why?

A. ZSTD is not supported
B. Session properties that belong to a connector must be qualified as `<catalog>.<property>`
C. The property only works in `config.properties`
D. You must quote the value differently

---

## Answer key

1. **B** — Trino is a distributed SQL engine; storage lives in connectors' underlying systems. [Trino concepts](https://trino.io/docs/current/overview/concepts.html) · [Use cases](https://trino.io/docs/current/overview/use-cases.html)
2. **B** — `coordinator=true` plus `node-scheduler.include-coordinator=true` lets one node serve both roles, as in `../compose/full-stack/conf/trino/config.properties`. [Deployment](https://trino.io/docs/current/installation/deployment.html)
3. **C** — Identifiers are `catalog.schema.table`; the catalog is a configured connector instance. [Trino concepts — catalog](https://trino.io/docs/current/overview/concepts.html#catalog)
4. **B** — The Iceberg connector asks HMS for the table's current `metadata.json` pointer, then reads the snapshot itself. [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) · [Iceberg Hive catalog](https://iceberg.apache.org/docs/latest/hive/)
5. **B** — Joining across connectors in one SQL statement is Trino's federation model. [Connectors](https://trino.io/docs/current/connector.html)
6. **B** — `EXPLAIN ANALYZE` wall time per stage points directly at the hot stage; here it is the shuffle+join. [EXPLAIN ANALYZE](https://trino.io/docs/current/sql/explain-analyze.html)
7. **B** — The stage view in the Web UI shows where splits are blocked, the signature of a connector or metadata problem. [Trino Web UI](https://trino.io/docs/current/admin/web-interface.html)
8. **C** — Resource groups are the coordinator's admission-control mechanism for concurrency, queueing, and sharing. [Resource groups](https://trino.io/docs/current/admin/resource-groups.html)
9. **C** — Interactive SQL over existing tables is Trino's sweet spot; heavy rewrites, UDFs, and streaming belong to Spark or other engines. [Trino use cases](https://trino.io/docs/current/overview/use-cases.html)
10. **B** — Connector-scoped session properties must be written as `<catalog>.<property>`. [SET SESSION](https://trino.io/docs/current/sql/set-session.html)
