# Vendor Branch A: AWS Data Engineering

> Target certification: **AWS Certified Data Engineer - Associate (DEA-C01)**.
> Duration: **100-130 hours** (9-12 weeks at 10-12h/week).

This branch organizes AWS DEA-C01 preparation into a six-module taxonomy aligned with the four content domains. Modules are self-contained and cite AWS official documentation for depth.

## Who should take this branch

- You have completed Phases 0-5 of the unified course (or met the fast-track rubric: data modeling, ETL/ELT patterns, Spark fundamentals, streaming concepts, Medallion architecture, orchestration, monitoring, security principles).
- Your target employer uses AWS, or you want the broadest cloud market share.
- You have **1-2 years hands-on AWS** and **2-3 years data engineering** experience, per the DEA-C01 target candidate description. *AWS DEA-C01 Exam Guide, Target Candidate Description*.

## Prerequisites

| Prereq | Source |
|---|---|
| Phase 0-5 of unified course complete OR fast-track rubric met | See the unified course plan in the repo root |
| Python, SQL, Git, basic networking/compute | *AWS DEA-C01 Exam Guide, Recommended general IT knowledge* |
| AWS Free Tier account + CLI configured | [AWS Free Tier](https://aws.amazon.com/free/) |
| LocalStack Community (offline labs) | [LocalStack docs](https://docs.localstack.cloud/) |

Out of scope for the candidate (per the guide): ML training/inference, language-specific syntax, drawing business conclusions. *AWS DEA-C01 Exam Guide, Job tasks that are out of scope*.

## Module map (6 modules + exam profile)

| # | Module | DEA-C01 Domain(s) | Approx. hours |
|---|---|---|---|
| 00 | [Exam profile](./00_exam_profile/README.md) | All | 3 |
| 01 | [Storage: S3, Lake Formation, Glue Catalog](./01_storage_s3_lakeformation/README.md) | D2 (26%) | 22 |
| 02 | [Ingestion: Glue, DMS, DataSync, AppFlow, Kinesis, MSK](./02_ingestion_glue_dms_kinesis/README.md) | D1 (34%) | 28 |
| 03 | [Compute: EMR, Athena, Redshift, Glue ETL](./03_compute_emr_athena_redshift/README.md) | D1 + D3 | 24 |
| 04 | [Orchestration: MWAA, Step Functions, EventBridge](./04_orchestration_mwaa_stepfunctions/README.md) | D1 + D3 | 12 |
| 05 | [Security: IAM, KMS, VPC endpoints, Macie, Secrets Manager](./05_security_iam_kms/README.md) | D4 (18%) | 14 |
| 06 | [Cost / FinOps on AWS](./06_cost_finops/README.md) | Cross | 8 |

Domain weights are taken directly from the exam guide. *AWS DEA-C01 Exam Guide, Content outline*.

## Week plan (12-week default)

| Week | Focus | Modules | Sibling anchor |
|---|---|---|---|
| 1 | Exam profile + S3 storage classes + Glue Catalog intro | 00, 01 | [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/), [S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/) |
| 2 | Lake Formation, Iceberg on S3, lifecycle | 01 | [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html), [S3 Lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) |
| 3 | Batch ingestion: S3, DMS, DataSync, AppFlow | 02 | [AWS DMS User Guide](https://docs.aws.amazon.com/dms/latest/userguide/), [AWS DataSync](https://docs.aws.amazon.com/datasync/latest/userguide/) |
| 4 | Streaming: KDS, Firehose, MSK, Flink | 02 | [Amazon Kinesis Developer Guide](https://docs.aws.amazon.com/kinesis/latest/dev/), [Amazon MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/) |
| 5 | Glue ETL + DataBrew | 02, 03 | [AWS Glue ETL](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl.html) |
| 6 | EMR + Athena | 03 | [Amazon EMR Management Guide](https://docs.aws.amazon.com/emr/latest/ManagementGuide/), [Amazon Athena User Guide](https://docs.aws.amazon.com/athena/latest/ug/) |
| 7 | Redshift (RA3, Spectrum, Serverless) | 03 | [Amazon Redshift Developer Guide](https://docs.aws.amazon.com/redshift/latest/dg/) |
| 8 | Orchestration: Step Functions + MWAA + EventBridge | 04 | [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/) |
| 9 | Security: IAM, KMS, VPC endpoints | 05 | [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/), [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/) |
| 10 | Data quality, Macie, audit logging | 05 | [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/), [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/) |
| 11 | Cross-domain architecture + FinOps | 06 | [AWS Well-Architected Data Analytics Lens](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/) |
| 12 | Mock exams + weak-area remediation | 00 | See [mock_exam_sources.md](./mock_exam_sources.md) |

Accelerated path: 9 weeks by collapsing weeks 5-6 and weeks 9-10.

## Exit criteria

Before booking the exam you should be able to:

- [ ] Choose between KDS, Firehose, and MSK for a given latency/throughput/retention requirement. *AWS DEA-C01, Skill 1.1.1*.
- [ ] Pick the right store among S3, Redshift, DynamoDB, Aurora, OpenSearch, MemoryDB for a given access pattern. *Skill 2.1.1-2.1.3*.
- [ ] Design an S3 lifecycle policy that meets a retention/cost requirement. *Skill 2.3.2-2.3.3*.
- [ ] Write a least-privilege IAM policy for a Glue job accessing S3 and DynamoDB, with KMS key grants. *Skill 4.1.5, 4.2.6*.
- [ ] Pick Step Functions vs. MWAA vs. EventBridge for a given orchestration need. *Skill 1.3.1, 3.1.1*.
- [ ] Score >=75% on mock exams (see [mock_exam_sources.md](./mock_exam_sources.md)) without reference material.
- [ ] Complete the capstone lab end-to-end (see this module's labs/ directory).

## How to use this branch

1. Read the [exam profile](./00_exam_profile/README.md) first to anchor the domain weightings in your mind.
2. Work the 6 modules in order. Each module README is compact (600-1500 words) and links to AWS official documentation for depth.
3. Run the labs cited in each module against LocalStack (free) or AWS Free Tier.
4. Take the per-module quizzes (`quiz.md`). Every question cites a primary source.
5. Finish with [mock_exam_sources.md](./mock_exam_sources.md) for practice exam guidance.

## Reuse and citation policy

This branch follows the unified course reuse policy. Every service claim must cite `docs.aws.amazon.com` or the [AWS DEA-C01 Exam Guide](https://aws.amazon.com/certification/certified-data-engineer-associate/). No blogs, no Medium, no Stack Overflow.

## References

See [references.md](./references.md) and [mock_exam_sources.md](./mock_exam_sources.md).
