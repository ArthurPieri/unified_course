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

## Sibling sources (reuse-first)
- `../aws_certified/docs/week-10-security-governance.md:L9-L22` — six IAM policy types table; reused as the foundation for the identity-based vs. resource-based discussion.
- `../aws_certified/docs/week-10-security-governance.md:L24-L68` — policy evaluation diagram and key principles; reused verbatim in concept section.
- `../aws_certified/docs/week-10-security-governance.md:L118-L165` — cross-account access patterns (resource policy vs. AssumeRole); referenced in the common-failures table.
- `../aws_certified/labs/week-10-lab-security.md:L13-L36` — LocalStack Docker startup pattern adapted for the module lab.
- `../aws_certified/labs/week-10-lab-security.md:L40-L53` — Glue trust policy example cited for trust vs. permission distinction.
- `../aws_certified/labs/week-10-lab-security.md:L61-L116` — reference least-privilege identity policy; cited as the canonical shape.
- `../aws_certified/labs/week-10-lab-security.md:L217-L248` — permissions boundary intersection example; used in the common-mistakes discussion.

## Canonical book
- *Fundamentals of Data Engineering*, Reis & Housley, Ch. 10 — security and access control foundations.
