# Module 05: IAM Primer — Identity, Policy, and Least Privilege (5h)

> Vendor-neutral IAM foundations with offline hands-on practice on LocalStack. The concepts here transfer directly to Azure RBAC and GCP IAM; the syntax shown is AWS because it is the most explicit and the easiest to test locally.

## Learning goals
- Explain the four pieces of every authorization decision: principal, action, resource, condition.
- Walk through AWS policy evaluation order and predict the outcome for a given request.
- Distinguish identity-based from resource-based policies and pick the right one for a cross-account scenario.
- Write a least-privilege policy by starting from implicit deny and adding the minimum allows.
- Obtain short-lived credentials via `sts:AssumeRole`, including from GitHub Actions using OIDC.
- Spot the three most common policy mistakes in a code review.

## Prerequisites
- `../04_cloud_concepts/` (shared responsibility, IAM vs. network control plane)
- Docker Desktop or Colima for LocalStack
- `awslocal` CLI (`pip install awscli-local`)

## Reading order
1. This README
2. `labs/lab_iam_localstack/README.md`
3. `quiz.md`

## Concepts

### The IAM mental model: principal, action, resource, condition
Every authorization decision answers one question: "Is this **principal** allowed to perform this **action** on this **resource** under these **conditions**?" A principal is whoever is making the request — a human user, an application, or an AWS service acting on someone's behalf. The action is an API operation (`s3:GetObject`, `dynamodb:PutItem`). The resource is the ARN the action targets. Conditions are extra tests on request context such as source IP, MFA presence, or tag equality. If you can name those four things for a request, you can reason about any IAM decision. Ref: [AWS IAM Identities and Policies overview](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_identity-management.html).

### Policy evaluation: explicit deny > allow > implicit deny
AWS evaluates policies in a fixed order, and the rule every engineer must memorise is: an **explicit deny in any applicable policy always wins**, an **allow** is required somewhere for the request to succeed, and if no statement matches the request is **implicitly denied**. The full order inside a single account is: explicit deny anywhere → SCPs → resource-based policy → permissions boundary → session policy → identity-based policy. Ref: [AWS Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) and `../aws_certified/docs/week-10-security-governance.md:L24-L68` for the evaluation diagram and six-policy-type table that this module reuses.

### Identity-based vs. resource-based policies
An **identity-based** policy is attached to a principal (user, group, or role) and answers "what can this identity do?" A **resource-based** policy is attached to a resource (S3 bucket, KMS key, SQS queue, Lambda function, Secrets Manager secret) and answers "who can touch this resource?" For same-account requests, either one allowing is enough. For cross-account requests, **both** sides must allow — the resource policy must name the external principal and the identity policy in the other account must allow the action. This two-sided handshake is why cross-account access feels harder than it should: people remember one side and forget the other. Ref: [AWS Identity-based vs resource-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html); policy type table at `../aws_certified/docs/week-10-security-governance.md:L15-L22`.

### Trust policies vs. permission policies
A role has **two** policies attached, and confusing them is the single most common IAM debugging rabbit hole. The **trust policy** (also called `AssumeRolePolicyDocument`) answers "who is allowed to **assume** this role?" The **permission policy** answers "once assumed, what can the role do?" A role with a perfect permission policy but a broken trust policy is unusable — nobody can become it. The trust policy is itself a resource-based policy where the resource is the role. Ref: [IAM roles terms and concepts](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html); Glue service role example at `../aws_certified/labs/week-10-lab-security.md:L40-L53`.

### Short-lived credentials with STS and OIDC
Long-lived access keys are the number-one source of cloud breaches. The modern replacement is `sts:AssumeRole`, which hands back a triplet (access key ID, secret, session token) that expires in 15 minutes to 12 hours. For CI/CD, the preferred pattern is **OIDC federation**: GitHub Actions (or GitLab, or any OIDC provider) presents a short-lived JWT to AWS STS, STS validates it against a registered OIDC provider, and the workflow receives temporary credentials scoped to a role whose trust policy pins the exact repository and branch. No static secret ever exists. Ref: [AWS STS AssumeRole](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html) and [Configuring OpenID Connect in Amazon Web Services](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services).

### Applying least privilege in practice
"Least privilege" is a slogan until you have a method. The method is: **start from implicit deny and add the minimum allows needed for the job to succeed**. Do not start from `*` and remove things — you will miss something and leave a hole. The concrete workflow is (1) list the exact API calls your workload makes; (2) write one `Allow` statement per logical capability, each scoped to specific resource ARNs; (3) run the workload against the policy and fix `AccessDenied` errors one by one until it works; (4) use Access Analyzer or CloudTrail `ErrorCode=AccessDenied` events to catch calls you missed. The reference Glue-job least-privilege policy at `../aws_certified/labs/week-10-lab-security.md:L61-L116` illustrates the shape: one `Sid` per capability, explicit resource ARNs, no wildcards on `Resource`.

### Common mistakes
Three mistakes show up in almost every IAM review:
1. **`"Resource": "*"`** on an action that supports resource-level permissions. If the docs list resource types for the action, name them explicitly.
2. **Wildcard `Action` without conditions** — `"Action": "s3:*"` on a bucket policy is almost always wrong. At minimum, gate it with a condition like `aws:PrincipalOrgID` or `aws:SourceVpce`.
3. **Overly broad principal matches in trust policies** — `"Principal": {"AWS": "*"}` with only a `sts:ExternalId` condition is weaker than most people think; pin the full principal ARN and keep the external ID.
Supporting material: Glue role pattern at `../aws_certified/labs/week-10-lab-security.md:L61-L116`; permissions boundary intersection example at `../aws_certified/labs/week-10-lab-security.md:L217-L248`.

### LocalStack for offline practice
LocalStack runs a mock AWS cloud in a single Docker container and implements IAM, STS, S3, and most other services well enough to practise policy writing without spending money or waiting for real API throttles. The community image is free and starts in under ten seconds. For IAM practice specifically, `SERVICES=iam,s3,sts` is enough. The `awslocal` wrapper injects `--endpoint-url=http://localhost:4566` so your commands look like normal AWS CLI calls. Ref: [LocalStack Getting Started](https://docs.localstack.cloud/getting-started/) and [LocalStack IAM coverage](https://docs.localstack.cloud/user-guide/aws/iam/).

### Vendor-neutral note
Azure RBAC uses role assignments with scope (management group / subscription / resource group / resource) and role definitions (actions + not-actions). GCP IAM uses bindings of member → role → resource. Both follow the same principal-action-resource-condition model and both support explicit deny (Azure deny assignments, GCP deny policies) layered over allow. If you understand the AWS evaluation flow, the other two are a syntax swap.

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_iam_localstack` | Write and test a least-privilege S3 read-only policy against LocalStack with positive and negative assertions | 75m | [labs/lab_iam_localstack/](labs/lab_iam_localstack/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `AccessDenied` despite allow in identity policy | Explicit deny in SCP, permissions boundary, or resource policy | Walk the full evaluation order; check all six policy types | `../aws_certified/docs/week-10-security-governance.md:L60-L68` |
| Role exists but `AssumeRole` fails | Trust policy missing or principal not listed | Edit `AssumeRolePolicyDocument`, confirm principal ARN is exact | `../aws_certified/labs/week-10-lab-security.md:L40-L53` |
| Cross-account access denied | Only one side (identity or resource policy) allows it | Add allow to both the caller's identity policy AND the resource-based policy | `../aws_certified/docs/week-10-security-governance.md:L122-L165` |
| Policy works in LocalStack but fails in real AWS | LocalStack community edition does not fully enforce IAM by default | Treat LocalStack as a syntax and logic sandbox; validate in a real sandbox account before prod | [LocalStack IAM docs](https://docs.localstack.cloud/user-guide/aws/iam/) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Name the four components of an authorization decision and apply them to a real request you made today.
- [ ] Predict the outcome of a request given identity policy, resource policy, and SCP snippets.
- [ ] Write a least-privilege policy granting read-only access to one S3 prefix and nothing else.
- [ ] Explain the difference between a role's trust policy and its permission policy in one sentence each.
- [ ] Configure a GitHub Actions workflow that uses OIDC instead of static access keys.
- [ ] List three common policy mistakes and show how to fix each.
