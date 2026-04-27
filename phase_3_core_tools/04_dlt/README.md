# Module 04: dlt — Python-native ingestion (6h)

> Code-first ingestion framework. You define Python iterables; dlt handles schema inference, state, incremental cursors, and destination writes.

## Learning goals
- Explain dlt's source/resource/pipeline model and when it beats a hand-written ingestion script.
- Write a `@dlt.resource` with a typed column hint and the correct `write_disposition`.
- Configure `dlt.sources.incremental("column")` and reason about its persisted state.
- Point a pipeline at MinIO (filesystem destination) and at an Iceberg destination.
- Diagnose schema-drift, credential, and cursor-reset failures from `load_info` output.

## Prerequisites
- `phase_3_core_tools/00_stack_overview/`
- `phase_3_core_tools/01_minio_iceberg_hms/`
- `phase_3_core_tools/02_trino/` (for verification queries)

## Reading order
1. This README
2. `labs/lab_L3b_dlt_ingest/README.md`
3. `quiz.md`

## Concepts

### Value proposition
dlt is a Python library, not a service: `pip install dlt`, write a function that yields records, run it. It auto-infers schemas from the data, persists cursor state between runs so re-executions are idempotent, and normalises nested JSON into relational tables without hand-written DDL. Its niche is **many small, heterogeneous sources** (REST APIs, SaaS exports, scraped files) where writing a custom loader per source is wasted effort. For a single heavy custom source — e.g. a bespoke binary protocol or a CDC stream — a hand-written script or Spark job usually wins because dlt's row-at-a-time model adds overhead.
Ref: [dlt — Why dlt?](https://dlthub.com/docs/reference/explainers/how-dlt-works)

### Source → resource → pipeline
The three-layer model maps cleanly to responsibilities.
- A **resource** is a Python generator decorated with `@dlt.resource` that yields records for one logical table. It owns the write disposition, primary key, and column hints.
- A **source** is a `@dlt.source`-decorated function that groups related resources (e.g. `users` + `orders` from one API) and shares auth.
- A **pipeline** is the runtime object: `dlt.pipeline(pipeline_name=..., destination=..., dataset_name=...)`. Calling `pipeline.run(source)` extracts, normalises, and loads.
See the lab's `pipeline.py` for the resource pattern and the source wrapper.
Ref: [dlt — Sources & resources](https://dlthub.com/docs/general-usage/source)

### Write dispositions
Set on the resource via `write_disposition=`:
- `replace` — truncate the destination table and reload. Fine for small dimensions.
- `append` — add new rows. The default for log-style data. Used by `taxi_pipeline.py:L54`.
- `merge` — upsert by `primary_key` (or `merge_key`). Required when the source emits updates and you need a current-state table. Without a primary key, `merge` errors out.
Ref: [dlt — Write dispositions](https://dlthub.com/docs/general-usage/incremental-loading#choosing-a-write-disposition)

### Incremental loading
`dlt.sources.incremental("tpep_pickup_datetime")` wraps a cursor column. On the first run it stores `max(column)` as state; on subsequent runs it passes that value back into the resource so you can filter the source (or, as in `taxi_pipeline.py:L66-L110`, hand dlt an Arrow batch and let it drop already-seen rows). State lives under `~/.dlt/pipelines/<pipeline_name>/state.json` and in the destination's `_dlt_pipeline_state` table, so state survives a wiped local dir. Reset it with `pipeline.drop()` or by passing `--reset-state`.
Primary pattern: the canonical incremental-append pattern used by this phase is in the lab's `pipeline.py`.
Ref: [dlt — Incremental loading](https://dlthub.com/docs/general-usage/incremental-loading)

### Destinations: filesystem and Iceberg
The **filesystem** destination writes Parquet (or JSONL) to a bucket. Against MinIO, set `destination.filesystem.bucket_url = "s3://lakehouse"` and provide S3-compatible credentials plus `endpoint_url = "http://minio:9000"` in `.dlt/config.toml` (or `DESTINATION__FILESYSTEM__*` env vars). Trino/Spark then register an Iceberg table on top of the Parquet layout — that is the pattern `taxi_pipeline.py` uses.
The **iceberg** destination (dlt ≥ 1.x) writes Iceberg tables directly via PyIceberg, using a catalog you configure (REST, SQL, or Hive). Credentials resolve from `config.toml` → env (`DESTINATION__ICEBERG__CREDENTIALS__*`) → `~/.dlt/secrets.toml`. For the full-stack compose in this phase, both approaches land in `s3://lakehouse/` on MinIO and become queryable through the Trino `iceberg` catalog wired in `phase_3_core_tools/compose/full-stack/docker-compose.yml:L105-L125`.
Refs: [dlt — Filesystem destination](https://dlthub.com/docs/dlt-ecosystem/destinations/filesystem) · [dlt — Iceberg destination](https://dlthub.com/docs/dlt-ecosystem/destinations/iceberg) · [Iceberg Trino connector](https://trino.io/docs/current/connector/iceberg.html)

### Pipeline state and resumability
State is the thing that makes dlt re-runs safe. Every resource that uses `incremental` stores its cursor high-water-mark; every load writes a row to `_dlt_loads` tagging which package of data landed. If a run crashes mid-load, the next run replays the failed load package, not the full history. This is why dlt's idempotency guarantee is "per load package", not "per row": the unit of retry is the package.
Ref: [dlt — Pipeline state](https://dlthub.com/docs/general-usage/state)

### When dlt vs hand-written
Choose dlt when: you have ten sources and don't want to write ten loaders; the sources emit paginated JSON; you need schema evolution without writing migrations; the team knows Python but not Spark. Choose a hand-written script or Spark job when: there is one source and it's large and weird; you already have a mature framework; you need sub-second latency (dlt is batch). The taxi Parquet lab is a borderline case — dlt is used here because the pattern generalises to any HTTP Parquet feed, not because it is strictly cheaper than `pyarrow.parquet.read_table` + a direct S3 write.

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L3b_dlt_ingest` | Ingest NYC taxi Parquet into MinIO as an Iceberg table with incremental cursor, verify via Trino | 60m | [labs/lab_L3b_dlt_ingest/](labs/lab_L3b_dlt_ingest/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `SchemaCorruptedException` on 2nd run | New column in source, `schema_contract="freeze"` | Set `schema_contract="evolve"` on the resource or add the column to hints | [dlt — Schema contracts](https://dlthub.com/docs/general-usage/schema-contracts) |
| `botocore ... InvalidAccessKeyId` | MinIO creds missing from `.dlt/secrets.toml` | Export `DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID` and `..._AWS_SECRET_ACCESS_KEY` | [dlt — Filesystem credentials](https://dlthub.com/docs/dlt-ecosystem/destinations/filesystem#setup-credentials) |
| Incremental run reloads everything | `pipeline.drop()` called or `~/.dlt/pipelines/<name>` deleted | State is the source of truth — keep it or accept the full reload | [dlt — Incremental state](https://dlthub.com/docs/general-usage/incremental-loading) |
| `merge` fails with "no primary key" | `write_disposition="merge"` without `primary_key=` | Add `primary_key="id"` on the resource | [dlt — Merge](https://dlthub.com/docs/general-usage/incremental-loading#merge-incremental-loading) |
| Endpoint URL ignored | Using `s3://` against MinIO without `endpoint_url` | Set `[destination.filesystem.credentials]` → `endpoint_url = "http://minio:9000"` | [dlt — Filesystem credentials](https://dlthub.com/docs/dlt-ecosystem/destinations/filesystem#setup-credentials) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Describe in two sentences the difference between a `@dlt.source` and a `@dlt.resource`.
- [ ] Pick the right `write_disposition` for (a) a daily events feed, (b) a small dim table, (c) a user table with updates.
- [ ] Explain where incremental cursor state lives and what deletes it.
- [ ] Run `pipeline.py` against the Phase 3 full-stack compose and see a non-zero row count from Trino.
- [ ] Read `load_info` output and identify the load package id.
