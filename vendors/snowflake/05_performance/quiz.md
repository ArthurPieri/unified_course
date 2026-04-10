# Module 05 — Quiz: Performance and Cost

10 questions. Key + citations at the bottom.

---

**1.** A single analytic query runs slowly and Query Profile shows "Bytes spilled to remote storage". What is the first tuning step?
A. Enable multi-cluster scaling
B. Scale the warehouse up (e.g., M -> L)
C. Add a clustering key
D. Enable Search Optimization

**2.** A team reports that dashboards queue during business hours while ELT jobs run on the same warehouse. What is the correct fix?
A. Scale the warehouse up to 4XL
B. Enable multi-cluster warehouses, or split BI onto its own warehouse
C. Add Search Optimization on all tables
D. Increase `AUTO_SUSPEND`

**3.** Which setting controls when an idle warehouse stops billing?
A. `AUTO_RESUME`
B. `AUTO_SUSPEND`
C. `MAX_CONCURRENCY_LEVEL`
D. `SCALING_POLICY`

**4.** Which statement about the warehouse (SSD) local cache is **true**?
A. It survives suspension.
B. It survives a resize.
C. It is cleared on suspend or resize.
D. It is stored in Cloud Services.

**5.** Which query pattern is the **best** fit for enabling the Search Optimization Service?
A. Analytical aggregation over a full day of data
B. Point-lookup on a high-cardinality column not covered by the clustering key
C. JOIN between two small dimension tables
D. `COUNT(*)` on an entire table

**6.** Which function reports average clustering depth for a table?
A. `SYSTEM$PIPE_STATUS`
B. `SYSTEM$CLUSTERING_INFORMATION`
C. `SYSTEM$QUERY_STATS`
D. `QUERY_HISTORY`

**7.** The Query Acceleration Service is:
A. Billed as part of the warehouse it is attached to
B. Billed serverlessly, separate from the warehouse
C. Only available in Virtual Private Snowflake
D. A cache, not a compute service

**8.** Which `SCALING_POLICY` spins up additional clusters **eagerly** to minimize queueing?
A. STANDARD
B. ECONOMY
C. EAGER
D. BURST

**9.** A resource monitor has a quota of 100 credits and an action of `SUSPEND` at 100%. What happens at 100% used?
A. The account is locked.
B. All currently running queries finish, then the assigned warehouse(s) suspend.
C. All queries are killed immediately.
D. Nothing — SUSPEND only notifies.

**10.** Which of the following accelerate point-lookup queries on a large table? (Select TWO)
A. Clustering key on the lookup column
B. Search Optimization on the lookup column
C. Higher `AUTO_SUSPEND`
D. Result cache
E. Materialized view on the full table

---

## Answer key

1. **B** — Remote spill means memory pressure; scaling up gives more RAM per worker. *Core Study Guide Domain 3.0, p. 8*; [Query Profile](https://docs.snowflake.com/en/user-guide/ui-query-profile).
2. **B** — Concurrency problem, not a per-query latency problem. [Multi-cluster warehouses](https://docs.snowflake.com/en/user-guide/warehouses-multicluster).
3. **B** — `AUTO_SUSPEND` in seconds. [ALTER WAREHOUSE](https://docs.snowflake.com/en/sql-reference/sql/alter-warehouse).
4. **C** — Cache is cleared on suspend and resize. [Warehouses](https://docs.snowflake.com/en/user-guide/warehouses); `../01_architecture/README.md`.
5. **B** — SOS is for selective lookups on non-clustered columns. [SOS](https://docs.snowflake.com/en/user-guide/search-optimization-service).
6. **B** — `SYSTEM$CLUSTERING_INFORMATION`. [Clustering info](https://docs.snowflake.com/en/sql-reference/functions/system_clustering_information).
7. **B** — QAS is serverless, billed separately. [QAS](https://docs.snowflake.com/en/user-guide/query-acceleration-service).
8. **A** — STANDARD is eager. [Multi-cluster warehouses](https://docs.snowflake.com/en/user-guide/warehouses-multicluster).
9. **B** — SUSPEND waits for running queries to finish. `SUSPEND_IMMEDIATE` kills them. [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors).
10. **A, B** — Clustering key prunes partitions; SOS indexes for point lookups. [Clustering keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys); [SOS](https://docs.snowflake.com/en/user-guide/search-optimization-service).
