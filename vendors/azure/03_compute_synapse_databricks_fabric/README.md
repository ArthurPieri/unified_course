# Module 03 — Compute: Synapse, Databricks, Fabric Warehouse/Lakehouse, T-SQL, KQL

> DP-700 exam weight: Domain 2 (Ingest and transform data). Roughly 25–30 hours — deepest hands-on module.

## Learning goals

- Write Spark DataFrame and Spark SQL transformations (filter, groupBy, join, window, MERGE into Delta).
- Explain lazy evaluation, the difference between `repartition` and `coalesce`, and broadcast joins.
- Use T-SQL for Fabric Warehouse workloads: CTAS-style operations, `COPY INTO`, stored procedures, `OPENJSON`.
- Use KQL against an Eventhouse / KQL database for log and telemetry analytics.
- Map Synapse dedicated SQL pool concepts (distributions, CCI, resource classes) to their Fabric Warehouse equivalents.
- Choose Fabric notebooks vs Warehouse vs Dataflow Gen2 for a given transformation scenario.

## Prerequisites

- `01_storage_adls_fabric/README.md`, `02_ingestion_adf_fabric_pipelines/README.md`
- `phase_3_core_tools/` Spark module

## Concepts

### Fabric compute surfaces

| Surface | Language | Typical use |
|---|---|---|
| Fabric notebook (Spark) | PySpark, Spark SQL, Scala, SparkR | Complex batch transforms, ML, structured streaming |
| Fabric Warehouse | T-SQL (subset) | DW workloads, stored procedures, `COPY INTO`, `MERGE` |
| Lakehouse SQL analytics endpoint | T-SQL (read-only) | Ad-hoc SQL on lakehouse Delta tables |
| Dataflow Gen2 | Power Query M | Low-code batch transforms for Power BI users |
| KQL database / Eventhouse | KQL | Real-time telemetry, log analytics |

Choose Spark notebooks when you need Python/ML/complex joins; Warehouse for traditional DW with T-SQL writes; SQL endpoint for ad-hoc reads; Dataflow Gen2 for low-code ETL; KQL database for streaming telemetry.
Ref: [Fabric compute overview](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute) · [Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing)

### Spark fundamentals (transferable)

Spark uses **lazy evaluation**: transformations (`select`, `filter`, `groupBy`, `withColumn`, `join`) build a logical plan; actions (`count`, `show`, `collect`, `write`) execute it. The Catalyst optimizer reshapes the plan (pushdown, combining stages). `repartition(n)` triggers a full shuffle and can increase or decrease partition count; `coalesce(n)` is shuffle-free but can only reduce. Broadcast joins (`broadcast(df_small)`) avoid shuffle when one side fits in memory (default threshold 10 MB, tunable via `spark.sql.autoBroadcastJoinThreshold`). Never call `.collect()` on large datasets — it materializes everything on the driver.
Ref: `../../../azure_certified/IMPLEMENTATION-PLAN.md:L284-L295` · `../../../azure_certified/labs/02-spark-transformations.ipynb` · `../../../azure_certified/flashcards/top-33-flashcards.md` Card 2

### Delta Lake MERGE — exam favorite

```sql
MERGE INTO target t USING source s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE THEN DELETE;
```

The three-clause pattern handles upsert + delete in one atomic transaction. `MERGE` is Delta-only (not plain Parquet) because it relies on the transaction log. In Fabric, `MERGE` works in both notebooks (Spark SQL) and Warehouse (T-SQL).
Ref: `../../../azure_certified/labs/01-delta-lake-fundamentals.ipynb` · `../../../azure_certified/flashcards/top-33-flashcards.md` Card 1

### T-SQL in Fabric Warehouse

Fabric Warehouse supports a curated T-SQL subset. Unsupported (vs full SQL Server / Synapse dedicated pool): user-defined CLR, PolyBase external tables, `CREATE INDEX` (tables are columnstore-only), triggers, cursors. Supported and heavily tested: `CREATE TABLE`, `INSERT`/`UPDATE`/`DELETE`, `MERGE`, `CREATE VIEW`, stored procedures, `COPY INTO` from Parquet/CSV in ADLS, `OPENJSON`/`JSON_VALUE` for JSON shredding.
Ref: [Fabric Warehouse T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area) · `../../../azure_certified/labs/06-tsql-exercises.md:L7-L560`

### KQL — read and transform streaming telemetry

KQL (Kusto Query Language) is used in two DP-700 contexts: (1) as the query language for an **Eventhouse / KQL Database** (Fabric Real-Time Intelligence) storing streaming events; (2) as the query language for **Log Analytics** when monitoring Fabric/Azure workloads (module 06). KQL essentials: `where`, `summarize`, `project`, `extend`, `join kind=`, `make-series`, `bin()`, `ago()`, `render timechart`.
Ref: [KQL reference](https://learn.microsoft.com/en-us/kusto/query/) · `../../../azure_certified/labs/07-kql-exercises.md:L9-L473`

### Synapse dedicated SQL pool (legacy context)

Know these for migration questions. **Distributions**: hash (large fact tables, choose high-cardinality join column), round-robin (staging heap), replicated (small dims <2 GB). **CCI** is the default storage format. **Resource classes** (smallrc → xlargerc) allocate memory per query; batch loads need larger classes. **PolyBase** / `COPY INTO` load from ADLS external files, with `COPY INTO` being Microsoft's preferred path. **Two-step load pattern**: stage heap RR → CTAS to hash CCI.
Ref: `../../../azure_certified/IMPLEMENTATION-PLAN.md:L186-L245` · `../../../azure_certified/flashcards/top-33-flashcards.md` Card 5, Card 9 · `../../../azure_certified/labs/06-tsql-exercises.md:L336-L760`

### Azure Databricks on Azure (legacy context, partial transfer)

Databricks on Azure runs the Databricks Lakehouse Platform with Azure integration (Entra ID, ADLS Gen2, Key Vault). Transferable concepts: Spark, Delta Lake, structured streaming, notebooks, clusters (job vs all-purpose), Unity Catalog (centralized governance). **Non-transferable** to DP-700: Databricks-specific features like DBFS, Databricks SQL warehouses, Photon. DP-700 questions lean on Spark and Delta Lake rather than Databricks UI specifics.
Ref: [Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/) · `../../../azure_certified/IMPLEMENTATION-PLAN.md:L122-L128`

### Service comparison: Synapse dedicated pool vs Fabric Warehouse

| Feature | Synapse dedicated pool | Fabric Warehouse |
|---|---|---|
| Storage | Proprietary columnstore | Open Delta Lake in OneLake |
| Distribution tuning | Hash / round-robin / replicated | Automatic; no user-visible distributions |
| Billing | DWU provisioned | Fabric capacity (F-SKUs) |
| Indexes | CCI default, can add NCI/rowstore | Columnstore only; no user indexes |
| PolyBase / external tables | Supported (exam topic) | Not supported — use shortcuts + mirroring |
| T-SQL surface | Full T-SQL including PolyBase, CETAS, resource classes | Curated subset; no CLR, no triggers, no cursors |
| Migration story | — | Use Fabric Warehouse migration assistant |

Ref: [Fabric Warehouse vs legacy DW](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing) · [T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area)

## Labs

| Lab | Goal | Est. time | Source |
|---|---|---|---|
| L03.1 Spark transformations | Filter, groupBy, join, broadcast, `.explain()` plan reading | 60 m | `../../../azure_certified/labs/02-spark-transformations.ipynb` |
| L03.2 Delta MERGE | Upsert scenario with three-clause `MERGE`, time travel, history | 45 m | `../../../azure_certified/labs/01-delta-lake-fundamentals.ipynb` |
| L03.3 T-SQL on Warehouse | `COPY INTO`, `CTAS`-style pattern, JSON shredding, RLS | 90 m | `../../../azure_certified/labs/06-tsql-exercises.md:L7-L1266` |
| L03.4 KQL exercises | Basic `where` / `summarize` / `render` against a KQL DB or Log Analytics demo | 60 m | `../../../azure_certified/labs/07-kql-exercises.md:L9-L473` |

## Common failures

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `OutOfMemoryError` on driver | `.collect()` / `.toPandas()` on a big DataFrame | Process in partitions, write to storage, or aggregate first | `../../../azure_certified/IMPLEMENTATION-PLAN.md:L703-L710` |
| One Spark task takes 100x longer than others | Data skew on the join key | Enable AQE skew join, salt the key, or broadcast the small side | `../../../azure_certified/IMPLEMENTATION-PLAN.md:L693-L700` |
| `MERGE` fails with "ambiguous rows" | Multiple source rows match the same target row | Dedupe source first (ROW_NUMBER + filter) | `../../../azure_certified/labs/01-delta-lake-fundamentals.ipynb` |
| Fabric Warehouse rejects `CREATE INDEX` | Warehouse is columnstore-only | Remove manual index DDL; rely on built-in stats | [T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area) |

## References

See [references.md](./references.md). Quiz in [quiz.md](./quiz.md).

## Checkpoint

- [ ] I can write a Spark SQL `MERGE` into a Delta table with three clauses.
- [ ] I can read a Spark `.explain()` plan and spot a broadcast vs shuffle join.
- [ ] I can run `COPY INTO` on a Fabric Warehouse from ADLS Gen2 Parquet.
- [ ] I can write a KQL query that aggregates events by 5-minute bins and renders a timechart.
