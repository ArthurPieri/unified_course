# Module 04 References

## Trino
- [Trino — File-based system access control](https://trino.io/docs/current/security/file-system-access-control.html) — `rules.json` syntax for catalog/schema/table rules, **column masks**, and **row filters**.
- [Trino — Built-in access control overview](https://trino.io/docs/current/security/built-in-system-access-control.html) — how Trino evaluates authorization and where masks/filters sit in the flow.

## Iceberg
- [Iceberg — Row-level deletes: DELETE FROM](https://iceberg.apache.org/docs/latest/spark-writes/#delete-from) — row-level delete semantics.
- [Iceberg — Maintenance: expire snapshots and remove orphan files](https://iceberg.apache.org/docs/latest/maintenance/) — required to complete GDPR erasure.

## dbt
- [dbt — Model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts) — enforced columns, types, constraints at build time.
- [dbt — Model versions](https://docs.getdbt.com/docs/collaborate/govern/model-versions) — versioning a contracted model without breaking consumers.
- [dbt — Documentation and lineage](https://docs.getdbt.com/docs/collaborate/documentation) — manifest-driven lineage graph.

## Lineage
- [OpenLineage — Object model specification](https://openlineage.io/docs/spec/object-model) — run/job/dataset lineage events independent of orchestrator.

## Identity and access concepts
- [AWS IAM User Guide — Attribute-based access control (ABAC)](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html) — ABAC mental model, used here for concepts only (not AWS-specific).
- [AWS IAM User Guide — Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) — explicit deny > allow, useful framing for any policy engine.

## Canonical documentation sources
- [AWS IAM User Guide — Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) — IAM, policy evaluation, RBAC/ABAC framing.
- [AWS Lake Formation — Fine-grained access control](https://docs.aws.amazon.com/lake-formation/latest/dg/access-control-overview.html) — column-level, row-level, and cell-level security patterns.
- [AWS — Data masking best practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-data-masking/welcome.html) — masking vs tokenization vs hashing vs encryption comparison.
- [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) — audit logging and the centralized audit pattern.
- [AWS — Data classification](https://docs.aws.amazon.com/whitepapers/latest/data-classification/data-classification.html) — data privacy, classification, GDPR framing, secrets management.

## Book
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 10 — batch processing, immutability, and consequences for deletion.
