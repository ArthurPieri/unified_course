# Module 01 — Quiz: Architecture

10 questions. Answer key + citations at the bottom. Treat as formative; for exam-realistic practice use `../mock_exam_sources.md`.

---

**1.** Which Snowflake layer is **always running** and cannot be suspended by the customer?
A. Database Storage
B. Query Processing
C. Cloud Services
D. Virtual Warehouse layer

**2.** Two separate virtual warehouses run queries against the same table at the same time. What is the result?
A. One query queues until the other completes.
B. Both run concurrently without contention; each reads from the shared storage layer independently.
C. Snowflake automatically clones the table.
D. The queries fail unless MULTI_STATEMENT_COUNT is set.

**3.** A user runs `SELECT COUNT(*) FROM big_table` and the query returns instantly with no warehouse credits consumed. Which cache served the query?
A. Warehouse local disk cache
B. Result cache
C. Metadata cache
D. Snowpipe ingest cache

**4.** Which of the following is **true** about Snowflake micro-partitions? (Select TWO)
A. Each micro-partition is typically 50-500 MB uncompressed.
B. Users can directly update a single row inside a micro-partition in place.
C. Snowflake tracks per-column min/max and distinct counts for each micro-partition.
D. Micro-partitions are stored as Apache Parquet files.
E. Micro-partitions are identified by file paths the user supplies.

**5.** A developer resizes a running warehouse from M to L. What happens to the warehouse's local SSD cache?
A. It migrates to the new VMs automatically.
B. It is cleared; new VMs are provisioned.
C. It doubles in size but retains contents.
D. Nothing — resizing only affects Cloud Services.

**6.** A user runs a query, then 10 minutes later runs the identical query after an `INSERT` into the source table. Does the result cache serve the second run?
A. Yes — result cache lives for 24 hours.
B. No — any DML on source data invalidates the result cache.
C. Yes — but only if the warehouse is still running.
D. Only if the query includes `RESULT_SCAN`.

**7.** Which statement about the separation of storage and compute in Snowflake is **correct**?
A. Customers must pre-provision disk capacity when creating a warehouse.
B. Compute scales independently of storage, and multiple warehouses share the same underlying storage.
C. Each warehouse has its own copy of every table.
D. Cloud Services storage is billed per TB per month like database storage.

**8.** What is the correct Snowflake object hierarchy?
A. Account -> Warehouse -> Schema -> Table
B. Account -> Database -> Schema -> Table/View/Stage/Pipe/...
C. Organization -> Database -> Warehouse -> Table
D. Account -> Schema -> Database -> Table

**9.** Which layer handles **query parsing and optimization**?
A. Database Storage
B. Query Processing (virtual warehouses)
C. Cloud Services
D. Snowpipe

**10.** A team needs isolation between ELT and BI workloads so heavy loads never slow down dashboards. What is the idiomatic Snowflake pattern?
A. Use a single warehouse with max concurrency set high.
B. Provision two warehouses — one for ELT, one for BI — both reading the same tables.
C. Clone the production database for BI.
D. Put BI queries on the Cloud Services layer directly.

---

## Answer key

1. **C** — Cloud Services is always on; only virtual warehouses can be suspended. *Platform Study Guide §1.1, p. 5*; `domain_1_0_architecture.md:L85`.
2. **B** — Workload isolation is the defining benefit of separated storage/compute. [Key concepts](https://docs.snowflake.com/en/user-guide/intro-key-concepts); `domain_1_0_architecture.md:L64, L91-L93`.
3. **C** — `COUNT(*)` without a predicate is served by the metadata cache in Cloud Services. [Micro-partitions](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions); *Core Study Guide Domain 3.0, p. 8*.
4. **A, C** — Size range and tracked metadata are both documented. [Micro-partitions](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions). B is false (micro-partitions are immutable); D is false (proprietary columnar format); E is false (Snowflake-managed).
5. **B** — Resize provisions new VMs; local disk cache is not migrated. [Virtual warehouses](https://docs.snowflake.com/en/user-guide/warehouses).
6. **B** — Any DML touching source data invalidates the result cache immediately. [Using persisted query results](https://docs.snowflake.com/en/user-guide/querying-persisted-results).
7. **B** — Independent scaling and shared storage are the point. *Platform Study Guide §1.1, p. 5*; `domain_1_0_architecture.md:L22-L27`.
8. **B** — Standard hierarchy. *Platform Study Guide §1.5, p. 5*.
9. **C** — Parsing, optimization, metadata, transactions all live in Cloud Services. *Core Study Guide Domain 1.0, p. 6*; `domain_1_0_architecture.md:L65-L66`.
10. **B** — Classic workload-isolation pattern. `domain_1_0_architecture.md:L88-L93`.
