# Appendix A — Data Architecture Landscape

## Why this appendix

Phase 2 teaches the core domain hands-on (modeling, ETL/ELT, distributed systems, streaming, lakehouse). This appendix is the 50,000-ft view that V1 Finding #4 moved out of Phase 2 to keep that phase tight. Read it once when you want to place a new tool or pattern on the map; it is not required to finish the course.

Everything below cites a primary source. If a claim is here, you can trace it to a book chapter, a spec, or an official vendor page. See [references.md](references.md) for the full citation list.

## The archetypes

### Data Warehouse — Inmon CIF (Corporate Information Factory)

A centrally modeled, normalized enterprise layer (3NF) feeds topic-specific data marts. The defining constraint is a single integrated enterprise data model built before marts. Subject-oriented, integrated, time-variant, non-volatile — the canonical four properties. See *Building the Data Warehouse*, Inmon, Ch. 1–3.

### Data Warehouse — Kimball bus architecture

Dimensional modeling (stars and snowflakes) with conformed dimensions shared across process-oriented fact tables. The defining constraint is the enterprise bus matrix: dimensions are conformed, facts are additive where possible, grain is declared per fact table. See *The Data Warehouse Toolkit* (3rd ed.), Kimball & Ross, Ch. 1–3 for the four-step design process and Ch. 5 for SCDs.

### Data Lake

Schema-on-read storage of raw files in object storage. The defining constraint is that the system accepts any shape and defers schema resolution to query time. Kleppmann's treatment of schema-on-read versus schema-on-write is the clearest concept anchor: *Designing Data-Intensive Applications*, Ch. 4.

### Lakehouse

Object-storage data lake plus an open table format (Iceberg, Delta, Hudi) that adds ACID commits, snapshots, schema evolution, and time travel. The defining constraint is catalog-mediated atomic commits against files that any engine can read. Canonical specs: [Apache Iceberg table spec](https://iceberg.apache.org/spec/) and the [Delta Lake protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Fabric and Databricks documentation both describe the medallion pattern — Bronze (raw) → Silver (cleaned) → Gold (serving) — as the operating model layered on top (see [Databricks medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion)).

### Data Mesh

An organizational pattern: domain-oriented ownership of data-as-a-product, self-serve platform, federated computational governance. The defining constraint is domain ownership — the team that produces the data also publishes and supports it. Canonical source: Zhamak Dehghani's principles post, [martinfowler.com/articles/data-mesh-principles.html](https://martinfowler.com/articles/data-mesh-principles.html).

### Lambda vs Kappa

Lambda runs a batch layer and a speed layer in parallel and reconciles results in a serving layer. Kappa replaces both with a single replayable log. Kleppmann treats both in *DDIA*, Ch. 11 (Stream Processing) as consequences of choosing log-replay versus dual-path reprocessing. Kafka's documentation on [log compaction](https://kafka.apache.org/documentation/#compaction) and [delivery semantics](https://kafka.apache.org/documentation/#semantics) is the primary source for why a replayable log can serve as the source of truth.

## Which course module covers what

| Archetype | Taught in |
|---|---|
| Dimensional modeling (Kimball) | [phase_2_core_domain/01_data_modeling](../phase_2_core_domain/01_data_modeling/) |
| 3NF / Inmon / Data Vault | [phase_2_core_domain/01_data_modeling](../phase_2_core_domain/01_data_modeling/) |
| ETL vs ELT + medallion | [phase_2_core_domain/02_etl_elt_patterns](../phase_2_core_domain/02_etl_elt_patterns/) |
| Distributed storage + replication | [phase_2_core_domain/03_distributed_systems](../phase_2_core_domain/03_distributed_systems/) |
| Streaming / Lambda / Kappa | [phase_2_core_domain/05_streaming_concepts](../phase_2_core_domain/05_streaming_concepts/) |
| Lakehouse (concept) | [phase_2_core_domain/06_lakehouse_bridge](../phase_2_core_domain/06_lakehouse_bridge/) |
| Lakehouse (hands-on: MinIO + Iceberg + HMS) | [phase_3_core_tools/01_minio_iceberg_hms](../phase_3_core_tools/01_minio_iceberg_hms/) |
| CDC (reasoning about change streams) | [phase_4_specializations/01_cdc_debezium](../phase_4_specializations/01_cdc_debezium/) |
| Warehouse on Snowflake | [vendors/snowflake/](../vendors/snowflake/) |
| Lakehouse on Databricks / Fabric | [vendors/azure/03_compute_synapse_databricks_fabric](../vendors/azure/03_compute_synapse_databricks_fabric/) |
| Lakehouse on AWS (S3 + Athena + Glue) | [vendors/aws/01_storage_s3_lakeformation](../vendors/aws/01_storage_s3_lakeformation/), [vendors/aws/03_compute_emr_athena_redshift](../vendors/aws/03_compute_emr_athena_redshift/) |

Data Mesh has no dedicated module — it is an organizational layer, not a tool stack. The module on data governance ([phase_4_specializations/04_security_governance](../phase_4_specializations/04_security_governance/)) covers the closest technical surface: contracts, ownership, lineage.

## Reading order if you want the deep dive

1. *Fundamentals of Data Engineering*, Reis & Housley — whole-lifecycle framing.
2. *The Data Warehouse Toolkit* (3rd ed.), Kimball & Ross, Ch. 1–3, 5 — dimensional modeling and SCDs.
3. *Building the Data Warehouse* (4th ed.), Inmon, Ch. 1–3 — the CIF contrast.
4. *Designing Data-Intensive Applications*, Kleppmann, Ch. 3 (storage engines), Ch. 4 (encoding and schema evolution), Ch. 10 (batch), Ch. 11 (streams).
5. [Iceberg spec](https://iceberg.apache.org/spec/) + [Delta protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md) — read enough to understand snapshots, manifests, and commit protocols.
6. [Databricks medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion) — the pattern layered on top.
7. [Data Mesh principles](https://martinfowler.com/articles/data-mesh-principles.html) — the organizational argument.
8. *Building a Scalable Data Warehouse with Data Vault 2.0*, Linstedt & Olschimke — if you encounter a hub/link/satellite modeling environment.

If you only have time for one item: *Designing Data-Intensive Applications*, Ch. 10–11. Those two chapters carry the course.
