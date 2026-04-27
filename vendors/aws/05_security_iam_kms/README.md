# Module 05: Security — IAM, KMS, VPC endpoints, Macie, Secrets Manager (14h)

> Domain 4 (**18%**) of scored content. Every question is dense — this module repays deep study. *AWS DEA-C01 Exam Guide, Content outline*.

## Learning goals

- Write a least-privilege IAM policy with conditions (`aws:SourceVpce`, `aws:PrincipalTag`, `s3:prefix`). *Skill 4.1.5, 4.2.6*.
- Set up KMS envelope encryption for S3 (SSE-KMS), Redshift, EBS, and cross-account keys. *Skill 4.3.2, 4.3.3*.
- Use VPC endpoints (Gateway for S3/DynamoDB, Interface for other services) and PrivateLink. *Skill 4.1.1, 4.1.5*.
- Detect PII in S3 with Macie and quarantine via EventBridge + Lake Formation. *Skill 4.5.2*.
- Rotate database credentials with Secrets Manager or Parameter Store. *Skill 4.1.3, 4.2.2*.
- Prepare audit logs with CloudTrail (including CloudTrail Lake), CloudWatch Logs, and Config. *Skill 4.4.1-4.4.5, 4.5.4*.

## Exam weight

Domain 4 is 18% — nine scored questions out of fifty. Tasks 4.1 (authN), 4.2 (authZ), 4.3 (encryption), 4.4 (audit), 4.5 (privacy) are all in scope. *Exam Guide, Content Domain 4, pp. 11-13*.

## Key services and primary docs

| Service | What to know | AWS doc |
|---|---|---|
| AWS IAM | Identity-based and resource-based policies, trust policies, SCPs, permission boundaries, condition keys | [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) |
| AWS KMS | CMKs (AWS managed vs. customer managed), envelope encryption, key policies, grants, cross-account | [KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) |
| AWS Secrets Manager | Credential storage + rotation via Lambda | [Secrets Manager User Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html) |
| AWS Systems Manager Parameter Store | Cheaper config/secret store; no built-in rotation | [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) |
| VPC Endpoints / PrivateLink | Gateway endpoints (S3, DynamoDB), Interface endpoints (everything else) | [VPC endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html) |
| Amazon Macie | PII discovery in S3, scheduled and one-time jobs | [Macie User Guide](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html) |
| AWS CloudTrail | Management, data, and Insights events; CloudTrail Lake for SQL queries | [CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) |
| Amazon CloudWatch Logs | Log groups, metric filters, Logs Insights | [CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) |
| AWS Config | Resource configuration history and compliance rules | [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html) |

## Concepts (compact)

### IAM decision model
AWS evaluates: (1) Organizations SCPs, (2) resource-based policies, (3) identity-based policies, (4) permission boundaries, (5) session policies. An explicit Deny anywhere wins. For cross-account access the resource policy must grant the remote principal AND the remote principal's identity policy must allow the action. Primary: [IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html).

### Least privilege in practice
Use action-level grants (e.g., `s3:GetObject` only for `arn:aws:s3:::bucket/raw/*`), add `Condition` blocks for `aws:SourceVpce`, `aws:PrincipalTag`, `s3:prefix`, or `kms:ViaService`. IAM Access Analyzer finds unused permissions and overly broad policies. Primary: [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html), [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html). See the hands-on labs in this module's labs/ directory.

### KMS envelope encryption
Data keys encrypt data; the KMS CMK encrypts the data key. SSE-KMS on S3 and Redshift use this pattern. Customer-managed keys (CMKs) let you rotate annually, control the key policy, and require grants for cross-account and cross-service use. S3 Bucket Keys reduce KMS call cost by ~99% by caching a bucket-level data key. Primary: [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/), [S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html).

### VPC endpoints and PrivateLink
Gateway endpoints (free) route S3 and DynamoDB traffic without leaving the AWS backbone — add them to route tables. Interface endpoints (PrivateLink) are ENIs in your subnets for almost every other AWS service and partner SaaS; they cost per-hour-per-AZ + per-GB. Use `aws:SourceVpce` IAM conditions to deny access from outside your VPC. Primary: [VPC endpoints and PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html), [Gateway VPC endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html).

### Macie for PII discovery
Managed sensitive-data discovery on S3. Schedule jobs, configure custom data identifiers, and route findings to EventBridge to quarantine objects or trigger Lake Formation column-level restrictions. Primary: [Amazon Macie User Guide](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html).

### Secrets Manager vs. Parameter Store
Secrets Manager: automatic rotation via Lambda, cross-region replication, higher cost per secret. Parameter Store: free for standard tier, no built-in rotation, use `SecureString` with KMS. For RDS/Redshift credentials with rotation, Secrets Manager is the exam answer. *Skill 4.1.3*.

### Audit: CloudTrail + CloudTrail Lake + Config
CloudTrail logs API calls (management events by default; data events are opt-in and billed per event). CloudTrail Lake stores events as an immutable queryable store for SQL across the org. AWS Config tracks resource state over time and can enforce rules (e.g., "S3 buckets must be encrypted"). Primary: [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/), [CloudTrail Lake](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake.html), [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html).

### Data quality adjacency (Domain 3.4)
Glue Data Quality + DQDL rules are the exam answer for rule-based validation in data lakes; DataBrew rules for interactive quality. Primary: [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html).

## Labs

See the hands-on labs in this module's labs/ directory. Key exercises:

| Lab | Goal | AWS reference |
|---|---|---|
| IAM + Lake Formation + KMS | Least-privilege Glue job, Lake Formation permissions, KMS envelope | [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/), [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/) |
| CloudWatch + CloudTrail | Alarms, metric filters, structured logging | [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/), [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/) |
| Capstone | KMS keys, IAM roles, encrypted S3, encrypted Kinesis | [AWS Well-Architected Data Analytics Lens](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/) |

## Common exam gotchas

| Gotcha | Why it trips people | Reference |
|---|---|---|
| S3 column-level security | Lake Formation, not IAM bucket policies | *Exam Guide, Skill 4.2.4* |
| CloudTrail data events | Not logged by default; must be enabled and billed separately | [CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html) |
| Cross-account KMS | Requires key policy grant AND IAM policy allow on both sides | [KMS cross-account](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) |
| Gateway vs. Interface endpoints | S3 and DynamoDB are Gateway (route-table based, free); everything else is Interface (ENI, hourly) | [VPC endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html) |
| IAM explicit Deny | Explicit Deny beats any Allow, across any policy type | [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) |
| Secrets Manager rotation | Rotation is performed by a Lambda function you configure; not automatic for all engines | [Secrets Manager rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html) |

## References

See [references.md](./references.md).

## Checkpoint

- [ ] You can write a least-privilege IAM policy with `aws:SourceVpce` and `kms:ViaService` conditions.
- [ ] You can explain SSE-S3 vs. SSE-KMS vs. SSE-C and when each is the right answer.
- [ ] You can describe a Macie + EventBridge + Lake Formation quarantine pipeline.
