# Module 05 — Quiz (Security)

1. A user is granted the Azure `Contributor` role on a storage account. Can they read blob data?
   - A. Yes, `Contributor` includes data-plane access.
   - B. No — `Contributor` is a management-plane role; they need `Storage Blob Data Reader` (or similar) for data access.
   - C. Only if HNS is enabled.
   - D. Only from a VNet.

2. A user has `Storage Blob Data Reader` on a container AND an ACL `---` (no permissions) on a file in that container. Can they read the file?
   - A. No, ACL denies.
   - B. Yes, RBAC is evaluated first and grants access; ACLs are not checked.
   - C. Only through Fabric.
   - D. Only with SAS token.

3. Your auditor requires that no traffic to a storage account ever traverses the public internet, including from other Azure services. Which networking control satisfies this?
   - A. Service endpoint with firewall rules.
   - B. Private endpoint with public access disabled.
   - C. Storage account key rotation.
   - D. TLS 1.2 enforcement.

4. A user has `rwx` ACL on `/container/dir1/dir2/file.csv` but only `r--` on `dir1`. Can they read the file?
   - A. Yes, file ACL is sufficient.
   - B. No, they need execute (`x`) on every ancestor directory to traverse.
   - C. Only if HNS is disabled.
   - D. Yes, with SAS token.

5. Which auth method is preferred for ADF/Fabric pipelines connecting to ADLS Gen2?
   - A. Storage account key
   - B. SAS token
   - C. Managed identity
   - D. Embedded password

6. RLS works on which SQL surfaces?
   - A. Dedicated pool only
   - B. Serverless only
   - C. Dedicated, serverless, and Fabric Warehouse
   - D. Fabric Lakehouse only

7. Dynamic Data Masking is best described as:
   - A. Transparent strong encryption.
   - B. Query-time obfuscation bypassable by `UNMASK` permission or inference; not true security.
   - C. A key-rotation strategy.
   - D. TLS variant.

8. Microsoft Purview automatically captures lineage from ADF pipelines when:
   - A. You run a pipeline in debug mode.
   - B. ADF is connected to the Purview account; lineage then flows automatically.
   - C. You enable Advanced Threat Protection.
   - D. Never — lineage is manual only.

9. Which storage role grants read access to actual blob bytes?
   - A. Contributor
   - B. Owner
   - C. Reader (management plane)
   - D. Storage Blob Data Reader

10. Fabric workspace roles include:
    - A. Admin, Member, Contributor, Viewer
    - B. Owner, Editor, Viewer
    - C. Root, Admin, Guest
    - D. Global Administrator only

---

## Answer key

1. **B** — Management-plane vs data-plane ([Storage built-in roles](https://learn.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access)).
2. **B** — RBAC checked first; see [ADLS Gen2 access control model](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control-model).
3. **B** — Private endpoint ([docs](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)).
4. **B** — Execute on every parent directory ([ADLS access control](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control-model)).
5. **C** — Managed identity ([docs](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)).
6. **C** — See [Row-level security](https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security) and [Dynamic data masking](https://learn.microsoft.com/en-us/sql/relational-databases/security/dynamic-data-masking).
7. **B** — DDM is not encryption ([docs](https://learn.microsoft.com/en-us/sql/relational-databases/security/dynamic-data-masking)).
8. **B** — [Purview lineage](https://learn.microsoft.com/en-us/purview/concept-data-lineage).
9. **D** — [Storage built-in roles](https://learn.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access).
10. **A** — [Fabric workspace roles](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces).
