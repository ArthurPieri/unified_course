# Module 01: Storage — S3, Lake Formation, Glue Data Catalog (22h)

> Domain 2 on the exam is **26%** of scored content and this module is its center of gravity. *AWS DEA-C01 Exam Guide, Content outline*.

## Learning goals

- Select an S3 storage class for a given access pattern and retention requirement. *Skill 2.3.2-2.3.3*.
- Design an S3 Lifecycle policy that transitions and expires objects to meet a cost/compliance target. *Skill 2.3.2*.
- Explain the Glue Data Catalog's role (databases, tables, partitions, crawlers) and when to use it vs. a Hive metastore. *Skill 2.2.2-2.2.5*.
- Grant column/row/cell-level permissions through Lake Formation across Athena, Redshift Spectrum, EMR, and Glue. *Skill 4.2.4*.
- Manage Apache Iceberg tables on S3 (snapshots, compaction, schema evolution). *Skill 2.1.7, 2.4.2*.
- Apply partitioning, compression, and file-size best practices to reduce query cost. *Skill 2.4.5*.

## Exam weight

Data Store Management = 26% of scored content. Lifecycle (Task 2.3), cataloging (Task 2.2), and schema/modeling (Task 2.4) all live here. *Exam Guide, Content outline + Content Domain 2*.

## Key services and primary docs

| Service | What to know | AWS doc |
|---|---|---|
| Amazon S3 | Storage classes, Lifecycle, Versioning, Object Lock, Multipart Upload, Transfer Acceleration, Access Points | [S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) |
| S3 storage classes | Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Instant/Flexible/Deep Archive, Express One Zone | [Using Amazon S3 storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html) |
| S3 Lifecycle | Transition and expiration rules; noncurrent-version rules; minimum duration per class | [Managing your storage lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) |
| AWS Glue Data Catalog | Databases, tables, partitions, schema versions, crawlers | [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html#data-catalog-intro) |
| AWS Lake Formation | TBAC, column/row/cell filters, LF-tags, cross-account sharing | [What is Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html) |
| Apache Iceberg on AWS | Athena/EMR/Glue Iceberg support, snapshots, time travel, compaction | [Using Iceberg tables in Athena](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg.html) |
| DynamoDB TTL | Attribute-based expiry, ~48h delete latency | [Expiring items by using DynamoDB Time to Live](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) |

## Concepts (compact)

### Storage classes and the cheap/slow trade-off
Standard is the default for hot data. Standard-IA has a lower per-GB cost but a per-GB retrieval fee and a 30-day minimum charge; One Zone-IA drops AZ redundancy for ~20% savings. Intelligent-Tiering auto-moves objects between access tiers for a monitoring fee. Glacier Instant/Flexible/Deep Archive trade retrieval latency (ms / minutes-hours / hours) for progressively lower storage cost. Every class except Standard has a minimum storage duration (30/90/180 days) — transitioning too early is a common exam trap. Depth: `../../../aws_certified/docs/week-07-lifecycle-schema.md:22-157`. Primary: [Using Amazon S3 storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html).

### Lifecycle rules
A lifecycle rule targets a prefix or tag and chains transitions plus a final expiration. For versioned buckets, noncurrent-version transitions/expirations are configured separately. Transitions have a 30-day minimum to IA classes. Depth: `../../../aws_certified/docs/week-07-lifecycle-schema.md:22-229`. Lab: `../../../aws_certified/labs/week-07-lab-lifecycle.md:13-258`.

### Glue Data Catalog
The Catalog is a Hive-metastore-compatible store of databases, tables, and partitions consumed by Athena, Redshift Spectrum, EMR, and Glue ETL. Crawlers infer schema and register partitions; partition indexes speed up queries with high partition counts. Depth: `../../../aws_certified/docs/week-06-cataloging-data-lakes.md:9-100`. Primary: [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html#data-catalog-intro).

### Lake Formation permissions
Lake Formation sits in front of the Catalog and enforces fine-grained permissions (database, table, column, row, cell) across Athena, Redshift Spectrum, EMR, and Glue ETL. LF-tags (TBAC) scale better than resource grants for large lakes. It is the canonical answer to "column-level access in a data lake". Depth: `../../../aws_certified/docs/week-06-cataloging-data-lakes.md:101-196` and `week-10-security-governance.md:224-357`. Primary: [Lake Formation permissions reference](https://docs.aws.amazon.com/lake-formation/latest/dg/lf-permissions-reference.html).

### Open table formats — Iceberg
Iceberg tables on S3 give you ACID, schema evolution, time travel, and hidden partitioning, readable by Athena (engine v3), EMR (Spark/Trino), and Glue. Maintenance = snapshot expiration + file compaction, otherwise small-file counts blow up query cost. Depth: `../../../aws_certified/docs/week-07-lifecycle-schema.md:294-501`. Primary: [Querying Iceberg tables in Athena](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg.html).

### Partitioning, compression, file size
For Athena/Spectrum, partition by low-cardinality filters (date, region) and aim for 128 MB-1 GB Parquet files. Snappy is the default Parquet codec; ZSTD gives better ratios at a CPU cost. Depth: `../../../aws_certified/docs/week-07-lifecycle-schema.md:502-638`. Primary: [Top 10 performance tuning tips for Athena](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html).

## Labs (from sibling `../../../aws_certified/labs/`)

| Lab | Goal | Sibling anchor |
|---|---|---|
| Week 1 Lab — S3 buckets and lifecycle on LocalStack | Create buckets, lifecycle rules, multipart upload | `../../../aws_certified/labs/week-01-lab-ingestion.md:83-258` |
| Week 6 Lab — 3-zone data lake | Raw/curated/consumption zones on S3 with partitioned Parquet | `../../../aws_certified/labs/week-06-lab-datalake.md:13-400` |
| Week 7 Lab — Lifecycle + DynamoDB TTL + Iceberg | Lifecycle rules, TTL, Iceberg table DDL in Athena | `../../../aws_certified/labs/week-07-lab-lifecycle.md:13-434` |
| Week 10 Lab — Lake Formation permissions | Database/table/column-level access | `../../../aws_certified/labs/week-10-lab-security.md:1-400` |

## Common exam gotchas (derived from the exam guide)

| Gotcha | Why it trips people | Reference |
|---|---|---|
| Transitioning to Standard-IA before 30 days | Not allowed; Lifecycle rule will fail validation | [Lifecycle configuration elements](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html) |
| Column-level security in a data lake | Lake Formation — not IAM bucket policy | *Exam Guide, Skill 4.2.4* |
| DynamoDB TTL deletion latency | Can take up to 48 hours; always filter expired items in queries | [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html); `../../../aws_certified/labs/week-07-lab-lifecycle.md:411-433` |
| Glacier Flexible vs. Deep Archive retrieval | Flexible: minutes-hours; Deep Archive: within 12 hours | [Glacier retrieval options](https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects-retrieval-options.html) |
| Iceberg small-file problem | Without compaction, queries slow down; run `OPTIMIZE` / Glue table optimization | [Athena Iceberg OPTIMIZE](https://docs.aws.amazon.com/athena/latest/ug/optimize-statement.html) |

## References

See [references.md](./references.md).

## Checkpoint

- [ ] Given a retention spec (e.g., "keep 1 year hot, 6 years cold, delete at 7"), you can write the lifecycle rule.
- [ ] You can explain when Lake Formation is required over plain IAM.
- [ ] You can read and write an Iceberg table from Athena.
