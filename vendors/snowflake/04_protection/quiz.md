# Module 04 — Quiz: Data Protection

10 questions. Key + citations at the bottom.

---

**1.** What is the **maximum** Time Travel retention on a permanent table in Enterprise edition?
A. 1 day
B. 7 days
C. 14 days
D. 90 days

**2.** What is the Time Travel retention range for a **transient** table?
A. 0 or 1 day
B. Up to 7 days
C. Up to 90 days
D. Same as permanent

**3.** Who can recover data from **Fail-safe**?
A. Any user with ACCOUNTADMIN
B. SYSADMIN with an UNDROP
C. Only Snowflake Support
D. Any user with MONITOR on the database

**4.** How long does Fail-safe last, and for which table type?
A. 7 days, permanent tables only
B. 14 days, all table types
C. 1 day, temporary tables only
D. 90 days, permanent tables only

**5.** `CREATE DATABASE dev CLONE prod;` — which is **true** about the resulting clone?
A. Clones double the storage used by `prod`.
B. The clone shares micro-partitions with `prod` until either diverges.
C. Grants on `prod` objects automatically apply to `dev`.
D. Cloning takes roughly the same time as a full copy.

**6.** Which statement restores a dropped table within the Time Travel window?
A. `RESTORE TABLE sales;`
B. `UNDROP TABLE sales;`
C. `ROLLBACK;`
D. `RECOVER TABLE sales;`

**7.** Tri-Secret Secure is available in which Snowflake edition?
A. Standard
B. Enterprise
C. Business Critical
D. Virtual Private Snowflake only

**8.** A team needs cross-region disaster recovery that includes databases, users, roles, and warehouses — promoted in one command. Which feature fits?
A. Zero-copy cloning
B. Database replication alone
C. Failover groups
D. Tri-Secret Secure

**9.** Which clause queries a table as of a specific query ID?
A. `AT(TIMESTAMP => ...)`
B. `BEFORE(STATEMENT => '<query_id>')`
C. `AT(OFFSET => -60)`
D. `FROM sales HISTORY`

**10.** True or False: Temporary tables have a 7-day Fail-safe period.

---

## Answer key

1. **D** — Enterprise+ supports up to 90 days. [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel); *Platform Study Guide §4.1, p. 8*.
2. **A** — Transient and temporary tables support 0 or 1 day only. [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel); `domain_4_0_data_protection.md:L19-L33`.
3. **C** — Fail-safe is Support-only. *Core Study Guide Domain 6.0, p. 12*; `domain_4_0_data_protection.md:L34-L45`.
4. **A** — 7 days, permanent only. [Fail-safe](https://docs.snowflake.com/en/user-guide/data-failsafe).
5. **B** — Zero-copy clones share micro-partitions. [Cloning considerations](https://docs.snowflake.com/en/user-guide/object-clone).
6. **B** — `UNDROP`. [UNDROP TABLE](https://docs.snowflake.com/en/sql-reference/sql/undrop-table); `lab_05_data_protection.sql` Section 4.
7. **C** — Business Critical. [Encryption management](https://docs.snowflake.com/en/user-guide/security-encryption-manage).
8. **C** — Failover groups bundle databases + account-level objects. [Account replication](https://docs.snowflake.com/en/user-guide/account-replication-intro); *DEA Study Guide §3.1, p. 8*.
9. **B** — `BEFORE(STATEMENT => '<qid>')`. [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel).
10. **False** — Temporary and transient tables have no Fail-safe. [Fail-safe](https://docs.snowflake.com/en/user-guide/data-failsafe); `domain_4_0_data_protection.md:L34-L45`.
