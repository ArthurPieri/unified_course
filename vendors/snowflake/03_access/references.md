# Module 03 — References

## Snowflake docs
- [Access control overview](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [Access control considerations](https://docs.snowflake.com/en/user-guide/security-access-control-considerations)
- [System-defined roles](https://docs.snowflake.com/en/user-guide/security-access-control-overview#system-defined-roles)
- [GRANT <privileges>](https://docs.snowflake.com/en/sql-reference/sql/grant-privilege)
- [USE ROLE](https://docs.snowflake.com/en/sql-reference/sql/use-role)
- [USE SECONDARY ROLES](https://docs.snowflake.com/en/sql-reference/sql/use-secondary-roles)
- [SCIM overview](https://docs.snowflake.com/en/user-guide/scim-intro)
- [Managing SCIM for Okta / Azure AD](https://docs.snowflake.com/en/user-guide/scim-okta)

## Official study guides
- *SnowPro Associate: Platform Study Guide*, §2.1 "Define the roles that are used in Snowflake", p. 6 — RBAC, role hierarchy, role types, privileges, object access by role.
- *SnowPro Core Study Guide*, Domain 2.0 "Account Access and Security", p. 7 — auth methods, access control frameworks, privilege inheritance, governance overview.
- *SnowPro Advanced: Data Engineer Study Guide*, Domain 4.0 "Data Governance", p. 9 — tagging, classification, masking, row access, masking with RBAC.

## Sibling reuse
- `../../../../snowflake_eng/phase1_platform/study_notes/domain_2_0_identity.md:L12-L250` — full conceptual + SQL examples for system roles, hierarchy, INFORMATION_SCHEMA, ownership transfer.
- `../../../../snowflake_eng/phase1_platform/labs/lab_04_identity_and_access.sql:L20-L320` — sections 1-10 covering system-defined roles, custom role hierarchy, grants, context functions, SHOW GRANTS, ownership transfer.
