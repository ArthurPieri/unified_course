# Module 04 — References

## Snowflake docs
- [Continuous Data Protection (CDP)](https://docs.snowflake.com/en/user-guide/data-cdp)
- [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel)
- [Fail-safe](https://docs.snowflake.com/en/user-guide/data-failsafe)
- [Cloning considerations](https://docs.snowflake.com/en/user-guide/object-clone)
- [UNDROP TABLE](https://docs.snowflake.com/en/sql-reference/sql/undrop-table)
- [Database replication & failover](https://docs.snowflake.com/en/user-guide/account-replication-intro)
- [Encryption management & Tri-Secret Secure](https://docs.snowflake.com/en/user-guide/security-encryption-manage)
- [TABLE_STORAGE_METRICS](https://docs.snowflake.com/en/sql-reference/account-usage/table_storage_metrics)

## Official study guides
- *SnowPro Associate: Platform Study Guide*, §4.1 "Outline continuous data protection with Snowflake", p. 8 — Time Travel, cloning, Marketplace.
- *SnowPro Core Study Guide*, Domain 6.0 "Data Protection and Data Sharing", p. 12 — Fail-safe, encryption, cloning, replication, failover.
- *SnowPro Advanced: Data Engineer Study Guide*, Domain 3.0 "Storage and Data Protection", p. 8 — recovery, cloning for dev, clustering interaction with Time Travel.

## Sibling reuse
- `../../../../snowflake_eng/phase1_platform/study_notes/domain_4_0_data_protection.md:L7-L250` — CDP, Time Travel, Fail-safe, cloning, Marketplace.
- `../../../../snowflake_eng/phase1_platform/labs/lab_05_data_protection.sql:L19-L330` — sections 1-9: retention, history, Time Travel, UNDROP, cloning, per-object retention, Marketplace, data share DDL.
