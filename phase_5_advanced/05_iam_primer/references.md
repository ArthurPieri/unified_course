# References — 05 IAM Primer

## Primary docs
- [AWS IAM User Guide — Identity management overview](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_identity-management.html) — principal/action/resource/condition model.
- [AWS IAM — Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) — canonical source for explicit deny > allow > implicit deny and the full order of policy types.
- [AWS IAM — Identity-based vs. resource-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html) — same-account vs. cross-account evaluation rules.
- [AWS IAM — Roles terms and concepts](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) — trust policy vs. permission policy.
- [AWS STS — Requesting temporary security credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html) — `sts:AssumeRole`, session duration, session tags.
- [GitHub Docs — Configuring OpenID Connect in AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) — OIDC trust policy patterns for CI/CD.
- [LocalStack — Getting Started](https://docs.localstack.cloud/getting-started/) — install, single-container startup.
- [LocalStack — IAM coverage](https://docs.localstack.cloud/user-guide/aws/iam/) — what IAM features are emulated and the enforcement caveats.
- [LocalStack — S3 service](https://docs.localstack.cloud/user-guide/aws/s3/) — used in the lab for prefix-scoped read-only testing.
- [LocalStack — STS service](https://docs.localstack.cloud/user-guide/aws/sts/) — `AssumeRole` behaviour in LocalStack.

## AWS official sources (concepts adapted from)
- [AWS IAM policy types](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) — six IAM policy types; foundation for the identity-based vs. resource-based discussion.
- [AWS Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) — policy evaluation diagram and key principles; reused in concept section.
- [AWS cross-account access](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies-cross-account-resource-access.html) — cross-account access patterns (resource policy vs. AssumeRole); referenced in the common-failures table.
- [LocalStack Getting Started](https://docs.localstack.cloud/getting-started/) — LocalStack Docker startup pattern adapted for the module lab.
- [AWS Glue — Setting up IAM permissions](https://docs.aws.amazon.com/glue/latest/dg/getting-started-access.html) — Glue trust policy example cited for trust vs. permission distinction.
- [AWS Glue security best practices](https://docs.aws.amazon.com/glue/latest/dg/security-best-practices.html) — reference least-privilege identity policy; cited as the canonical shape.
- [AWS IAM permissions boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) — permissions boundary intersection example; used in the common-mistakes discussion.

## Canonical book
- *Fundamentals of Data Engineering*, Reis & Housley, Ch. 10 — security and access control foundations.
