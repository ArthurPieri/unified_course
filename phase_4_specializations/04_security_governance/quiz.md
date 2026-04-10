# Module 04 Quiz — Security and Governance

Ten multiple-choice questions. Answer key at the bottom.

---

**1.** An analyst needs to join two tables on `email` across systems without ever seeing the cleartext address. Which technique fits best?

A. Dynamic masking (`left(email,2) || '***'`)
B. Deterministic keyed HMAC hash of `email` applied in both systems with the same key
C. KMS envelope encryption of `email`
D. Drop the email column

**2.** Which statement about **masking** is correct?

A. Masking rewrites the data on disk
B. Masking is a display-time control enforced by the query engine
C. Masking is reversible with the right key
D. Masking replaces tokenization for PCI-DSS

**3.** In a Trino `rules.json` column mask, the expression is evaluated:

A. Once at rule load time and cached
B. By the client driver
C. By Trino on every query that selects the column, substituted into the projection
D. By the underlying Iceberg connector at compaction

**4.** Which scenario favors **ABAC** over RBAC?

A. Five roles, one region, stable over years
B. Permissions must differ by (department × sensitivity × region) producing hundreds of role combinations
C. A single DPO account that reads everything
D. Read-only demo environment

**5.** A **data contract** in dbt primarily enforces what, and when?

A. Runtime row-count thresholds, at query time
B. Column names, data types, and constraints at `dbt build`
C. Encryption of the underlying files, at compaction
D. Row-level access, at query time

**6.** A user is granted `SELECT` on a table with a row filter `region = current_user`. A query returns zero rows. Why?

A. The filter silently dropped all rows because the user's name does not match any region value
B. Trino refused to run the query
C. Row filters only apply to aggregates
D. The table is empty

**7.** Under GDPR, a subject requests erasure. Your base table is Iceberg with one year of snapshots. Minimally, which steps make erasure complete?

A. `DELETE FROM base WHERE subject_id = ?`
B. `DELETE FROM base WHERE subject_id = ?` + expire snapshots + remove orphan files
C. Add the subject to an `erasure_requests` table only
D. Drop the base table

**8.** What does a **lineage graph** answer that an **audit trail** cannot?

A. Who ran a query yesterday
B. Which downstream reports depend on a specific source field
C. Whether a login attempt failed
D. The timestamp of a GRANT statement

**9.** You need to store credit card numbers so an analytics job can still join rows by card across datasets, and the legal team must be able to recover the original values. Choose:

A. SHA-256 hashing
B. Dynamic masking
C. Vault-backed tokenization
D. Drop the column

**10.** The minimal audit event for a sensitive SELECT should include:

A. Only the username
B. Principal, action, resource (with columns), timestamp, outcome, and — for sensitive tables — the query text
C. Only the timestamp and table name
D. Principal and row count only

---

## Answer key

1. **B** — a shared keyed HMAC gives a deterministic pseudonym that joins but is not reversible from the hash alone. Ref: masking techniques table, `aws_certified/docs/week-10-security-governance.md:L718-L728`.
2. **B** — masking is a display/projection-time control; the underlying bytes are unchanged. Ref: module concepts, Trino FBAC docs.
3. **C** — Trino evaluates mask expressions per query as part of projection. Ref: [Trino FBAC](https://trino.io/docs/current/security/file-system-access-control.html).
4. **B** — role explosion is the classic ABAC trigger. Ref: [AWS IAM — ABAC](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html).
5. **B** — dbt contracts are build-time checks on columns, types, and constraints. Ref: [dbt contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts).
6. **A** — row filters are SQL predicates; a non-matching predicate yields an empty result. Ref: Trino FBAC.
7. **B** — Iceberg deletes are only physical after snapshot expiry and orphan cleanup. Ref: [Iceberg Maintenance](https://iceberg.apache.org/docs/latest/maintenance/).
8. **B** — lineage is a dependency graph; audit trails record events. Ref: [OpenLineage spec](https://openlineage.io/docs/spec/object-model), dbt lineage docs.
9. **C** — tokenization is format-preserving, joinable, and reversible via vault — the standard PCI choice. Ref: masking techniques table, `aws_certified/docs/week-10-security-governance.md:L718-L728`.
10. **B** — principal/action/resource/time/outcome plus query text for sensitive tables. Ref: `aws_certified/docs/week-10-security-governance.md:L731-L826`.
