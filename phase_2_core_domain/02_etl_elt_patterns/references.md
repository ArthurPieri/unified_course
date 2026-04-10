# References — 02 ETL/ELT Patterns

## Books
- *Fundamentals of Data Engineering*, Reis & Housley — data engineering lifecycle framing (ingestion → transformation → serving)
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 7 — transactions, atomicity, and what "one correct result" means for reruns
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 10 — batch processing fundamentals underpinning ETL/ELT
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — stream processing and change data capture

## Official docs
- [dlt documentation](https://dlthub.com/docs/intro) — Python declarative E+L
- [dlt incremental loading](https://dlthub.com/docs/general-usage/incremental-loading) — cursor-based incrementals
- [dbt documentation](https://docs.getdbt.com/docs/introduction) — SQL transformation framework (the T in ELT)
- [dbt model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts) — schema enforcement at layer boundaries
- [Databricks Medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion) — Bronze/Silver/Gold pattern reference
- [Apache Iceberg spec](https://iceberg.apache.org/spec/) — atomic snapshot commits underpinning safe reruns and backfills
- [Apache Iceberg docs](https://iceberg.apache.org/docs/latest/) — table operations, snapshot management
- [Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html) — canonical CDC implementation reading DB transaction logs
- [Apache Kafka documentation](https://kafka.apache.org/documentation/) — transport for CDC streams
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/) — source-system reference (WAL, logical replication)
- [Trino documentation](https://trino.io/docs/current/) — SQL engine that executes the T on the lakehouse
- [Apache Spark documentation](https://spark.apache.org/docs/latest/) — alternative heavy-transform engine
- [Airflow core concepts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html) — task-DAG model
- [Dagster concepts](https://docs.dagster.io/concepts) — asset-DAG model

## Sibling-dir sources
- `../../../dataeng/dlt_pipelines/taxi_pipeline.py:L52-L110` — concrete dlt incremental-cursor + append pattern (`write_disposition="append"`, `dlt.sources.incremental("tpep_pickup_datetime")`)
- `../../../dataeng/enhanced-plan.md:L460` — "this stack is ELT: dlt = E+L, dbt = T, Trino = compute"
- `../../../dataeng/enhanced-plan.md:L681` — ETL vs. ELT and idempotency listed as core pipeline-paradigm concepts
- `../../../dataeng/enhanced-plan.md:L1565` — Airflow backfill CLI vs. Dagster partitioned-asset backfills
- `../../../dataeng/enhanced-plan.md:L1716-L1748` — Medallion architecture with contracts at Silver
- `../../../dataeng/dbt_project/models/marts/fct_trip_metrics.sql` — Gold-layer fact model example
- `../../../dataeng/dbt_project/snapshots/snap_taxi_zones.sql` — snapshot (change capture) pattern in dbt

## Central course references
- [../../references/books.md](../../references/books.md)
- [../../references/docs.md](../../references/docs.md)
- [../../references/glossary.md](../../references/glossary.md) — CDC, Medallion architecture entries
- [../../references/sibling_sources.md](../../references/sibling_sources.md)
