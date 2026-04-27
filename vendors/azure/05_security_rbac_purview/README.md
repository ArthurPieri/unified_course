# Module 05 — Security: Entra ID, RBAC, ADLS ACLs, Purview, Managed Identity

> DP-700 exam weight: Domain 1 (security and governance) + Domain 3 crossover. Roughly 15 hours.

## Learning goals

- Explain the difference between Azure RBAC roles and POSIX ACLs on ADLS Gen2, and the order of evaluation.
- Pick the right authentication method across Azure services (managed identity > OAuth > SAS > account key).
- Configure row-level security (RLS), column-level security (CLS), and dynamic data masking (DDM) in T-SQL.
- Choose between service endpoints and private endpoints for network isolation.
- Describe Microsoft Purview capabilities: data map, lineage, classification, glossary, and how it integrates with ADF/Fabric.
- Explain Fabric workspace roles and OneLake security (item-level and row/column-level).

## Prerequisites

- `01_storage_adls_fabric/README.md`
- `02_ingestion_adf_fabric_pipelines/README.md`

## Concepts

### Microsoft Entra ID (formerly Azure AD) and Azure RBAC

Entra ID is the identity provider; Azure RBAC assigns principals (users, groups, service principals, managed identities) to roles at a **scope** (subscription, resource group, resource). Key data-plane roles to memorize: **Storage Blob Data Reader / Contributor / Owner** — these grant access to the actual bytes in a storage container. The `Contributor` and `Owner` roles at the management plane do **not** grant data access; this is a classic exam trap.
Ref: [Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview) · [Storage built-in roles](https://learn.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access)

### POSIX ACLs on ADLS Gen2

ADLS Gen2 supports POSIX-like ACLs (`rwx`) on files and directories when HNS is enabled. **Access ACLs** apply to the current object; **Default ACLs** are inherited by new children (not retroactive). Traversing a path requires **execute (x)** on every parent directory. Max 32 ACL entries per object — use Entra ID security groups to stay within the limit.

**Interplay with RBAC:** RBAC is evaluated first. If an RBAC role grants the requested action (e.g., `Storage Blob Data Reader` at container scope), ACLs are not checked. If RBAC does not grant access, ACLs are evaluated. This means ACLs can *grant* access that RBAC omitted, but they cannot *deny* access that RBAC already permits — a frequently tested gotcha.
Ref: [ADLS Gen2 access control model](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control-model)

### Managed identity — the preferred auth method

Managed identity (system-assigned or user-assigned) gives Azure services an Entra-managed credential with no secrets to rotate. Preferred everywhere DP-700 cares about: ADF/Fabric Data Factory to ADLS, Synapse to Key Vault, Databricks to storage, Fabric workspace identity to external sources. **Avoid**: account keys, SAS tokens (beyond short-lived scenarios), embedded PATs. **Disable storage account keys** in production to enforce identity-only auth.
Ref: [Managed identities](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview) · [Fabric workspace identity](https://learn.microsoft.com/en-us/fabric/security/workspace-identity)

### Row-level security (RLS), column-level security (CLS), Dynamic Data Masking (DDM)

- **RLS**: a security predicate function filters rows transparently based on the caller's identity (`SESSION_CONTEXT`, `USER_NAME`). Attached via `CREATE SECURITY POLICY`. Works on Synapse dedicated pool, Synapse serverless, **and Fabric Warehouse**.
- **CLS**: standard SQL `GRANT SELECT ON table (col1, col2) TO role`. Queries that reference denied columns fail outright.
- **DDM**: replaces column values with masks (default, email, random, partial) at query time. Users with `UNMASK` permission see real values. **DDM is obfuscation, not encryption** — a determined user can often infer real values via `WHERE SSN = '...'` probing.

Ref: [Row-level security](https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security) · [Column-level security](https://learn.microsoft.com/en-us/sql/relational-databases/security/column-level-security) · [Dynamic data masking](https://learn.microsoft.com/en-us/sql/relational-databases/security/dynamic-data-masking)

### Encryption

- **At rest**: ADLS Gen2 encrypts with service-managed keys (SSE) by default; customer-managed keys (CMK) via Key Vault give rotation and revocation control. Revoking the CMK makes data inaccessible. **Double encryption** must be set at account creation.
- **In transit**: TLS 1.2 is enforced by default; "Secure transfer required" on storage accounts rejects HTTP.
- **Fabric Warehouse / Synapse**: TDE enabled by default, AES-256, service- or customer-managed keys.

Ref: [Storage encryption](https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption) · [Customer-managed keys](https://learn.microsoft.com/en-us/azure/storage/common/customer-managed-keys-overview)

### Private endpoints vs service endpoints

| Feature | Service endpoint | Private endpoint |
|---|---|---|
| IP | Service keeps its public IP | Private IP injected into your VNet |
| Traffic path | Azure backbone, but service remains publicly reachable unless firewalled | Private link; service can have public access disabled |
| Cost | Free | Per endpoint + per GB processed |
| Exfiltration protection | No | Yes, combined with managed VNet |
| On-premises via VPN/ExpressRoute | No | Yes |

If the question says "no public internet, ever" or "prevent exfiltration", answer is **private endpoint**.
Ref: [Private endpoints](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview) · [Service endpoints](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)

### Microsoft Purview — governance

Purview is the data-governance and catalog service. Key capabilities: **data map** (automated discovery and scanning of Azure, AWS, on-prem sources), **lineage** (ADF/Synapse/Fabric pipelines push lineage automatically when integrated), **classifications** (built-in PII classifiers: SSN, credit card, email, plus custom), **business glossary**, **access policies**. For DP-700, expect questions on Purview's role alongside Fabric (Fabric has its own governance surface but integrates with Purview for cross-tenant lineage and classification).
Ref: [Microsoft Purview](https://learn.microsoft.com/en-us/purview/purview) · [Data Map overview](https://learn.microsoft.com/en-us/purview/concept-data-map)

### Fabric workspace roles and OneLake security

Fabric workspaces use four roles — **Admin, Member, Contributor, Viewer** — analogous to but distinct from Power BI workspace roles. Item-level permissions override workspace roles for specific artifacts. OneLake supports **OneLake data access roles** (preview/GA moving target; verify on MS Learn), enabling folder-level RBAC inside a lakehouse. SQL analytics endpoint supports RLS/CLS/DDM natively. Fabric **sensitivity labels** (from Microsoft Purview Information Protection) propagate down through dependent items.
Ref: [Fabric workspace roles](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces) · [OneLake security](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-security)

## Labs

| Lab | Goal | Est. time | Source |
|---|---|---|---|
| L05.1 RBAC + ACL exercise | Grant a user data access via ACLs only, then via RBAC, and observe differences | 45 m | [Azure Synapse security](https://learn.microsoft.com/en-us/azure/synapse-analytics/security/) |
| L05.2 RLS, CLS, DDM | Implement all three on a Fabric Warehouse or Synapse serverless table | 60 m | [Row-level security](https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security) · [Dynamic data masking](https://learn.microsoft.com/en-us/sql/relational-databases/security/dynamic-data-masking) |
| L05.3 Managed identity auth | Configure an ADF linked service to ADLS using managed identity | 30 m | [Azure Synapse security](https://learn.microsoft.com/en-us/azure/synapse-analytics/security/) |
| L05.4 Private endpoint walkthrough | Create a private endpoint to a storage account and verify public access is blocked | 45 m | [Private endpoint tutorial](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal) |

## Common failures

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| User with `Contributor` role cannot read blobs | `Contributor` is a management-plane role, not a data-plane role | Assign `Storage Blob Data Reader` (or Contributor/Owner) | [Storage built-in roles](https://learn.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access) |
| User has `rwx` ACL on a nested file but cannot read it | Missing execute (`x`) on an ancestor directory | Grant `x` on every parent directory in the path | [ADLS Gen2 access control model](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control-model) |
| DDM bypassed by `db_owner` | DDM is not security; `db_owner` always unmasks | Combine DDM with CLS/RLS and the principle of least privilege | [Dynamic data masking](https://learn.microsoft.com/en-us/sql/relational-databases/security/dynamic-data-masking) |
| Purview shows no lineage for an ADF pipeline | Purview not linked to the ADF / Synapse workspace | Connect ADF to Purview; lineage is automatic once linked | [Purview lineage](https://learn.microsoft.com/en-us/purview/concept-data-lineage) |

## References

See [references.md](./references.md). Quiz in [quiz.md](./quiz.md).

## Checkpoint

- [ ] I can answer a scenario question about RBAC+ACL evaluation order without hesitation.
- [ ] I can write a `CREATE SECURITY POLICY` for RLS.
- [ ] I can explain why private endpoint wins over service endpoint for zero-public-internet scenarios.
- [ ] I can list the Fabric workspace roles and describe where OneLake security sits.
