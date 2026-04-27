# Vendor Azure — Branch References

Primary-source index for the DP-700 branch. Per `../../docs/REUSE_POLICY.md` only official documentation, specifications, canonical books, sibling files, and vendor certification pages are cited.

## Official exam pages

- [Microsoft Certified: Fabric Data Engineer Associate (DP-700)](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/) — certification landing page.
- [Exam DP-700: Implementing Data Engineering Solutions Using Microsoft Fabric](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/) — exam page (booking, policies).
- [DP-700 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700) — skills measured, domain weights.
- [Microsoft Learn practice assessment for DP-700](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/practice/assessment) — official practice test.

## Microsoft Learn — Fabric

- [What is Microsoft Fabric?](https://learn.microsoft.com/en-us/fabric/get-started/microsoft-fabric-overview)
- [OneLake overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview)
- [OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts)
- [Fabric Lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview)
- [Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing)
- [Fabric Data Factory (pipelines + Dataflow Gen2)](https://learn.microsoft.com/en-us/fabric/data-factory/)
- [Fabric Real-Time Intelligence](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview)
- [Fabric Spark compute](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute)
- [Fabric Delta Lake guidance](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order)
- [Fabric deployment pipelines](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines)
- [Fabric monitoring hub](https://learn.microsoft.com/en-us/fabric/admin/monitoring-hub)

## Microsoft Learn — legacy/transferable Azure services

- [Azure Data Lake Storage Gen2](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
- [ADLS Gen2 access control (RBAC + POSIX ACLs)](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control-model)
- [Azure Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/introduction)
- [Azure Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is)
- [Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/)
- [Azure Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about)
- [Azure Stream Analytics](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-introduction)
- [Microsoft Purview](https://learn.microsoft.com/en-us/purview/purview)
- [Microsoft Entra ID (RBAC)](https://learn.microsoft.com/en-us/entra/fundamentals/whatis)
- [Managed identities for Azure resources](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)
- [Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/overview)
- [Log Analytics / KQL](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-overview)
- [Kusto Query Language reference](https://learn.microsoft.com/en-us/kusto/query/)
- [T-SQL reference](https://learn.microsoft.com/en-us/sql/t-sql/language-reference)

## Supplementary Microsoft Learn labs and study material

- [Microsoft Learn: Delta Lake](https://learn.microsoft.com/en-us/azure/databricks/delta/) — Delta MERGE, time travel, history (logic reusable in Fabric notebooks).
- [Azure Databricks Spark](https://learn.microsoft.com/en-us/azure/databricks/getting-started/spark/) — DataFrame ops, broadcast joins, repartition vs coalesce.
- [Structured Streaming](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/) — checkpoints, watermarks, output modes.
- [Azure Data Factory pipelines](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities) — ADF, medallion, batch processing, triggers.
- [Azure Synapse security](https://learn.microsoft.com/en-us/azure/synapse-analytics/security/) — RBAC/ACL, Monitor, tuning exercises.
- [Fabric Warehouse T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area) — OPENROWSET, CETAS, CTAS, JSON, RLS, DDM exercises.
- [KQL reference](https://learn.microsoft.com/en-us/kusto/query/) — KQL for pipeline monitoring, alerts, throughput.
- [Microsoft DP-700 practice assessment](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/) — **format reference only** (see `mock_exam_sources.md`).

## Canonical books

- *Designing Data-Intensive Applications*, Kleppmann, Ch. 5, 6, 11 — streaming, partitioning.
- *The Data Warehouse Toolkit*, Kimball, Ch. 1–3 — dimensional modeling used in Fabric warehouses.
- *Fundamentals of Data Engineering*, Reis/Housley — lifecycle framing for medallion/lakehouse.
