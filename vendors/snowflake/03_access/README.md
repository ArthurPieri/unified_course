# Module 03: Identity and Access (RBAC)

Snowflake's access model is **role-based access control**: privileges are granted to roles, roles are granted to users or other roles. Understanding the system-defined roles and their intended separation of duties is Platform Domain 2.0 (15%), Core Domain 2.0 (18%), and the substrate for DEA Domain 4.0 governance (14%).

## Learning goals
- Name the four system-defined roles and state one responsibility of each.
- Draw the default role hierarchy including PUBLIC and USERADMIN.
- Explain privilege inheritance and the difference between primary and secondary roles.
- Describe what SCIM does and which role owns SCIM provisioning.
- Pick the right role to perform a given action in a scenario.

## Prerequisites
- `../01_architecture/` — object hierarchy frames privilege grants.

## Reading order
1. This README
2. [Snowflake Access Control](https://docs.snowflake.com/en/user-guide/security-access-control-overview) — system roles, hierarchy, INFORMATION_SCHEMA, ownership transfer
3. [Snowflake Quickstarts](https://quickstarts.snowflake.com/) — identity and access hands-on labs
4. `quiz.md`

## Concepts

### System-defined roles
| Role | Purpose |
|---|---|
| `ORGADMIN` | Manages the organization (top-level), creates accounts. Not granted to ACCOUNTADMIN by default. |
| `ACCOUNTADMIN` | Top of the in-account hierarchy. Can do anything. Use sparingly. |
| `SECURITYADMIN` | Manages users, roles, grants. Inherits USERADMIN. |
| `USERADMIN` | Creates and manages users and roles (but not grants on objects). |
| `SYSADMIN` | Creates and owns objects (databases, schemas, warehouses). The parent of all custom roles by convention. |
| `PUBLIC` | Implicit role every user has; privileges granted to PUBLIC are universal. |

Ref: *SnowPro Associate: Platform Study Guide, §2.1, p. 6* · [Snowflake Access Control](https://docs.snowflake.com/en/user-guide/security-access-control-overview).

### Default hierarchy
```
         ORGADMIN          ACCOUNTADMIN
                               / \
                  SECURITYADMIN   SYSADMIN
                        |             \
                    USERADMIN        (custom roles by convention)
                                         \
                                        PUBLIC
```
ACCOUNTADMIN inherits SYSADMIN and SECURITYADMIN. SECURITYADMIN inherits USERADMIN. Custom roles should be granted to SYSADMIN so that ACCOUNTADMIN still sees everything.

Ref: `domain_2_0_identity.md:L22-L60`.

### Privileges and inheritance
Privileges are granted on objects (`GRANT SELECT ON TABLE ... TO ROLE analyst`). Roles granted to other roles inherit all their privileges — there is no revocation by exclusion. **Future grants** (`GRANT ... ON FUTURE TABLES IN SCHEMA`) apply to objects not yet created. Ownership is a privilege too; `OWNERSHIP` can be transferred with `GRANT OWNERSHIP ... COPY CURRENT GRANTS`.

Ref: *SnowPro Core Study Guide, Domain 2.0 "Account Access and Security", p. 7* · `domain_2_0_identity.md:L125-L235`.

### Primary vs secondary roles
A session has exactly one **primary role** (`USE ROLE x;`) but can have multiple **secondary roles** activated (`USE SECONDARY ROLES ALL;`). Secondary roles' privileges are additive — effectively a union. Ownership operations still require the primary role. Secondary roles are enabled at the user level with `DEFAULT_SECONDARY_ROLES`.

Ref: [USE SECONDARY ROLES](https://docs.snowflake.com/en/sql-reference/sql/use-secondary-roles) · *Core Study Guide, Domain 2.0, p. 7*.

### SCIM (System for Cross-domain Identity Management)
SCIM automates user and group provisioning from an IdP (Okta, Azure AD) into Snowflake. You configure a SCIM integration (`CREATE SECURITY INTEGRATION ... TYPE = SCIM`). Provisioning runs under a dedicated role (typically `OKTA_PROVISIONER` or `AAD_PROVISIONER`) granted at setup. SECURITYADMIN owns the integration by default.

Ref: [SCIM overview](https://docs.snowflake.com/en/user-guide/scim-intro) · *Core Study Guide, Domain 2.0, p. 7*.

### Object access by role
Every `SELECT`, `INSERT`, `CREATE`, `ALTER`, or `DROP` is evaluated against the active role's privileges. `SHOW GRANTS TO ROLE x;` and `SHOW GRANTS ON TABLE t;` are the diagnostic commands. Use `USE ROLE` to switch; `CURRENT_ROLE()` returns the active primary role.

Ref: [Snowflake Quickstarts](https://quickstarts.snowflake.com/) · [Snowflake Access Control](https://docs.snowflake.com/en/user-guide/security-access-control-overview).

## Hands-on drills

| # | Drill | Est. time | Source |
|---|---|---|---|
| D1 | Use each of ACCOUNTADMIN, SECURITYADMIN, SYSADMIN, USERADMIN in a session; observe what each can and cannot do. | 30 min | `lab_04_identity_and_access.sql` Sections 1-2 |
| D2 | Create a custom role `analyst` as SYSADMIN, grant USAGE on a database and SELECT on a schema, assign to a user. | 25 min | `lab_04_identity_and_access.sql` Sections 2-3 |
| D3 | Apply `GRANT SELECT ON FUTURE TABLES IN SCHEMA raw TO ROLE analyst;` then create a new table and confirm `analyst` can read it without an additional grant. | 20 min | *Core Study Guide §2.0, p. 7* |
| D4 | Enable secondary roles (`USE SECONDARY ROLES ALL;`) and confirm privileges union. | 15 min | [USE SECONDARY ROLES docs](https://docs.snowflake.com/en/sql-reference/sql/use-secondary-roles) |
| D5 | Transfer ownership of a table using `GRANT OWNERSHIP ... COPY CURRENT GRANTS`. | 20 min | `lab_04_identity_and_access.sql` Section 9 |

## Common failures (exam gotchas)

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| "SECURITYADMIN can create databases" | False | SECURITYADMIN manages grants, not objects. Use SYSADMIN to create objects. | `domain_2_0_identity.md:L61-L74` |
| "ACCOUNTADMIN is the default role for daily work" | Anti-pattern | Work under SYSADMIN or a custom role; elevate to ACCOUNTADMIN only when necessary. | `domain_2_0_identity.md:L149-L161` |
| "A role can have a privilege revoked from a subset of its grantees" | False | Grants are inherited; you cannot exclude. Create a narrower role instead. | [Access control](https://docs.snowflake.com/en/user-guide/security-access-control-overview) |
| "Future grants apply to existing tables" | False | Future grants apply only to objects created after the grant. Use standard GRANT for existing. | *Core Study Guide §2.0, p. 7* |
| "SCIM creates Snowflake accounts" | Wrong scope | SCIM provisions users and groups inside an existing account; it does not create accounts. | [SCIM docs](https://docs.snowflake.com/en/user-guide/scim-intro) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Name every system role and pick the correct one for a given task.
- [ ] Write grants that use both standard and future-grant syntax.
- [ ] Explain primary vs secondary roles and when secondary roles apply.
- [ ] Describe what SCIM provisions and which role owns the integration.
