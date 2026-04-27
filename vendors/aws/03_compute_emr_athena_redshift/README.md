# Module 03: Compute — EMR, Athena, Redshift, Glue ETL (24h)

> Crosses Domain 1 (transform/process) and Domain 3 (analyze data). Together these domains = **56%** of scored content. *AWS DEA-C01 Exam Guide, Content outline*.

## Learning goals

- Pick Glue ETL vs. EMR vs. Athena vs. Redshift for a given SLA, data size, language, and team skillset. *Skill 1.2.5, 2.1.1*.
- Write Athena queries against partitioned S3 data and Iceberg tables, including federated queries. *Skill 3.2.3*.
- Design a Redshift schema: distribution key, sort key, RA3 vs. Serverless, materialized views, data sharing. *Skill 2.4.1, 2.1.5*.
- Tune EMR clusters (instance types, Spot, EMR Serverless, EMR on EKS). *Skill 1.2.1, 1.2.5*.
- Use Redshift Spectrum and federated queries to read S3 / RDS without ETL. *Skill 2.1.5*.
- Optimize costs during processing (Spot, auto-scaling, file formats). *Skill 1.2.4*.

## Exam weight

- Domain 1, Tasks 1.2 and 1.4 — transform/process and programming.
- Domain 2, Task 2.1 — choose a data store (Redshift, EMR, Athena, RDS).
- Domain 3, Tasks 3.1 and 3.2 — automate and analyze.

## Key services and primary docs

| Service | What to know | AWS doc |
|---|---|---|
| AWS Glue ETL | Spark/Python jobs, DynamicFrames, bookmarks, worker types (G.1X/G.2X/G.025X/Flex) | [AWS Glue Dev Guide](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html) |
| Amazon EMR | Managed Hadoop/Spark/Hive/Presto, EMR Serverless, EMR on EKS, instance fleets, Spot | [EMR Management Guide](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html) |
| EMR Serverless | Pay-per-job Spark/Hive, pre-initialized capacity | [EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html) |
| Amazon Athena | Serverless SQL on S3, Iceberg, federated query, Athena Spark notebooks | [Athena User Guide](https://docs.aws.amazon.com/athena/latest/ug/what-is.html) |
| Amazon Redshift | RA3 nodes (managed storage), Serverless, distribution styles, sort keys, materialized views, data sharing | [Redshift Developer Guide](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html) |
| Redshift Spectrum | Query S3 directly from Redshift via external schemas | [Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html) |
| Managed Flink | Stateful stream processing (SQL and Apache Flink) | [Managed Service for Apache Flink](https://docs.aws.amazon.com/managed-flink/latest/java/what-is.html) |
| Amazon QuickSight | Serverless BI, SPICE, direct query, row-level security | [QuickSight User Guide](https://docs.aws.amazon.com/quicksight/latest/user/welcome.html) |

## Concepts (compact)

### Glue vs. EMR vs. Athena vs. Redshift
- **Glue ETL** — serverless Spark, pay-per-DPU-second, best for "move and shape" batch jobs with schema drift (DynamicFrames). Cold-start ~1 min for standard jobs; Flex saves ~35% at relaxed SLA.
- **EMR** — cluster Spark/Hive/Presto with full control. Use for large long-running jobs, custom libraries, Spot savings, HBase/Trino stacks. EMR Serverless removes cluster management; EMR on EKS shares a k8s cluster.
- **Athena** — serverless SQL, pay-per-TB-scanned. Best for ad-hoc SQL on S3, Iceberg, federated queries. Athena Spark notebooks handle PySpark ad-hoc analysis.
- **Redshift** — columnar MPP warehouse. RA3 nodes separate compute from managed storage; Serverless autoscales RPUs. Best for BI workloads that need sub-second interactive SQL across TBs-PBs.

Primary: [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/), [Amazon EMR Management Guide](https://docs.aws.amazon.com/emr/latest/ManagementGuide/), [Amazon Athena User Guide](https://docs.aws.amazon.com/athena/latest/ug/), [Amazon Redshift Developer Guide](https://docs.aws.amazon.com/redshift/latest/dg/).

### Redshift distribution styles and sort keys
Distribution styles: **KEY** (co-locate rows with matching hash), **ALL** (replicate small dim tables), **EVEN** (round-robin), **AUTO** (Redshift chooses). Sort keys: compound (default) or interleaved (rare). Pick DIST KEY on the most common join column; pick SORT KEY on filter columns (e.g., date). Wrong DIST KEY = shuffle-heavy queries. Primary: [Redshift distribution styles](https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html).

### Redshift Spectrum and federated queries
Spectrum reads external tables in S3 (Glue Catalog) without loading to Redshift. Federated queries reach into RDS/Aurora PostgreSQL or MySQL. Together they give you "load only the hot table" designs. Primary: [Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html), [Athena federated query](https://docs.aws.amazon.com/athena/latest/ug/connect-to-a-data-source.html).

### Athena partition projection and results reuse
Partition projection removes the need to run `MSCK REPAIR` / crawlers when the partition scheme is predictable (date-based). Query results reuse caches results for up to 7 days. Workgroups enforce per-query and per-workgroup data-scanned limits for cost control. Primary: [Athena partition projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html), [Athena query results reuse](https://docs.aws.amazon.com/athena/latest/ug/reusing-query-results.html), [Athena workgroups](https://docs.aws.amazon.com/athena/latest/ug/workgroups.html).

### EMR cost levers
Use Instance Fleets with Spot for task nodes; keep core nodes On-Demand or Spot-with-capacity-reservation; use managed scaling; prefer EMR Serverless for bursty workloads. Primary: [EMR instance fleets](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-instance-fleet.html), [EMR managed scaling](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-scaling.html), [EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html).

### Spark programming concepts in scope
`repartition` vs. `coalesce`, broadcast joins, window functions, skew handling, caching. *Skill 1.4.10 — distributed computing*. Primary: [AWS Glue ETL programming](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl.html). Language-specific syntax is explicitly out of scope. *Exam Guide, out-of-scope tasks*.

## Labs

See the hands-on labs in this module's labs/ directory. Key exercises:

| Lab | Goal | AWS reference |
|---|---|---|
| Glue ETL | JSON->Parquet Glue job, bookmarks, ResolveChoice | [AWS Glue ETL](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl.html) |
| Data stores | DynamoDB GSI queries, Redshift load, Athena queries | [Amazon Redshift](https://docs.aws.amazon.com/redshift/latest/dg/), [Amazon Athena](https://docs.aws.amazon.com/athena/latest/ug/) |
| Athena + Lambda automation | Lambda schema validation, Athena ad-hoc queries | [Amazon Athena User Guide](https://docs.aws.amazon.com/athena/latest/ug/) |
| Capstone | End-to-end pipeline (Kinesis -> Firehose -> S3 -> Glue -> Athena) | [AWS Well-Architected Data Analytics Lens](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/) |

## Common exam gotchas

| Gotcha | Why it trips people | Reference |
|---|---|---|
| Athena billing = data scanned, not rows | Unpartitioned or SELECT * blows up cost | [Athena pricing](https://aws.amazon.com/athena/pricing/) |
| Redshift DIST ALL on a large fact table | Storage and load-time blow-up; use KEY instead | [Distribution styles](https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html) |
| Glue bookmarks + schema drift | Bookmarks track paths, not schemas — drift can silently skip files | [Glue bookmarks](https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html) |
| EMR Serverless vs. EMR on EKS | Serverless = no cluster, per-job billing; EKS = share k8s | [EMR Serverless vs EKS](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html) |
| Redshift materialized views refresh | Can be auto or manual; stale on high-churn bases | [Redshift materialized views](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-overview.html) |
| Athena federated query | Uses Lambda data source connectors, extra latency | [Athena federated query](https://docs.aws.amazon.com/athena/latest/ug/connect-to-a-data-source.html) |

## References

See [references.md](./references.md).

## Checkpoint

- [ ] Given a data size, SLA, and team skillset, you can pick Glue vs. EMR vs. Athena vs. Redshift and justify.
- [ ] You can design a Redshift schema with correct DIST/SORT keys.
- [ ] You can run an Athena query cost-estimation before executing.
