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

## Sibling reuse source
- `../../../aws_certified/docs/week-10-security-governance.md:L9-L223` — IAM, policy evaluation, RBAC/ABAC framing.
- `../../../aws_certified/docs/week-10-security-governance.md:L274-L325` — column-level, row-level, and cell-level security patterns.
- `../../../aws_certified/docs/week-10-security-governance.md:L664-L728` — masking vs tokenization vs hashing vs encryption comparison.
- `../../../aws_certified/docs/week-10-security-governance.md:L731-L826` — audit logging and the centralized audit pattern.
- `../../../aws_certified/docs/week-10-security-governance.md:L828-L920` — data privacy, classification, GDPR framing, secrets.

## Book
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 10 — batch processing, immutability, and consequences for deletion.
