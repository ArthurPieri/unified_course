# Module 03 Quiz — Compute (EMR, Athena, Redshift, Glue ETL)

9 questions. Answer key with cites.

---

**Q1.** A fact table of 10 B rows is frequently joined to a small dimension of 5 K rows in Redshift. Which distribution style should the dimension use?

- A) KEY on the join column
- B) EVEN
- C) ALL
- D) AUTO

**Q2.** An analyst runs `SELECT * FROM events WHERE event_date = '2025-01-01'` in Athena against a table partitioned on `event_date`. The query scans the entire dataset. Most likely cause:

- A) Athena does not support partitioning
- B) The table is not registered in the Glue Data Catalog
- C) Partition column is not being used as a partition (i.e., not declared or partitions not loaded)
- D) S3 Intelligent-Tiering is enabled

**Q3.** Which service is best for ad-hoc PySpark exploration against S3 data without managing a cluster or a Glue job?

- A) EMR Serverless Spark application
- B) Athena Spark notebooks
- C) Glue DataBrew
- D) Redshift stored procedures

**Q4.** Which Redshift feature lets another Redshift cluster query your data live without copying it?

- A) UNLOAD to S3
- B) Redshift Spectrum
- C) Redshift data sharing (datashares)
- D) Materialized views

**Q5.** What is the cheapest valid way to run a bursty weekly Spark job that processes 2 TB and tolerates a 30-minute start delay?

- A) Always-on EMR cluster, On-Demand
- B) Glue ETL with Flex execution class
- C) Redshift Serverless
- D) EMR on EKS with reserved capacity

**Q6.** Athena is billed primarily on which metric?

- A) Rows returned
- B) Data scanned (bytes read from S3)
- C) Query duration seconds
- D) Number of partitions

**Q7.** A Glue job's bookmarks skipped new files after the source added a column. Why?

- A) Bookmarks track only paths/timestamps, not schema; a crawler or job re-read is needed if schema handling differs
- B) Bookmarks are disabled by default
- C) Glue bookmarks require Iceberg
- D) Bookmarks require Lake Formation

**Q8.** Which Redshift node family separates compute from managed storage, enabling independent scaling?

- A) DS2
- B) DC2
- C) RA3
- D) DL1

**Q9.** A Redshift query that joins a 500 M-row table on `customer_id` to another 500 M-row table on `customer_id` is slow with heavy network shuffle. Best first fix:

- A) Add a BRIN index
- B) Set DIST KEY = `customer_id` on both tables
- C) Switch to DIST ALL on both tables
- D) Convert to external Spectrum tables

---

## Answer key

1. **C** — DIST ALL replicates small dim tables to every node, eliminating shuffle. [Redshift distribution styles](https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html).
2. **C** — Partitions not declared as partition columns or not loaded (or partition projection not configured). [Athena partitions](https://docs.aws.amazon.com/athena/latest/ug/partitions.html).
3. **B** — Athena Spark notebooks. *AWS DEA-C01 Exam Guide, Skill 3.2.4*. [Athena notebooks](https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark.html).
4. **C** — Redshift data sharing. [Redshift data sharing](https://docs.aws.amazon.com/redshift/latest/dg/datashare-overview.html).
5. **B** — Glue Flex execution class is designed for non-urgent batch and is cheaper than standard. [Glue Flex](https://docs.aws.amazon.com/glue/latest/dg/add-job.html#glue-execution-class).
6. **B** — Data scanned. [Athena pricing](https://aws.amazon.com/athena/pricing/).
7. **A** — Bookmarks track processed paths and timestamps; schema drift can cause unexpected behavior. [Glue job bookmarks](https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html).
8. **C** — RA3 nodes with managed storage. [RA3 nodes](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#rs-ra3-node-types).
9. **B** — Co-locating on DIST KEY = `customer_id` removes the shuffle. [Distribution styles](https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html).
