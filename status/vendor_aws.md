# Vendor AWS Branch — Build Status

Last updated: 2026-04-10
Target certification: **DEA-C01** (AWS Certified Data Engineer – Associate)

## Modules
- [x] 00_exam_profile — drafted 2026-04-10 (DEA-C01 4 domains 34/26/22/18; 50 scored + 15 unscored; 720 pass)
- [x] 01_storage_s3_lakeformation — drafted 2026-04-10 (S3 classes, Lake Formation, Glue Catalog)
- [x] 02_ingestion_glue_dms_kinesis — drafted 2026-04-10 (Glue, DMS, DataSync, AppFlow, Kinesis, MSK)
- [x] 03_compute_emr_athena_redshift — drafted 2026-04-10 (EMR, Athena, Redshift, Glue ETL)
- [x] 04_orchestration_mwaa_stepfunctions — drafted 2026-04-10 (MWAA, Step Functions, EventBridge)
- [x] 05_security_iam_kms — drafted 2026-04-10 (IAM, KMS, VPC endpoints, Macie, Secrets Manager)
- [x] 06_cost_finops — drafted 2026-04-10

## Artifacts
- [x] vendors/aws/README.md (branch hub with 12-week plan)
- [x] vendors/aws/references.md (branch-wide AWS docs index)
- [x] vendors/aws/mock_exam_sources.md (links only; no fabricated questions)

## Decisions recorded
- Primary source: AWS official documentation (replaced sibling citations with doc links)
- Exam guide PDF revision reads © 2026; newer in-scope services include SageMaker Catalog, Bedrock knowledge bases, HNSW/IVF vector indexes
- Exam duration not in exam guide PDF — flagged for AWS Certification product page re-verify
- `vendors/aws/labs/` directory left empty — labs live inline per-module; AWS official docs and tutorials are the reference

## Blockers
none

## Next action
Stage 10: appendices + master references merge
