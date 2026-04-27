# Phase 3 — References (aggregator)

Phase-level index. Each module carries its own `references.md`; this file points at them and at the phase-wide sources.

## Module-level references

- `00_stack_overview/references.md`
- `01_minio_iceberg_hms/references.md` - `02_trino/references.md` - `03_pyspark/references.md` - `04_dlt/references.md` - `05_dbt/references.md` - `06_dagster/references.md` - `07_metabase/references.md` 
## Phase-wide primary docs

### Storage and table format

- MinIO docs: https://min.io/docs/minio/linux/index.html
- Apache Iceberg docs: https://iceberg.apache.org/docs/latest/
- Iceberg spec: https://iceberg.apache.org/spec/
- Iceberg Spark configuration: https://iceberg.apache.org/docs/latest/spark-configuration/
- Iceberg Hive catalog: https://iceberg.apache.org/docs/latest/hive/

### Query and compute engines

- Trino docs: https://trino.io/docs/current/
- Trino Iceberg connector: https://trino.io/docs/current/connector/iceberg.html
- Apache Spark 3.5.3 docs: https://spark.apache.org/docs/3.5.3/
- Spark SQL + DataFrames: https://spark.apache.org/docs/3.5.3/sql-programming-guide.html
- Spark tuning: https://spark.apache.org/docs/3.5.3/tuning.html
- Hadoop S3A (3.3.4): https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html

### Catalog backend

- Apache Hive 4 metastore: https://hive.apache.org/
- PostgreSQL 16 docs: https://www.postgresql.org/docs/16/

### Ingestion, modelling, orchestration, BI

- dlt docs: https://dlthub.com/docs
- dbt Core docs: https://docs.getdbt.com/docs/introduction
- dbt-trino adapter: https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup
- Dagster docs: https://docs.dagster.io/
- Dagster dbt integration: https://docs.dagster.io/integrations/dbt
- Metabase docs: https://www.metabase.com/docs/latest/

### Release pages (version pinning — see `../references/tools.md`)

- MinIO: https://github.com/minio/minio/releases
- Hive: https://hive.apache.org/general/downloads/
- Trino: https://github.com/trinodb/trino/releases
- Spark: https://spark.apache.org/releases/
- Iceberg: https://github.com/apache/iceberg/releases
- Dagster: https://github.com/dagster-io/dagster/releases
- Metabase: https://github.com/metabase/metabase/releases

## Sibling reuse

- `../../dataeng/docker-compose.yml:L1-L243` — full stack reference
- `../../dataeng/README.md` — topology notes
- `../../dataeng/dbt_project/` — working dbt project (Phase 3 · 05_dbt)
- `../../dataeng/dagster/lakehouse/` — working Dagster project (Phase 3 · 06_dagster)
- `../../dataeng/dlt_pipelines/` — working dlt pipeline (Phase 3 · 04_dlt)
- Full reuse map: `../references/sibling_sources.md` (grep "Phase 3")

## Books (per `docs/REUSE_POLICY.md`)

- *Fundamentals of Data Engineering*, Reis & Housley — lakehouse chapter
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 3, 10 — storage + batch
- *The Data Warehouse Toolkit*, Kimball, Ch. 1–3, 5 — dimensional modelling basis for dbt marts
