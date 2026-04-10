# Module 01 — References

## Microsoft Learn

- [Azure Data Lake Storage Gen2 introduction](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
- [ADLS Gen2 access control model (RBAC + POSIX ACLs)](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control-model)
- [OneLake overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview)
- [OneLake security](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-security)
- [OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts)
- [Create a OneLake shortcut](https://learn.microsoft.com/en-us/fabric/onelake/create-onelake-shortcut)
- [Fabric mirroring overview](https://learn.microsoft.com/en-us/fabric/database/mirrored-database/overview)
- [Fabric Lakehouse overview](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview)
- [Create a lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/create-lakehouse)
- [Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing)
- [COPY statement for Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/ingest-data-copy)
- [Delta optimization and V-Order in Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order)
- [Delta Lake table maintenance in Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance)

## Sibling reuse

- `../../../../azure_certified/IMPLEMENTATION-PLAN.md:L175-L270` — ADLS Gen2, Delta format, partitioning, Synapse pool types (legacy context).
- `../../../../azure_certified/labs/01-delta-lake-fundamentals.ipynb` — Delta MERGE, time travel, history.
- `../../../../azure_certified/labs/04-batch-and-pipeline-patterns.md:L451-L842` — medallion architecture as applied to lakehouse storage.
- `../../../../azure_certified/flashcards/top-33-flashcards.md` — Card 1 (MERGE), Card 11 (OPTIMIZE/ZORDER/VACUUM), Card 5 (distributions, legacy).

## Books

- *Designing Data-Intensive Applications*, Kleppmann, Ch. 6 — partitioning.
- *The Data Warehouse Toolkit*, Kimball, Ch. 1–3 — dimensional modeling for warehouse layer.
