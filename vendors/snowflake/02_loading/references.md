# Module 02 — References

## Snowflake docs
- [Loading data overview](https://docs.snowflake.com/en/user-guide/data-load-overview)
- [COPY INTO <table>](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table)
- [CREATE STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage)
- [CREATE FILE FORMAT](https://docs.snowflake.com/en/sql-reference/sql/create-file-format)
- [CREATE STORAGE INTEGRATION](https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration)
- [Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro)
- [Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-overview)
- [Kafka connector](https://docs.snowflake.com/en/user-guide/kafka-connector-overview)
- [INFER_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema)
- [Semi-structured data](https://docs.snowflake.com/en/user-guide/semistructured-concepts)
- [SYSTEM$PIPE_STATUS](https://docs.snowflake.com/en/sql-reference/functions/system_pipe_status)
- [VALIDATE_PIPE_LOAD](https://docs.snowflake.com/en/sql-reference/functions/validate_pipe_load)

## Official study guides
- *SnowPro Associate: Platform Study Guide*, Domain 3.0 "Data Loading and Virtual Warehouses", p. 7 — stages, COPY INTO, INSERT, LIST, file formats, structured/semi-structured.
- *SnowPro Core Study Guide*, Domain 4.0 "Data Loading and Unloading", p. 10 — Snowpipe, loading best practices, loading commands, unloading.
- *SnowPro Advanced: Data Engineer Study Guide*, Domain 1.0 "Data Movement", pp. 5-6 — 1.2 ingest of various formats, 1.3 troubleshoot ingestion, 1.4 continuous pipelines, 1.5 connectors.

## Sibling reuse
- `../../../../snowflake_eng/phase1_platform/study_notes/domain_3_0_data_loading.md:L16-L100` — stages, file formats, loading commands, semi-structured.
- `../../../../snowflake_eng/phase1_platform/labs/lab_02_data_loading.sql:L1-L400+` — end-to-end data loading SQL lab with file formats, COPY INTO, JSON/VARIANT.
