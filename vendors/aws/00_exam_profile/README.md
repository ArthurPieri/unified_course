# Module 00: DEA-C01 Exam Profile (3h)

> Anchor every study decision to the official exam guide.
> Source of truth for this module: `../../../../aws_certified/data-engineer-associate-01.pdf` = *AWS DEA-C01 Exam Guide* (cited inline).

## Learning goals

- Recite the four content domains and their weightings without looking them up.
- Name the target candidate profile (experience, in-scope tasks, out-of-scope tasks).
- Describe the exam format (question types, scoring, passing score).
- Book the exam through the correct channel (AWS Certification portal + Pearson VUE).
- Build a personal prep order that matches the domain weightings.

## The certification in one table

| Field | Value | Source |
|---|---|---|
| Code | DEA-C01 | *AWS DEA-C01 Exam Guide, cover* |
| Level | Associate | *Exam Guide, Introduction* |
| Scored questions | 50 | *Exam Guide, Response types* |
| Unscored (pretest) questions | 15 | *Exam Guide, Unscored content* |
| Response types | Multiple choice, multiple response | *Exam Guide, Response types* |
| Scoring model | Scaled 100-1000, compensatory | *Exam Guide, Exam results* |
| Passing score | **720** | *Exam Guide, Exam results* |
| Designation | Pass / fail | *Exam Guide, Exam results* |
| Delivery | Pearson VUE test center or OnVUE online | [AWS Certification - Schedule your exam](https://aws.amazon.com/certification/policies/before-testing/) |
| Registration | [AWS Certification portal](https://www.aws.training/certification) | AWS |

Note: unanswered questions are scored incorrect; there is no guessing penalty. *Exam Guide, Response types*.

## The four domains

| # | Domain | Weight | Key tasks | Primary modules |
|---|---|---|---|---|
| 1 | **Data Ingestion and Transformation** | **34%** | Ingestion (streaming + batch), transform/process, orchestrate pipelines, programming concepts | 02, 03, 04 |
| 2 | **Data Store Management** | **26%** | Choose a data store, cataloging, lifecycle, data models + schema evolution | 01, 03 |
| 3 | **Data Operations and Support** | **22%** | Automate with AWS services, analyze data, monitor pipelines, data quality | 03, 04 |
| 4 | **Data Security and Governance** | **18%** | Authentication, authorization, encryption/masking, audit logs, data privacy/governance | 05 |

Weights are from *AWS DEA-C01 Exam Guide, Content outline*. Domain task breakdown with skill numbers is at pages 5-13 of the guide.

### Domain 1 task statements
- **1.1** Perform data ingestion (streaming + batch sources, schedulers, event triggers, throttling, replay). *Exam Guide, Task 1.1*.
- **1.2** Transform and process data (containers, connectors, format conversion, cost). *Task 1.2*.
- **1.3** Orchestrate data pipelines (Lambda, EventBridge, MWAA, Step Functions, Glue workflows, SNS/SQS alerts). *Task 1.3*.
- **1.4** Apply programming concepts (Python/SQL, IaC with CFN/CDK/SAM, CI/CD, distributed computing). *Task 1.4*.

### Domain 2 task statements
- **2.1** Choose a data store (Redshift, EMR, Lake Formation, RDS, DynamoDB, KDS, MSK, Iceberg, vector indexes). *Task 2.1*.
- **2.2** Understand data cataloging systems (Glue Data Catalog, Hive metastore, crawlers, SageMaker Catalog). *Task 2.2*.
- **2.3** Manage data lifecycle (S3 <-> Redshift load/unload, S3 Lifecycle, versioning, DynamoDB TTL). *Task 2.3*.
- **2.4** Design data models and schema evolution (Redshift/DynamoDB/Lake Formation schemas, SCT, DMS Schema Conversion, lineage, indexing/partitioning). *Task 2.4*.

### Domain 3 task statements
- **3.1** Automate processing (MWAA, Step Functions, EMR/Redshift/Glue features, DataBrew, Athena, Lambda, EventBridge). *Task 3.1*.
- **3.2** Analyze data (QuickSight, DataBrew, Athena, Redshift SQL, Athena Spark notebooks, provisioned vs. serverless trade-offs). *Task 3.2*.
- **3.3** Maintain and monitor pipelines (CloudWatch Logs, CloudTrail, Logs Insights, OpenSearch, troubleshooting). *Task 3.3*.
- **3.4** Ensure data quality (DataBrew rules, sampling, skew). *Task 3.4*.

### Domain 4 task statements
- **4.1** Apply authentication (VPC SGs, IAM roles/groups/policies, Secrets Manager, S3 Access Points, PrivateLink). *Task 4.1*.
- **4.2** Apply authorization (custom IAM policies, Parameter Store, Redshift DB users, **Lake Formation permissions for Redshift/EMR/Athena/S3**, RBAC/TBAC/ABAC, least privilege). *Task 4.2*.
- **4.3** Ensure data encryption and masking (KMS, cross-account encryption, in-transit). *Task 4.3*.
- **4.4** Prepare logs for audit (CloudTrail, CloudWatch Logs, CloudTrail Lake, Athena/Insights/OpenSearch for log analysis). *Task 4.4*.
- **4.5** Data privacy and governance (Redshift data sharing, Macie + Lake Formation for PII, AWS Config, SageMaker Catalog projects). *Task 4.5*.

## Target candidate (who should take this exam)

- **Experience:** 2-3 years data engineering, 1-2 years hands-on AWS. *Exam Guide, Target Candidate Description*.
- **Assumes knowledge of:** ETL setup, Git, data lakes, networking/storage/compute concepts, vectors. *Exam Guide, Recommended general IT knowledge*.
- **Assumes AWS knowledge of:** encryption/governance/logging, cost/performance comparisons between services, SQL on AWS, data quality/consistency. *Exam Guide, Recommended AWS knowledge*.
- **Out of scope** (will not be tested): ML training/inference, language-specific syntax, business conclusions. *Exam Guide, Job tasks that are out of scope*.

## In-scope services (high-level)

The guide lists in-scope services by category (analytics, app integration, cloud financial management, compute, containers, database, developer tools, ML, mgmt & governance, migration/transfer, networking, security, storage). *Exam Guide, In-Scope AWS Services, pp. 13-18*. Key analytics services: Athena, EMR, Glue, Glue DataBrew, Lake Formation, Kinesis Data Firehose, Kinesis Data Streams, Managed Service for Apache Flink, MSK, OpenSearch Service. *Exam Guide, Analytics, p. 14*.

## Recommended prep order

1. **Module 00** — this file. Anchor the domain weightings.
2. **Module 01** (storage, 26%) — because everything else lands in or reads from S3.
3. **Module 02** (ingestion, part of the 34%) — the largest domain.
4. **Module 03** (compute/analytics, 34% + 22%) — overlaps Domains 1 and 3.
5. **Module 04** (orchestration) — small surface, high exam value.
6. **Module 05** (security, 18%) — smallest domain but every question is dense.
7. **Module 06** (FinOps) — cross-cutting; ties into Skill 1.2.4 "Optimize costs while processing data".
8. Mock exams from [mock_exam_sources.md](../mock_exam_sources.md).

## Booking logistics

1. Create an account at the [AWS Certification portal](https://www.aws.training/certification).
2. Schedule through the portal; exams are delivered by **Pearson VUE** at test centers or **OnVUE** online proctored. See [AWS Certification Policies - Before Testing](https://aws.amazon.com/certification/policies/before-testing/).
3. Review the [AWS Certification Exam Retake Policy](https://aws.amazon.com/certification/policies/before-testing/) before booking.
4. If you fail, there is no penalty for guessing, so answer every question. *Exam Guide, Response types*.

## References

See [references.md](./references.md).

## Checkpoint

- [ ] You can recite the 4 domain weightings (34/26/22/18).
- [ ] You have read pages 1-13 of the exam guide PDF.
- [ ] You have an AWS Certification portal account.
- [ ] You have scheduled a practice exam window 4-6 weeks out.
