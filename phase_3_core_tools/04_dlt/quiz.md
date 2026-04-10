# Module 04: dlt — Quiz

8 multiple-choice questions. Answer key at the bottom.

---

**1.** Which statement best describes the relationship between `@dlt.source` and `@dlt.resource`?
- A. A source runs a resource on a schedule.
- B. A resource is a generator yielding rows for one table; a source groups related resources and shares config/auth.
- C. They are aliases for the same decorator.
- D. A resource is a destination adapter; a source is the pipeline runner.

**2.** You need to load a `users` table where rows are *updated* over time and the destination must reflect the latest state. Which `write_disposition` is correct?
- A. `append` with no primary key
- B. `replace` on every run
- C. `merge` with `primary_key="user_id"`
- D. `upsert` (dlt's default)

**3.** `dlt.sources.incremental("tpep_pickup_datetime")` is passed as a resource argument. What does dlt persist between runs?
- A. The full row set of the previous load.
- B. The maximum observed value of `tpep_pickup_datetime`, used as the next run's low-water-mark.
- C. Nothing — incremental is stateless and re-reads the source each run.
- D. A hash of each row, for dedup.

**4.** A learner deletes `~/.dlt/pipelines/nyc_taxi/` and reruns the pipeline. What happens?
- A. dlt refuses to run because state is missing.
- B. State is rebuilt from the destination's `_dlt_pipeline_state` table if present; otherwise the incremental cursor restarts from zero and data is reloaded.
- C. Only the last load package is replayed.
- D. The destination is dropped.

**5.** You are pointing the filesystem destination at MinIO. Which configuration is required in addition to `aws_access_key_id` / `aws_secret_access_key`?
- A. `region_name = "us-east-1"` only.
- B. An explicit `endpoint_url` pointing at the MinIO service (e.g. `http://minio:9000`).
- C. A Hive Metastore URI.
- D. Nothing — dlt auto-detects MinIO.

**6.** In `../dataeng/dlt_pipelines/taxi_pipeline.py:L52-L110`, the resource yields `pyarrow.Table` batches instead of Python dicts. The main reason is:
- A. dlt only accepts Arrow input.
- B. Arrow batches keep memory bounded and preserve types through the extract stage.
- C. It bypasses the normaliser entirely.
- D. It enables streaming merges.

**7.** When does a hand-written ingestion script typically beat dlt?
- A. When there are ten small REST APIs to ingest.
- B. When the source is a single, large, bespoke system and you need maximum throughput or sub-second latency.
- C. When you want automatic schema inference.
- D. When you need idempotent re-runs.

**8.** Which failure mode matches the symptom "second run errors with `SchemaCorruptedException` after the upstream source added a new column"?
- A. Missing primary key on a merge resource.
- B. Schema contract set to `freeze`; change to `evolve` or add the column to hints.
- C. Incremental cursor reset.
- D. MinIO endpoint URL not configured.

---

## Answer key
1. **B** — source groups resources; resource is the table-level generator.
2. **C** — `merge` is the only disposition that upserts; it requires a primary or merge key.
3. **B** — dlt stores the max cursor value and uses it as the next lower bound.
4. **B** — `_dlt_pipeline_state` in the destination is the durable copy; without it the cursor restarts.
5. **B** — MinIO requires an explicit S3 endpoint URL; without it the boto client targets AWS.
6. **B** — Arrow batches bound memory (see `taxi_pipeline.py:L107-L110`) and keep types intact.
7. **B** — dlt's sweet spot is many small sources; single heavy/low-latency sources favour custom code.
8. **B** — `schema_contract="evolve"` allows new columns; `freeze` rejects them.
