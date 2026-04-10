# Vendor Branch A: AWS Data Engineering

> Target certification: **AWS Certified Data Engineer - Associate (DEA-C01)**.
> Duration: **100-130 hours** (9-12 weeks at 10-12h/week). See `../../UNIFIED_COURSE_PLAN.md:581-653`.

This branch re-organizes the sibling `../../../aws_certified/` curriculum into a six-module taxonomy aligned with the four DEA-C01 content domains. It is **curation, not rewrite**: the sibling weeks carry the depth; modules here cite-link into them and fill service gaps from AWS official docs.

## Who should take this branch

- You have completed Phases 0-5 of the unified course (or met the fast-track rubric: data modeling, ETL/ELT patterns, Spark fundamentals, streaming concepts, Medallion architecture, orchestration, monitoring, security principles).
- Your target employer uses AWS, or you want the broadest cloud market share.
- You have **1-2 years hands-on AWS** and **2-3 years data engineering** experience, per the DEA-C01 target candidate description. *AWS DEA-C01 Exam Guide, Target Candidate Description*.

## Prerequisites

| Prereq | Source |
|---|---|
| Phase 0-5 of unified course complete OR fast-track rubric met | `../../UNIFIED_COURSE_PLAN.md:583` |
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
| 1 | Exam profile + S3 storage classes + Glue Catalog intro | 00, 01 | `../../../aws_certified/docs/week-01-ingestion-fundamentals.md:41-128` |
| 2 | Lake Formation, Iceberg on S3, lifecycle | 01 | `../../../aws_certified/docs/week-06-cataloging-data-lakes.md:101-246`, `week-07-lifecycle-schema.md:22-415` |
| 3 | Batch ingestion: S3, DMS, DataSync, AppFlow | 02 | `../../../aws_certified/docs/week-01-ingestion-fundamentals.md:129-367` |
| 4 | Streaming: KDS, Firehose, MSK, Flink | 02 | `../../../aws_certified/docs/week-02-streaming-ingestion.md:7-410` |
| 5 | Glue ETL + DataBrew | 02, 03 | `../../../aws_certified/docs/week-03-data-transformation.md:20-358` |
| 6 | EMR + Athena | 03 | `../../../aws_certified/docs/week-03-data-transformation.md:359-606`, `week-08-automation-analysis.md:368-644` |
| 7 | Redshift (RA3, Spectrum, Serverless) | 03 | `../../../aws_certified/docs/week-05-data-store-selection.md:242-345`, `week-08-automation-analysis.md:645-802` |
| 8 | Orchestration: Step Functions + MWAA + EventBridge | 04 | `../../../aws_certified/docs/week-04-orchestration.md:20-559` |
| 9 | Security: IAM, KMS, VPC endpoints | 05 | `../../../aws_certified/docs/week-10-security-governance.md:9-663` |
| 10 | Data quality, Macie, audit logging | 05 | `../../../aws_certified/docs/week-09-monitoring-quality.md:539-875`, `week-10-security-governance.md:664-921` |
| 11 | Cross-domain architecture + FinOps | 06 | `../../../aws_certified/docs/week-11-cross-domain.md:20-476` |
| 12 | Mock exams + weak-area remediation | 00 | `../../../aws_certified/docs/week-12-mock-exam-1.md`, `week-12-mock-exam-2.md` |

Accelerated path: 9 weeks by collapsing weeks 5-6 and weeks 9-10.

## Exit criteria

Before booking the exam you should be able to:

- [ ] Choose between KDS, Firehose, and MSK for a given latency/throughput/retention requirement. *AWS DEA-C01, Skill 1.1.1*.
- [ ] Pick the right store among S3, Redshift, DynamoDB, Aurora, OpenSearch, MemoryDB for a given access pattern. *Skill 2.1.1-2.1.3*.
- [ ] Design an S3 lifecycle policy that meets a retention/cost requirement. *Skill 2.3.2-2.3.3*.
- [ ] Write a least-privilege IAM policy for a Glue job accessing S3 and DynamoDB, with KMS key grants. *Skill 4.1.5, 4.2.6*.
- [ ] Pick Step Functions vs. MWAA vs. EventBridge for a given orchestration need. *Skill 1.3.1, 3.1.1*.
- [ ] Score >=75% on `week-12-mock-exam-1.md` and `week-12-mock-exam-2.md` without reference material.
- [ ] Complete the capstone lab end-to-end: `../../../aws_certified/labs/week-11-lab-capstone.md`.

## How to use this branch

1. Read the [exam profile](./00_exam_profile/README.md) first to anchor the domain weightings in your mind.
2. Work the 6 modules in order. Each module README is compact (600-1500 words) and points to the sibling `week-*.md` files for depth.
3. Run the labs cited in each module against LocalStack (free) or AWS Free Tier.
4. Take the per-module quizzes (`quiz.md`). Every question cites a primary source.
5. Finish with `mock_exam_sources.md` and the sibling `week-12-mock-exam-*.md` files.

## Reuse and citation policy

This branch follows `../../docs/REUSE_POLICY.md`. Every service claim must cite `docs.aws.amazon.com` or the DEA-C01 exam guide. Sibling files are cited as `../../../aws_certified/<path>:L<start>-L<end>`. No blogs, no Medium, no Stack Overflow.

## References

See [references.md](./references.md) and [mock_exam_sources.md](./mock_exam_sources.md).
