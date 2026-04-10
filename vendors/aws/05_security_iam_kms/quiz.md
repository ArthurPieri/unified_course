# Module 05 Quiz — Security & Governance

10 questions. Answer key with cites.

---

**Q1.** Which statement about IAM policy evaluation is correct?

- A) Allow always wins when a resource policy allows it.
- B) An explicit Deny in any applicable policy always overrides any Allow.
- C) Permission boundaries grant permissions in addition to identity policies.
- D) SCPs only apply to root users.

**Q2.** You need a VPC endpoint for private access to S3 from EC2 instances in a VPC. Which endpoint type?

- A) Interface endpoint (PrivateLink)
- B) Gateway endpoint
- C) Transit Gateway
- D) NAT gateway

**Q3.** Which is the strongest recommendation to reduce KMS request costs for a high-volume S3 workload using SSE-KMS?

- A) Use SSE-S3 instead
- B) Enable S3 Bucket Keys
- C) Disable KMS key rotation
- D) Switch to customer-provided keys (SSE-C)

**Q4.** A Glue job needs to read from bucket `raw/` and write to DynamoDB table `curated_events`. Which IAM policy pattern is least-privileged?

- A) `AdministratorAccess` managed policy
- B) Action-level grants with resource ARNs scoped to `raw/*` and the specific DynamoDB table
- C) `AmazonS3FullAccess` + `AmazonDynamoDBFullAccess`
- D) A resource-based policy on the Glue service role

**Q5.** Which service automates rotation of an RDS PostgreSQL master password?

- A) Parameter Store standard tier
- B) AWS Secrets Manager with a rotation Lambda
- C) AWS Config managed rule
- D) KMS alias

**Q6.** You must identify PII objects in an S3 bucket on a schedule and trigger a workflow when findings appear. Which combination fits?

- A) GuardDuty + SNS
- B) Macie classification job + EventBridge rule on findings
- C) Athena query + Lambda
- D) S3 Inventory + SQS

**Q7.** A compliance requirement mandates an immutable, SQL-queryable audit store of all management API calls across the org. Best fit?

- A) CloudWatch Logs with metric filters
- B) CloudTrail Lake
- C) S3 with Object Lock
- D) AWS Config conformance pack

**Q8.** Which CloudTrail event type must be explicitly enabled and is billed per event?

- A) Management events
- B) Insights events
- C) Data events
- D) Service events

**Q9.** A Redshift cluster and an S3 bucket in another AWS account both use KMS CMKs. Which is required for the cluster role to decrypt objects?

- A) Only a KMS grant from the bucket's key owner
- B) Only an IAM policy allowing `kms:Decrypt`
- C) Both the key policy in the owning account AND the IAM policy in the using account must allow the action
- D) Nothing; KMS allows cross-account by default

**Q10.** What is the exam-canonical AWS service for rule-based data quality checks inside a data lake ETL job?

- A) AWS Config
- B) AWS Glue Data Quality (DQDL)
- C) Amazon Macie
- D) AWS Audit Manager

---

## Answer key

1. **B** — Explicit Deny wins everywhere. [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html).
2. **B** — S3 (and DynamoDB) use Gateway endpoints. [Gateway VPC endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html).
3. **B** — S3 Bucket Keys reduce KMS request volume substantially. [S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html).
4. **B** — Action-level grants scoped to specific resources. *AWS DEA-C01, Skill 4.2.6*; `../../../aws_certified/labs/week-10-lab-security.md:9-260`.
5. **B** — Secrets Manager with a rotation Lambda. [Secrets Manager rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html).
6. **B** — Macie classification jobs emit findings to EventBridge. [Macie findings](https://docs.aws.amazon.com/macie/latest/user/findings.html).
7. **B** — CloudTrail Lake stores events for SQL queries across the org. [CloudTrail Lake](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake.html).
8. **C** — Data events must be explicitly enabled and billed per event. [CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html).
9. **C** — Both the key policy and the IAM policy must allow the action for cross-account KMS. [KMS cross-account](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).
10. **B** — Glue Data Quality with DQDL. [Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html); *Exam Guide, Task 3.4*.
