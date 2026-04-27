# Module 02: Data Loading

Loading is the heaviest domain on Platform (40%, Domain 3.0) and remains first-class on Core (Domain 4.0, 12%) and DEA (Domain 1.0, 28%). The commands and concepts rarely change; the twist at the DEA level is **continuous** loading — Snowpipe vs Snowpipe Streaming vs Kafka connector.

## Learning goals
- List the four stage types and when to use each.
- Write a `COPY INTO` that loads CSV with a header and a named file format.
- Explain how Snowpipe auto-ingest differs from Snowpipe Streaming.
- Describe `INFER_SCHEMA` and when it is valid (Parquet/Avro/ORC).
- Identify which load metadata Snowflake keeps and for how long.

## Prerequisites
- `../01_architecture/` — stages sit in the storage layer; COPY INTO runs on a warehouse.

## Reading order
1. This README
2. [Snowflake Data Loading](https://docs.snowflake.com/en/user-guide/data-load-overview) (structured + semi-structured + stages)
3. [Snowflake Quickstarts](https://quickstarts.snowflake.com/) — hands-on data loading labs
4. `quiz.md`

## Concepts

### Stages — the four types
| Stage | Syntax | Scope | Notes |
|---|---|---|---|
| Internal named | `@stage_name` | Account-wide | Created with `CREATE STAGE`; most flexible. |
| Internal user | `@~` | Per user | Auto-created; cannot be altered or dropped. |
| Internal table | `@%table` | Per table | Auto-created; cannot be altered or dropped. |
| External | `@ext_stage` | Account-wide | Points at S3, GCS, or Azure Blob; uses a storage integration. |

Ref: *SnowPro Associate: Platform Study Guide, §3.1, p. 7* · [Snowflake Data Loading](https://docs.snowflake.com/en/user-guide/data-load-overview).

### File formats and COPY INTO (table)
A **file format object** (`CREATE FILE FORMAT`) captures parse rules (delimiter, header, compression, null representation, etc.) once and is then referenced by name from `COPY INTO`. Inline file format options are allowed but brittle. `COPY INTO` tracks which files have been loaded via **load metadata** retained for **64 days** — it will skip already-loaded files automatically. `PURGE = TRUE` removes source files after a successful load.

Ref: [COPY INTO <table>](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table) · [Snowflake Data Loading](https://docs.snowflake.com/en/user-guide/data-load-overview).

### Semi-structured data
JSON, Avro, Parquet, ORC, and XML land in a `VARIANT` column. Navigate with `:` (top-level), `.` or `[]` (nested). Use `FLATTEN` / `LATERAL FLATTEN` to unnest arrays. `STRIP_OUTER_ARRAY = TRUE` is the usual trick when a JSON file is a top-level array. Snowflake supports **schema-on-read** for these formats — no table schema required to land data.

Ref: [Semi-structured data](https://docs.snowflake.com/en/user-guide/semistructured-concepts) · *SnowPro Core Study Guide, Domain 5.0 "Data Transformations", p. 11*.

### INFER_SCHEMA (DEA-level)
`INFER_SCHEMA` reads Parquet, Avro, or ORC staged files and returns a result set of inferred column names/types. Pair with `GENERATE_COLUMN_DESCRIPTION` and `CREATE TABLE ... USING TEMPLATE` to bootstrap a table DDL. Does **not** support CSV.

Ref: [INFER_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) · *SnowPro Advanced: Data Engineer Study Guide, §1.2, p. 5*.

### Snowpipe — auto-ingest vs REST API
**Snowpipe (auto-ingest)** watches a cloud storage location via an event notification (S3 SNS, GCS Pub/Sub, Azure Event Grid) and loads new files automatically. **Snowpipe (REST API)** is triggered by your code calling `insertFiles`. Both bill as serverless compute — you do not size a warehouse. Monitor with `SYSTEM$PIPE_STATUS` and `VALIDATE_PIPE_LOAD`.

Ref: [Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro) · *SnowPro Advanced: Data Engineer Study Guide, §1.4, p. 5*.

### Snowpipe Streaming vs Kafka connector (DEA)
**Snowpipe Streaming** ingests rows directly into Snowflake over a low-latency SDK — no files, no stages. Latency is typically sub-second to a few seconds. The **Kafka connector** can run in *Snowpipe mode* (batches files) or *Snowpipe Streaming mode* (calls the Streaming SDK). Prefer Snowpipe Streaming for row-level, low-latency pipelines where you own the producer; use the Kafka connector when the source is already Kafka.

Ref: [Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-overview) · [Kafka connector](https://docs.snowflake.com/en/user-guide/kafka-connector-overview) · *DEA Study Guide, §1.4-§1.5, p. 5*.

### Storage integration
A **storage integration** is the canonical way to grant Snowflake access to an external bucket without embedding credentials. One storage integration, many external stages. Required for auto-ingest Snowpipe and external tables.

Ref: [CREATE STORAGE INTEGRATION](https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration) · *DEA Study Guide, §1.2, p. 5*.

## Hands-on drills

| # | Drill | Est. time | Source |
|---|---|---|---|
| D1 | Create a named file format for CSV and load a file from an internal named stage with `COPY INTO`. | 25 min | [Snowflake Quickstarts](https://quickstarts.snowflake.com/) |
| D2 | Load a JSON file into a `VARIANT` column and write a `LATERAL FLATTEN` query to extract nested array elements. | 30 min | [Snowflake Quickstarts](https://quickstarts.snowflake.com/) |
| D3 | Use `INFER_SCHEMA` against a staged Parquet file and `CREATE TABLE ... USING TEMPLATE`. | 25 min | [INFER_SCHEMA docs](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) |
| D4 | Create an external stage backed by a storage integration and a Snowpipe with `AUTO_INGEST = TRUE`; drop a file and confirm it loads. | 45 min | [Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro) |
| D5 | Run `SYSTEM$PIPE_STATUS` and `VALIDATE_PIPE_LOAD` to diagnose a load failure. | 20 min | *DEA Study Guide §1.3, p. 5* |

## Common failures (exam gotchas)

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `COPY INTO` silently loads zero rows on retry | Load metadata dedupes already-loaded files (64-day window) | Use `FORCE = TRUE` or rename the files | `domain_3_0_data_loading.md:L46` |
| JSON top-level array loads as one row | Missing `STRIP_OUTER_ARRAY = TRUE` | Set it in the file format | `domain_3_0_data_loading.md:L49` |
| `INFER_SCHEMA` on CSV returns an error | INFER_SCHEMA does not support CSV | Provide a manual DDL or use a schema-detection tool | [INFER_SCHEMA docs](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) |
| Snowpipe auto-ingest not firing | Missing or wrong event notification / SQS queue ARN | Rebind the notification channel; re-verify with `SYSTEM$PIPE_STATUS` | [Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro) |
| "Use Snowpipe Streaming for all new pipelines" | Over-generalization | Use Snowpipe Streaming for row-level low-latency SDK pipelines; keep file-based Snowpipe when producers emit files | *DEA Study Guide §1.4, p. 5* |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Write a `COPY INTO` with `FILE_FORMAT = (FORMAT_NAME = ...)` and `PURGE = TRUE`.
- [ ] Explain when `INFER_SCHEMA` applies and when it does not.
- [ ] Compare Snowpipe (auto-ingest) vs Snowpipe Streaming in one sentence each.
- [ ] Name the four stage types and identify which cannot be altered.
