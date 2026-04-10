# Module 04: dlt — References

## Primary reuse (sibling source)
- `../dataeng/dlt_pipelines/taxi_pipeline.py:L52-L110` — canonical `@dlt.resource` with incremental cursor on `tpep_pickup_datetime`; batch-yield pattern from pyarrow.
- `../dataeng/dlt_pipelines/taxi_pipeline.py:L118-L132` — `@dlt.source` wrapper grouping the resource.
- `../dataeng/dlt_pipelines/taxi_pipeline.py:L140-L166` — `dlt.pipeline(...)` construction + `pipeline.run(source)` with `load_info` print.
- `../dataeng/dlt_pipelines/.dlt/config.toml` — filesystem destination + MinIO endpoint credentials pattern.
- `../dataeng/dagster/lakehouse/resources/dlt_resource.py` — dlt wrapped as a Dagster resource (forward reference for Module 06).
- `../dataeng/tests/test_dlt_pipelines/test_taxi_pipeline.py` — pipeline-level pytest pattern.

## Official dlt docs (dlthub.com)
- [How dlt works](https://dlthub.com/docs/reference/explainers/how-dlt-works) — extract/normalise/load model.
- [Sources](https://dlthub.com/docs/general-usage/source) — `@dlt.source` decorator, grouping resources.
- [Resources](https://dlthub.com/docs/general-usage/resource) — `@dlt.resource`, column hints, primary keys.
- [Incremental loading](https://dlthub.com/docs/general-usage/incremental-loading) — cursor columns, merge vs append, state.
- [Write dispositions](https://dlthub.com/docs/general-usage/incremental-loading#choosing-a-write-disposition) — replace / append / merge semantics.
- [Pipeline state](https://dlthub.com/docs/general-usage/state) — where state lives, resumability.
- [Schema contracts](https://dlthub.com/docs/general-usage/schema-contracts) — evolve / freeze / discard behaviours.
- [Filesystem destination](https://dlthub.com/docs/dlt-ecosystem/destinations/filesystem) — Parquet/JSONL to S3/MinIO, credential setup.
- [Iceberg destination](https://dlthub.com/docs/dlt-ecosystem/destinations/iceberg) — PyIceberg-backed direct writes.
- [Configuration & secrets](https://dlthub.com/docs/general-usage/credentials) — `.dlt/config.toml`, env var mapping.

## Destination / engine docs
- [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) — verification query engine for the lab.
- [Apache Iceberg — Spark writes](https://iceberg.apache.org/docs/latest/spark-writes/) — reference for the Spark-side Iceberg config used by the compose stack.
- [Iceberg table spec](https://iceberg.apache.org/spec/) — format spec referenced when reasoning about snapshots and schema evolution.
- [MinIO — S3 compatibility](https://min.io/docs/minio/linux/developers/python/minio-py.html) — endpoint/credentials semantics for the filesystem destination.

## Compose context
- `phase_3_core_tools/compose/full-stack/docker-compose.yml` — MinIO (L26-L44), Hive Metastore (L71-L98), Trino (L105-L125) used by the lab.
