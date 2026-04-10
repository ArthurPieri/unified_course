# Module 03 — References

## Microsoft Learn

- [Fabric Spark compute](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute)
- [Fabric notebooks overview](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)
- [Fabric Lakehouse SQL analytics endpoint](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint)
- [Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing)
- [Fabric Warehouse T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area)
- [COPY INTO (Fabric Warehouse)](https://learn.microsoft.com/en-us/fabric/data-warehouse/ingest-data-copy)
- [Fabric KQL database](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/create-database)
- [Kusto Query Language reference](https://learn.microsoft.com/en-us/kusto/query/)
- [Spark SQL reference (Fabric)](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-sql-reference)
- [Delta Lake docs (Databricks)](https://learn.microsoft.com/en-us/azure/databricks/delta/)
- [Delta Lake MERGE](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/delta-merge-into)
- [Azure Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is)
- [Dedicated SQL pool distributions](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-distribute)
- [Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/)
- [T-SQL language reference](https://learn.microsoft.com/en-us/sql/t-sql/language-reference)

## Sibling reuse

- `../../../../azure_certified/IMPLEMENTATION-PLAN.md:L186-L295` — Synapse pool types, Spark, T-SQL, Delta MERGE.
- `../../../../azure_certified/IMPLEMENTATION-PLAN.md:L683-L745` — performance and tuning.
- `../../../../azure_certified/labs/01-delta-lake-fundamentals.ipynb` — Delta MERGE, history, time travel.
- `../../../../azure_certified/labs/02-spark-transformations.ipynb` — DataFrame ops, broadcast, repartition, explain plans.
- `../../../../azure_certified/labs/06-tsql-exercises.md:L7-L1266` — OPENROWSET, external tables, CTAS, COPY INTO, JSON, RLS, DDM.
- `../../../../azure_certified/labs/07-kql-exercises.md:L9-L473` — KQL exercises for pipeline monitoring and throughput.
- `../../../../azure_certified/flashcards/top-33-flashcards.md` — Card 1 (MERGE), Card 2 (Spark lazy), Card 5 (distributions), Card 9 (COPY INTO), Card 11 (OPTIMIZE).

## Books

- *Designing Data-Intensive Applications*, Kleppmann, Ch. 10 — batch processing and MapReduce lineage to Spark.
- *The Data Warehouse Toolkit*, Kimball, Ch. 1–5 — star schema modeling for Warehouse designs.
