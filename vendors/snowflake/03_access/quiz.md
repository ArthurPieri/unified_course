# Module 03 — Quiz: Access & RBAC

10 questions. Key + citations at the bottom.

---

**1.** Which system-defined role is intended for creating and owning **databases, schemas, and warehouses**?
A. ACCOUNTADMIN
B. SECURITYADMIN
C. SYSADMIN
D. USERADMIN

**2.** Which role manages **users and role grants**, inheriting USERADMIN?
A. ACCOUNTADMIN
B. SECURITYADMIN
C. SYSADMIN
D. PUBLIC

**3.** A developer runs `USE ROLE analyst; USE SECONDARY ROLES ALL;` then queries a table. How are privileges evaluated?
A. Only `analyst`'s privileges apply.
B. Union of `analyst` plus every role granted to the user.
C. Intersection of all granted roles.
D. The session fails unless one role has OWNERSHIP.

**4.** You want a role to automatically gain SELECT on **new** tables created in a schema. Which grant do you use?
A. `GRANT SELECT ON ALL TABLES IN SCHEMA raw TO ROLE analyst;`
B. `GRANT SELECT ON FUTURE TABLES IN SCHEMA raw TO ROLE analyst;`
C. `GRANT SELECT ON SCHEMA raw TO ROLE analyst;`
D. `GRANT OWNERSHIP ON SCHEMA raw TO ROLE analyst;`

**5.** Which statement about `PUBLIC` is **correct**?
A. PUBLIC is never granted to users.
B. Every user in the account is implicitly a member of PUBLIC.
C. PUBLIC inherits SYSADMIN.
D. Only ACCOUNTADMIN can grant to PUBLIC.

**6.** Which role is best used to **create new users** (but not to grant privileges on tables)?
A. USERADMIN
B. ACCOUNTADMIN
C. SYSADMIN
D. PUBLIC

**7.** What does a SCIM integration provision in Snowflake?
A. Snowflake accounts
B. Databases and schemas
C. Users and groups from an external IdP
D. External stages

**8.** Ownership of a table is being transferred from `role_a` to `role_b`. Which clause preserves all existing non-ownership grants on the table?
A. `GRANT OWNERSHIP ... REVOKE CURRENT GRANTS`
B. `GRANT OWNERSHIP ... COPY CURRENT GRANTS`
C. `GRANT ALL ... TO ROLE role_b`
D. `ALTER TABLE ... SET OWNER = role_b`

**9.** True or False: ACCOUNTADMIN should be the default role a developer uses for daily object creation.

**10.** A user with role `analyst` cannot see a table in `SHOW TABLES`. Which grant is most likely missing?
A. `USAGE` on the database or schema
B. `CREATE TABLE` on the schema
C. `OWNERSHIP` on the table
D. `MONITOR` on the warehouse

---

## Answer key

1. **C** — SYSADMIN is the canonical object owner. `domain_2_0_identity.md:L42-L60`; [Access control](https://docs.snowflake.com/en/user-guide/security-access-control-overview).
2. **B** — SECURITYADMIN manages grants and inherits USERADMIN. `domain_2_0_identity.md:L42-L60`.
3. **B** — Secondary roles are additive. [USE SECONDARY ROLES](https://docs.snowflake.com/en/sql-reference/sql/use-secondary-roles).
4. **B** — Future grants apply to objects created **after** the grant. *Core Study Guide §2.0, p. 7*; [GRANT](https://docs.snowflake.com/en/sql-reference/sql/grant-privilege).
5. **B** — PUBLIC is implicit. [Access control](https://docs.snowflake.com/en/user-guide/security-access-control-overview); `domain_2_0_identity.md:L42-L60`.
6. **A** — USERADMIN creates users/roles but does not manage object grants. `domain_2_0_identity.md:L61-L74`.
7. **C** — Users and groups from an external IdP. [SCIM docs](https://docs.snowflake.com/en/user-guide/scim-intro).
8. **B** — `COPY CURRENT GRANTS` preserves existing grants during an ownership transfer. [GRANT OWNERSHIP](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership); `lab_04_identity_and_access.sql` Section 9.
9. **False** — Anti-pattern. Work under SYSADMIN or a custom role; elevate to ACCOUNTADMIN only when necessary. `domain_2_0_identity.md:L149-L161`.
10. **A** — Without `USAGE` on the parent database/schema, the object is invisible. [Access control considerations](https://docs.snowflake.com/en/user-guide/security-access-control-considerations).
