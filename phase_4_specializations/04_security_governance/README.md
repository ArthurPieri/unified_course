# Module 04: Security and Governance for Data Platforms (10h)

## Learning goals
- Classify PII and choose a protection technique (mask, tokenize, hash, encrypt) from the query and recovery requirements, not vibes.
- Configure **column masking** and **row-level filters** in Trino's file-based access control and reason about how the predicates are enforced.
- Contrast **RBAC** and **ABAC** and say when each scales better.
- Describe why **data lineage** and **audit trails** are separate, complementary controls and what each should capture.
- Use **dbt model contracts** as an enforceable governance boundary between teams.
- Design a **right-to-erasure** workflow on an immutable lakehouse without breaking snapshot consistency.

## Prerequisites
- `../../phase_3_core_tools/02_trino/` (Trino config basics)
- `../../phase_3_core_tools/05_dbt/` (dbt models and tests)
- `../03_semi_structured/` (Iceberg schema evolution — tombstoning builds on it)

## Reading order
1. This README
2. `labs/lab_L4b_pii_masking/README.md`
3. `quiz.md`

## Conceptual frame
The control stack for a data platform is four layers: **authentication** (who you are), **authorization** (what you may do), **encryption** (who can read the bytes), and **audit** (what actually happened). The same layers appear in every managed offering — Lake Formation, Snowflake, BigQuery — which is why learning them once transfers across vendors.
Ref: `../../../aws_certified/docs/week-10-security-governance.md:L9-L223` (IAM and authorization framing) · `:L731-L826` (audit logging and centralized audit pattern)

## Concepts

### PII classification and handling
PII (personally identifiable information) is any attribute that alone or in combination can identify a natural person. A workable classification for a data platform:

| Class | Examples | Typical handling |
|---|---|---|
| Direct identifiers | name, email, SSN, passport, phone | mask or tokenize by default; cleartext only for a named role |
| Quasi-identifiers | birth date, ZIP, gender | generalize (ZIP3, birth year) before combining |
| Sensitive attributes | health, financial balance, location trace | encrypt at rest + restrict by column |
| Non-PII | SKU, region code, event type | no restriction |

Ref: `../../../aws_certified/docs/week-10-security-governance.md:L664-L728` (masking techniques comparison and exam framing)

### Masking vs tokenization vs hashing vs encryption
All four replace cleartext with something else; they differ in **reversibility**, **format preservation**, and **what a downstream join can still do**.

| Technique | Reversible? | Format preserved? | Joinable on the transformed value? | Typical use |
|---|---|---|---|---|
| Dynamic masking (`'***-**-' \|\| right(ssn,4)`) | No — at display time | Yes | No (collisions) | Showing analysts partial values |
| Hashing (SHA-256, keyed HMAC) | No | No | Yes, deterministic | De-identified join keys, pseudonymous analytics |
| Tokenization (vault-backed surrogate) | Yes, via vault | Yes (format-preserving) | Yes | PCI-DSS, keeping referential integrity across systems |
| Encryption (KMS-managed key) | Yes, via key | No | No in general | At-rest protection, recoverable secrets |

Ref: `../../../aws_certified/docs/week-10-security-governance.md:L718-L728`

Masking is a **display** control — the data on disk is still cleartext, you are trusting the engine to apply the rule. Encryption is a **storage** control — even if the engine is bypassed, the bytes are opaque. They are not substitutes; a regulated platform uses both.

### Column masking and row-level security in Trino
Trino's file-based system access control uses a `rules.json` that pairs user/group patterns with per-table rules, including column masks and row filters. A **column mask** is a SQL expression that replaces the column's value in the output; a **row filter** is a SQL predicate appended to the query's WHERE clause.

```json
{
  "tables": [
    {
      "user": "analyst",
      "catalog": "iceberg",
      "schema": "sales",
      "table": "customers",
      "privileges": ["SELECT"],
      "columns": [
        { "name": "email", "mask": "to_hex(sha256(to_utf8(email)))" },
        { "name": "ssn",   "mask": "'***-**-' || substr(ssn, 8, 4)" }
      ],
      "filter": "region = current_user"
    }
  ]
}
```
Both masks and filters are evaluated by Trino for every query, so a user cannot bypass them by writing a different SQL statement.
Ref: [Trino — File-based access control (column masks and row filters)](https://trino.io/docs/current/security/file-system-access-control.html)

### RBAC vs ABAC
**RBAC** binds permissions to **roles** (analyst, dpo, engineer). It is easy to reason about and easy to audit but grows a combinatorial number of roles as dimensions multiply (role × region × product). **ABAC** binds permissions to **attributes** of the principal, resource, and environment via a policy expression (`principal.department == resource.owner_department AND resource.sensitivity <= principal.clearance`). It scales with cardinality but is harder to audit — the effective permission is computed, not listed.

A practical rule: start with RBAC for coarse grants, add ABAC predicates (row filters keyed on `current_user`, group tags) when roles would otherwise explode.
Ref: [AWS IAM User Guide — ABAC](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html) · `../../../aws_certified/docs/week-10-security-governance.md:L185-L223`

### Data lineage
Lineage is the graph of "which inputs produced this output". It answers two questions audit cannot answer alone: (1) if a source field is wrong, which downstream tables and reports are affected? (2) if a report shows a number, which source fields and transformations did it come from? Lineage is computed from SQL and orchestration metadata (dbt's `manifest.json`, OpenLineage events, Dagster asset graph); it is not the same as lineage logs in an audit trail, which record *who ran the query*, not *what it depends on*.
Ref: [dbt — Documentation and lineage](https://docs.getdbt.com/docs/collaborate/documentation) · [OpenLineage — Spec](https://openlineage.io/docs/spec/object-model)

### Audit trails: what to log, what to keep
An audit trail for a data platform should capture, at minimum: principal (user or role), action (SELECT, INSERT, GRANT, DROP), resource (catalog.schema.table and column list if possible), timestamp, source IP or session id, and outcome (success/denied). For sensitive tables, log the **query text** too — column-level access decisions depend on which columns the user actually asked for. Retention is a regulatory decision (PCI-DSS is one year online + additional archive; many GDPR programs target two to six years); align with counsel, not with the default.
Ref: `../../../aws_certified/docs/week-10-security-governance.md:L731-L826` (CloudTrail event types, centralized audit pattern)

### Data contracts as governance
A **data contract** is an explicit, versioned schema + semantics agreement between a producer (source system, upstream dbt project) and a consumer. dbt's **model contracts** enforce the contract at build time: if a downstream model declares a contract, dbt fails the build when column names, data types, or constraints drift. The contract turns schema changes from "noticed in Slack" into "failed CI".
Ref: [dbt — Model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts) · [dbt — Model versions](https://docs.getdbt.com/docs/collaborate/govern/model-versions)

### GDPR right-to-erasure on an immutable lakehouse
Iceberg, Delta, and Hudi are copy-on-write: historical snapshots keep deleted rows around for time travel. Literal erasure requires either rewriting the affected files or using a tombstoning strategy.

Pattern: **identifier tombstoning + scheduled rewrite**
1. Maintain an `erasure_requests(subject_id, requested_at)` table.
2. Every base table has a `subject_id` column.
3. At query time, join (or use a row filter) against `erasure_requests` so downstream views exclude erased subjects immediately. This satisfies the *access* aspect of erasure within SLA.
4. On a schedule (e.g., nightly), run a **MERGE/DELETE** against base tables filtered by `erasure_requests`, and then **expire old snapshots** so the cleartext rows cannot be recovered by time travel.
5. Log every step into the audit trail with the request ID.

Iceberg's `DELETE FROM` produces delete files; `expire_snapshots` and `remove_orphan_files` are the operations that physically remove data. Until snapshots are expired, time-travel reads can still see the deleted rows — erasure is not complete until expiry.
Ref: [Iceberg — Row-level deletes and DELETE FROM](https://iceberg.apache.org/docs/latest/spark-writes/#delete-from) · [Iceberg — Maintenance: expire snapshots](https://iceberg.apache.org/docs/latest/maintenance/#expire-snapshots)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L4b_pii_masking` | One Iceberg table, three Trino roles, three result sets; audit trail populated | 90m | [labs/lab_L4b_pii_masking/](labs/lab_L4b_pii_masking/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Masked column appears in cleartext for the wrong user | Mask rule ordering — the first matching user pattern wins | Reorder `rules.json` so specific rules precede wildcards | [Trino FBAC](https://trino.io/docs/current/security/file-system-access-control.html) |
| Deleted rows reappear after a few days | Time-travel snapshot still references them | Expire snapshots after DELETE | [Iceberg Maintenance](https://iceberg.apache.org/docs/latest/maintenance/#expire-snapshots) |
| Analyst joins on hashed email and gets no matches | Different salt/key on each side | Use a single keyed HMAC in a shared function | `../../../aws_certified/docs/week-10-security-governance.md:L718-L728` |
| dbt build breaks downstream after upstream schema change | No contract between the models | Add a model contract and pin a version | [dbt contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts) |
| Audit log exists but cannot answer "who read column X" | Only logs query metadata, not text | Log query text for sensitive schemas, redact on ingest if needed | `../../../aws_certified/docs/week-10-security-governance.md:L731-L826` |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Pick mask vs hash vs tokenize vs encrypt for three given scenarios and justify each in one sentence.
- [ ] Write a Trino `rules.json` fragment that masks two columns and adds a row filter for one role.
- [ ] Explain why RBAC with 50 roles is easier to audit than an equivalent ABAC policy — and why ABAC still wins past some threshold.
- [ ] Sketch a GDPR erasure workflow for an Iceberg lakehouse that includes snapshot expiry.
- [ ] Describe what a dbt model contract enforces and at which lifecycle step.
