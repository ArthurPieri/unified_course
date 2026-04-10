# Module 06 Quiz — AWS Cost / FinOps

8 questions. Answer key below.

---

**Q1.** An Athena query scans 1.2 TB when it should be scanning 12 GB because the team uses `SELECT *` on unpartitioned CSV. Which TWO single fixes deliver the largest savings? (pick the best pair as one answer)

- A) Move files to Glacier + use SSE-KMS
- B) Partition by date + convert files to Parquet
- C) Enable workgroup metrics + archive query history
- D) Add Redshift Spectrum

**Q2.** Which Glue feature targets batch jobs with relaxed SLAs at a lower per-DPU price?

- A) Glue Studio
- B) Glue Flex execution class
- C) Glue DataBrew
- D) Glue Workflows

**Q3.** A customer runs a nightly 2-hour Redshift workload. Otherwise the cluster is idle. Lowest-cost option?

- A) Always-on RA3 cluster
- B) Redshift Serverless or Pause/Resume on RA3
- C) Migrate to Athena
- D) DC2 provisioned with Reserved Instances

**Q4.** Which EMR feature automatically adds and removes nodes based on YARN metrics?

- A) Instance fleets only
- B) Managed scaling
- C) Auto-termination policy
- D) EMR Studio

**Q5.** How should a data lake minimize Athena scan cost on raw JSON ingested by Firehose?

- A) Query the raw JSON directly in Athena
- B) Enable Firehose record format conversion to Parquet with a Glue schema reference, partitioned by event time
- C) Compress JSON with gzip only
- D) Use DynamoDB streams

**Q6.** Which DynamoDB capacity mode best fits a highly unpredictable, spiky workload with minimal ops?

- A) Provisioned with Reserved Capacity
- B) Provisioned with auto-scaling
- C) On-demand
- D) Provisioned 100k RCU baseline

**Q7.** Which feature lets administrators cap the amount of data Athena will scan for a single query?

- A) IAM `athena:*` conditions
- B) Athena workgroup per-query data-scanned limit
- C) CloudWatch alarm
- D) Service Quotas

**Q8.** For a weekly bursty Spark job with 30-minute start latency tolerance, cheapest option is typically:

- A) Always-on EMR on EC2
- B) EMR Serverless or Glue Flex
- C) Redshift
- D) Lambda

---

## Answer key

1. **B** — Partitioning + Parquet are the canonical Athena savings combo. [Athena tuning](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html).
2. **B** — Glue Flex execution class. [Glue pricing](https://aws.amazon.com/glue/pricing/).
3. **B** — Redshift Serverless or Pause/Resume matches intermittent load. [Redshift Serverless](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-whatis.html).
4. **B** — EMR managed scaling. [EMR managed scaling](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-scaling.html).
5. **B** — Firehose JSON->Parquet conversion with Glue schema reduces downstream scan cost. [Firehose format conversion](https://docs.aws.amazon.com/firehose/latest/dev/record-format-conversion.html).
6. **C** — On-demand mode for unpredictable workloads. [DynamoDB capacity modes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html).
7. **B** — Athena workgroup data-scanned limits. [Athena workgroups](https://docs.aws.amazon.com/athena/latest/ug/workgroups.html).
8. **B** — EMR Serverless or Glue Flex for bursty batch with relaxed SLA. [EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html); [Glue pricing](https://aws.amazon.com/glue/pricing/).
