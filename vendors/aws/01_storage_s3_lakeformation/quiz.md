# Module 01 Quiz — Storage, S3, Lake Formation, Glue Catalog

10 questions. Answer key below with primary-source cites.

---

**Q1.** A team wants to store log files for 7 years, with instant-millisecond access for the first 30 days and rare access thereafter, at lowest cost. Which lifecycle plan fits best?

- A) Standard -> Glacier Deep Archive at day 1
- B) Standard for 30 days -> S3 Glacier Instant Retrieval -> Expire at day 2555
- C) Standard for 30 days -> Standard-IA at day 15 -> Deep Archive at day 90
- D) Standard One Zone-IA for 7 years

**Q2.** What is the minimum storage duration charged for an object placed in S3 Standard-IA?

- A) 0 days
- B) 30 days
- C) 90 days
- D) 180 days

**Q3.** Which service enforces column-level access control across Athena, Redshift Spectrum, EMR, and Glue ETL consumers of a shared Glue Data Catalog?

- A) IAM bucket policies
- B) KMS key policies
- C) AWS Lake Formation
- D) AWS Config

**Q4.** Which statement about DynamoDB TTL is correct?

- A) Expired items are deleted within 1 minute of the TTL timestamp.
- B) TTL applies only to items in a GSI.
- C) Expired items may persist up to 48 hours, so queries should filter them out.
- D) TTL cannot be combined with on-demand capacity.

**Q5.** A data lake uses Apache Iceberg tables in Athena. Queries have slowed over time. What maintenance operation most directly addresses small-file proliferation?

- A) `VACUUM` on the underlying S3 bucket
- B) `OPTIMIZE ... REWRITE DATA USING BIN_PACK`
- C) Increase Athena query concurrency
- D) Switch to CSV format

**Q6.** Which S3 feature lets you create distinct hostnames and policies for application-specific access to the same bucket?

- A) Transfer Acceleration
- B) Access Points
- C) Multi-Region Access Points only
- D) Object Lock

**Q7.** A bucket is versioned. Which rule expires noncurrent object versions after 90 days?

- A) A Lifecycle rule with a `NoncurrentVersionExpiration` action
- B) An IAM policy denying GET on versions older than 90 days
- C) Enabling S3 Object Lock in Compliance mode
- D) A bucket replication rule

**Q8.** Which Glue feature automatically discovers schemas and registers partitions in the Data Catalog?

- A) Glue Studio
- B) Glue DataBrew
- C) Glue Crawlers
- D) Glue Workflows

**Q9.** Which is true about LF-tags (Lake Formation tag-based access control)?

- A) They are the same as S3 object tags.
- B) They let you grant permissions on catalog resources via key-value tags, scaling better than explicit resource grants.
- C) They only work in Redshift.
- D) They replace IAM for cross-account sharing.

**Q10.** You want ACID writes, schema evolution, and time travel on S3 data queried from Athena, EMR, and Glue. Which table format?

- A) CSV with Glue Catalog partitions
- B) Parquet-only directory
- C) Apache Iceberg
- D) JSON Lines

---

## Answer key

1. **C** — Standard-IA has a 30-day minimum after transition; Deep Archive fits the 7-year cold tail. Direct Glacier from day 1 (A) loses hot access and violates the 30-day requirement; Deep Archive cannot be targeted at day 15 (B is invalid because Standard-IA must be >=30d before further transitions and Instant Retrieval is pricier than Deep Archive for 6+ years). [S3 storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html).
2. **B** — 30 days minimum. [Using Amazon S3 storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html).
3. **C** — Lake Formation. *AWS DEA-C01 Exam Guide, Skill 4.2.4*. [Lake Formation permissions reference](https://docs.aws.amazon.com/lake-formation/latest/dg/lf-permissions-reference.html).
4. **C** — TTL deletions are asynchronous and can take up to 48 hours. [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html); `../../../aws_certified/labs/week-07-lab-lifecycle.md:411-413`.
5. **B** — `OPTIMIZE ... REWRITE DATA USING BIN_PACK` bin-packs small files. [Athena OPTIMIZE](https://docs.aws.amazon.com/athena/latest/ug/optimize-statement.html).
6. **B** — S3 Access Points. [S3 Access Points](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html).
7. **A** — `NoncurrentVersionExpiration` in a lifecycle rule. [Lifecycle configuration elements](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html).
8. **C** — Crawlers. [Working with crawlers](https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html).
9. **B** — LF-tags are catalog-level tag-based access control. [LF-TBAC](https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html).
10. **C** — Apache Iceberg. [Querying Iceberg tables in Athena](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg.html).
