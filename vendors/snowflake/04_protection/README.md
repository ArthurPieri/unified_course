# Module 04: Data Protection — Time Travel, Fail-safe, Cloning, Replication

Snowflake bundles recovery, dev-environment provisioning, and DR under **Continuous Data Protection (CDP)**. On Platform it is Domain 4.0 (10%), on Core Domain 6.0 (12%), and on DEA Domain 3.0 (14%) where recovery interacts with streams and clustering.

## Learning goals
- Define Time Travel and state the default and maximum `DATA_RETENTION_TIME_IN_DAYS` per table type and edition.
- Explain how Fail-safe differs from Time Travel, and who can access it.
- Use `CLONE` to provision dev environments and describe permission inheritance on clones.
- Describe database replication (primary -> secondary) and failover groups.
- Explain Tri-Secret Secure and what layer it applies to.

## Prerequisites
- `../01_architecture/` — micro-partitions and storage layer.
- `../03_access/` — role context for clone grants.

## Reading order
1. This README
2. [Snowflake Data Protection](https://docs.snowflake.com/en/user-guide/data-time-travel) — CDP, Time Travel, Fail-safe, cloning
3. [Snowflake Quickstarts](https://quickstarts.snowflake.com/) — data protection hands-on labs
4. `quiz.md`

## Concepts

### Time Travel
Time Travel lets you query, clone, or restore data **as of a past point in time** using `AT(TIMESTAMP => ...)`, `AT(OFFSET => -60)`, `AT(STATEMENT => 'qid')`, or `BEFORE(STATEMENT => 'qid')`. Retention is controlled by `DATA_RETENTION_TIME_IN_DAYS` set at account, database, schema, or table level. Defaults: **1 day** for Standard edition, **up to 90 days** for Enterprise edition and above. Permanent tables support the full configured range; transient and temporary tables support **0 or 1 day** only.

Ref: [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel) · *SnowPro Associate: Platform Study Guide, §4.1, p. 8* · [Snowflake Data Protection](https://docs.snowflake.com/en/user-guide/data-time-travel).

### Fail-safe
Fail-safe is a **7-day** non-configurable period after Time Travel expires, during which Snowflake Support — **not the customer** — can recover data in the event of catastrophic failure. Fail-safe applies only to permanent tables. Transient and temporary tables have no Fail-safe. You cannot query Fail-safe data yourself and you cannot disable it.

Ref: *SnowPro Core Study Guide, Domain 6.0, p. 12* · `domain_4_0_data_protection.md:L19-L45`.

### Zero-copy cloning
`CREATE TABLE dev_customers CLONE prod.public.customers;` creates a new object that shares the underlying micro-partitions until either side diverges. Clones are **instant and take no additional storage** at clone time. Cloning a database clones all schemas, tables, and most child objects. Cloned objects **inherit no grants by default** — privileges must be re-applied (a clone is a new object with a new owner).

Ref: [Cloning considerations](https://docs.snowflake.com/en/user-guide/object-clone) · *Core Study Guide Domain 6.0, p. 12* · [Snowflake Quickstarts](https://quickstarts.snowflake.com/).

### Replication and failover
**Database replication** creates a read-only secondary in another account (possibly another region/cloud). **Account replication** replicates account-level objects (users, roles, warehouses, shares). **Failover groups** bundle databases and account objects so you can promote an entire secondary in one command (`ALTER FAILOVER GROUP ... PRIMARY`). Cross-region replication is an Enterprise+ feature; cross-cloud replication requires Business Critical or higher for some object types.

Ref: [Database replication & failover](https://docs.snowflake.com/en/user-guide/account-replication-intro) · *DEA Study Guide, §3.1, p. 8*.

### Tri-Secret Secure
Tri-Secret Secure combines a **customer-managed key** (in AWS KMS, Azure Key Vault, or GCP KMS) with Snowflake's own key to produce a composite master key. Data is encrypted with the composite key; revoking the customer key renders data unreadable. Available only in **Business Critical** edition. Applies to data at rest in the storage layer.

Ref: [Tri-Secret Secure](https://docs.snowflake.com/en/user-guide/security-encryption-manage) · *Core Study Guide Domain 6.0 / Domain 2.0, pp. 7, 12*.

### UNDROP
`UNDROP TABLE|SCHEMA|DATABASE` restores a dropped object within its Time Travel window. After the Time Travel window expires, UNDROP fails — Fail-safe is recoverable only by Snowflake Support.

Ref: [UNDROP TABLE](https://docs.snowflake.com/en/sql-reference/sql/undrop-table) · [Snowflake Quickstarts](https://quickstarts.snowflake.com/).

## Hands-on drills

| # | Drill | Est. time | Source |
|---|---|---|---|
| D1 | Set `DATA_RETENTION_TIME_IN_DAYS = 2`, update a row, query the table `BEFORE(STATEMENT => <qid>)` and verify the old value. | 25 min | `lab_05_data_protection.sql` Sections 1-3 |
| D2 | Drop a table and `UNDROP` it. Drop again after retention expires and confirm the UNDROP fails. | 20 min | `lab_05_data_protection.sql` Section 4 |
| D3 | Clone a database with `CREATE DATABASE dev CLONE prod;` and modify a single table on the clone; confirm the original is untouched. | 25 min | `lab_05_data_protection.sql` Section 5 |
| D4 | Configure database replication to a secondary account (or simulate with a second database) and force a failover simulation. | 45 min | [Replication](https://docs.snowflake.com/en/user-guide/account-replication-intro) |
| D5 | Inspect `TABLE_STORAGE_METRICS` to see active bytes, Time Travel bytes, Fail-safe bytes for a table. | 15 min | *DEA Study Guide §3.1, p. 8* |

## Common failures (exam gotchas)

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| "Fail-safe gives me 7 more queryable days" | False | Fail-safe is not self-service. Only Snowflake Support can restore from Fail-safe. | `domain_4_0_data_protection.md:L34-L45` |
| "Transient tables support 90-day Time Travel" | False | Transient/temporary tables support 0 or 1 day only. | [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel) |
| "Clones inherit all grants" | False | A clone is a new object — re-apply grants (or use `GRANT ... ON ALL TABLES`). | `domain_4_0_data_protection.md:L143-L160` |
| "Tri-Secret Secure encrypts in transit" | Wrong layer | Tri-Secret Secure is a composite-key scheme for data at rest. | [Encryption management](https://docs.snowflake.com/en/user-guide/security-encryption-manage) |
| "Replication copies warehouses and users automatically" | Incomplete | Use **account replication** or failover groups for account-level objects; database replication only covers the database. | [Account replication](https://docs.snowflake.com/en/user-guide/account-replication-intro) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] State the default and max Time Travel retention per edition and table type.
- [ ] Explain Fail-safe: who, how long, how accessed.
- [ ] Write a `CLONE` DDL and explain permission inheritance on the clone.
- [ ] Explain when to use database replication vs failover groups.
