# Quiz — 05 IAM Primer

10 multiple-choice questions. Answer key at the bottom.

---

**1.** Which four elements together form every IAM authorization decision?
- A) User, password, MFA, region
- B) Principal, action, resource, condition
- C) Role, policy, tag, timestamp
- D) Identity, group, permission, boundary

**2.** In AWS policy evaluation, what beats everything else?
- A) An allow in the identity policy
- B) An allow in a resource-based policy
- C) An explicit deny in any applicable policy
- D) A permissions boundary that grants the action

**3.** A Lambda function in Account A must read an S3 object in Account B. Which statement is correct?
- A) Only Account B's bucket policy needs to allow it
- B) Only Account A's execution role needs to allow it
- C) Both Account A's role AND Account B's bucket policy must allow it
- D) An SCP in Account A is sufficient

**4.** What is the difference between a role's trust policy and its permission policy?
- A) Trust policy defines who can assume the role; permission policy defines what the role can do once assumed
- B) Trust policy is evaluated first; permission policy is evaluated last
- C) Trust policy is optional; permission policy is mandatory
- D) They are the same document with different names

**5.** Which condition key should pin a GitHub Actions OIDC trust policy to a specific repository and branch?
- A) `aws:SourceIp`
- B) `token.actions.githubusercontent.com:sub`
- C) `aws:PrincipalTag/repo`
- D) `sts:ExternalId`

**6.** What is the recommended method for applying least privilege?
- A) Start from `Action: "*"` and remove permissions as you find them unused
- B) Copy the AWS-managed `AdministratorAccess` policy and edit it
- C) Start from implicit deny and add the minimum allows needed, one capability per statement
- D) Grant `ReadOnlyAccess` to everyone and escalate per ticket

**7.** Which is the strongest indicator of an over-permissive policy?
- A) A policy with multiple `Sid` fields
- B) `"Resource": "*"` on an action that supports resource-level permissions
- C) A policy under 2 KB in size
- D) Use of `"Effect": "Allow"`

**8.** A role has an identity policy allowing `dynamodb:PutItem` on a table, but a permissions boundary attached to the role only allows `s3:*`. What happens when the role tries to `PutItem`?
- A) Allowed — identity policy wins
- B) Denied — effective permissions are the intersection of identity policy and boundary
- C) Allowed — boundaries only apply to users, not roles
- D) Denied — DynamoDB requires a resource-based policy

**9.** Which LocalStack environment variable set is sufficient to practise IAM policy writing with S3 and role assumption?
- A) `SERVICES=lambda,ec2`
- B) `SERVICES=iam,s3,sts`
- C) `SERVICES=kms,secretsmanager`
- D) `SERVICES=all` is always required

**10.** You see `"Principal": {"AWS": "*"}` in an S3 bucket policy, gated only by `aws:SourceIp`. What is the main risk?
- A) The policy will be rejected by AWS as invalid
- B) Any IP in the range can access the bucket without authenticating as a known principal, and IP conditions are weaker than principal pinning
- C) CloudTrail will not log the requests
- D) It will incur additional KMS charges

---

## Answer key

1. **B** — Principal, action, resource, condition. Ref: [AWS IAM identity overview](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_identity-management.html).
2. **C** — Explicit deny wins unconditionally. Ref: [AWS Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html); `../aws_certified/docs/week-10-security-governance.md:L60-L62`.
3. **C** — Cross-account requires both sides to allow. Ref: `../aws_certified/docs/week-10-security-governance.md:L118-L165`.
4. **A** — Trust vs. permission split. Ref: [IAM roles terms and concepts](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html).
5. **B** — The `sub` claim carries `repo:owner/name:ref:refs/heads/branch`. Ref: [GitHub OIDC for AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services).
6. **C** — Add minimum allows, one capability per statement. Ref: `../aws_certified/labs/week-10-lab-security.md:L57-L116`.
7. **B** — Wildcard resource on an action that supports resource-level permissions is the classic over-grant. Ref: [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).
8. **B** — Effective permissions = identity policy ∩ boundary. Ref: `../aws_certified/labs/week-10-lab-security.md:L217-L248`.
9. **B** — `iam,s3,sts` is the minimum set for this module's lab. Ref: [LocalStack IAM docs](https://docs.localstack.cloud/user-guide/aws/iam/).
10. **B** — `Principal: *` makes the bucket effectively anonymous from any source in the allowed IP range; pin principals explicitly. Ref: [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).
