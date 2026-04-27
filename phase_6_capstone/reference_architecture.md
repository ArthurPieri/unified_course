# Reference Architecture

This is the reference topology for the capstone. It is exactly the Phase 3 stack (`../phase_3_core_tools/compose/full-stack/docker-compose.yml`) plus the Phase 4 security/observability additions and the Phase 5 CI/CD layer. Nothing new. The capstone is integration work, not tool discovery — see `../UNIFIED_COURSE_PLAN.md` L523–L548 for the source spec.

You are free to deviate from this reference. If you do, write an ADR explaining why — that ADR itself counts toward Dimension 12 of [`12_dimension_rubric.md`](12_dimension_rubric.md).

## Topology (ASCII)

```
                    +-----------------------------------------------------+
                    |                   SOURCES                           |
                    |                                                     |
                    |   NYC Taxi API        Postgres OLTP     JSON/CSV    |
                    |   (HTTP batch)        (CDC source)      (producer)  |
                    +---------+----------------+-----------------+--------+
                              |                |                 |
                              | HTTP           | Debezium        | file
                              v                v                 v
                    +-----------------------------------------------------+
                    |                     dlt                             |
                    |   (batch + append + CDC pipelines, Python)          |
                    +---------------------------+-------------------------+
                                                |
                                                v
  +----------------+        +-----------------------------------------+
  |                |        |             MinIO (S3-compat)           |
  |  Hive          |<------>|   s3a://lakehouse/bronze/                |
  |  Metastore     | catalog|   s3a://lakehouse/silver/    (Iceberg)   |
  |  (Postgres)    |        |   s3a://lakehouse/gold/                  |
  |                |        +----------+-------------------+----------+
  +-------+--------+                   ^                   ^
          ^                            |                   |
          | jdbc                       | reads/writes      | reads
          |                            |                   |
  +-------+----------+       +---------+---------+  +------+---------+
  |  Trino           |<----->|  Spark (PySpark)  |  |  dbt-trino     |
  |  (query engine,  |       |  (heavy batch     |  |  (staging ->   |
  |   RBAC, masking) |       |   + compaction)   |  |   marts,       |
  +-------+-----+----+       +---------+---------+  |   contracts,   |
          |     |                      ^            |   tests)       |
          |     | jdbc                 |            +-------+--------+
          |     |                      |                    ^
          |     v                      |                    |
          | +-----------+               \______runs_________|
          | | Metabase  |                                   |
          | | (dashbd)  |                                   |
          | +-----------+                                   |
          |                                                 |
          |          +----------------------------+         |
          +--------->|   Dagster (webserver +      |--------+
                     |   daemon, assets, schedules,|
                     |   sensors, retry policies)  |
                     +--+-----------------------+--+
                        ^                       |
                        | scrape                | emit metrics
                        |                       v
                +-------+--------+      +-------+--------+
                |  Prometheus    |----->|  Grafana       |
                |  (metrics,     |      |  (dashboards)  |
                |  alert rules)  |      +----------------+
                +-------+--------+
                        |
                        | firing
                        v
                +----------------+
                | Alert receiver |
                | (webhook/file) |
                +----------------+

        ============== GitHub Actions (CI/CD) ==============
        PR -> lint + dbt compile + dbt test + integration test -> merge
        main -> rebuild images, redeploy compose stack
        ====================================================
```

## Component map

| Component | Responsibility | Tech choice | Alternatives |
|---|---|---|---|
| Source — batch API | Simulates a third-party data feed | Python producer against NYC TLC or GH Archive | Any public HTTP dataset |
| Source — CDC origin | OLTP source for change-data-capture | PostgreSQL + logical replication | MySQL + Debezium |
| Source — streaming | Append-only event stream | Python producer → file drop → dlt | Kafka + Debezium if Phase 4 fully done |
| Ingestion | Extract + land raw data in Bronze | dlt (`dlthub.com`) | Airbyte, Fivetran (not in scope — managed) |
| Object storage | S3-compatible blob store for all table data | MinIO (`min.io`) | Any S3-API store; real S3 in vendor branch |
| Table format | ACID + schema evolution + time travel on object storage | Apache Iceberg (`iceberg.apache.org/spec/`) | Delta Lake, Hudi — see Deliverable 3 in [`fast_track_rubric.md`](fast_track_rubric.md) |
| Catalog | Table metadata registry | Hive Metastore (Postgres-backed) | AWS Glue, REST catalog, Nessie |
| Batch compute | Heavy transformations, compaction, maintenance | Apache Spark + PySpark + Iceberg connector | Trino (for lighter workloads) |
| Query engine | Interactive SQL, RBAC, column masking | Trino (`trino.io`) | Presto, Dremio, DuckDB (single-node) |
| Transformations | Staging → intermediate → marts with contracts and tests | dbt-trino (`docs.getdbt.com`) | SQLMesh, hand-written Spark SQL |
| Orchestration | DAG, schedules, sensors, retries, asset checks | Dagster (`docs.dagster.io`) | Airflow — see Phase 5 · 03_airflow_bridge |
| BI | Dashboards for Gold marts | Metabase (`metabase.com`) | Superset, Lightdash |
| Programmatic serving | Read API over Gold (optional stretch) | FastAPI → Trino | gRPC, direct Trino JDBC |
| Metrics | Time-series collection | Prometheus (`prometheus.io`) | OpenTelemetry collector |
| Dashboards + alerts | Visualization and alert routing | Grafana (`grafana.com`) | Grafana Cloud, Datadog (managed) |
| Secrets | Credentials outside git | `.env` file + docker secrets | Vault, AWS Secrets Manager, Doppler |
| CI/CD | Automated lint, test, deploy | GitHub Actions | GitLab CI, Drone, Jenkins |

## Data flow narrative

**1. Ingestion — sources to Bronze.** dlt pipelines run on a Dagster schedule. The batch pipeline pulls from the API, normalizes the payload, and writes Parquet files into `s3a://lakehouse/bronze/<source>/dt=YYYY-MM-DD/` registered as an Iceberg table in HMS. The CDC pipeline tails the Postgres replication slot via Debezium and appends change events to a Bronze changelog table. The streaming pipeline consumes from a file drop (or Kafka topic in Phase 4) and appends. Bronze is immutable — no updates, no deletes except by retention. Reference: Phase 3 · 04_dlt, `../phase_3_core_tools/04_dlt/`.

**2. Bronze to Silver — dbt staging and intermediate.** dbt-trino runs staging models that rename, cast, and filter. Intermediate models join reference data and apply the first business logic. Schema contracts on the Silver marts catch any upstream drift. `dbt test` runs as a Dagster asset check after the build — if tests fail, downstream Gold assets do not execute. Reference: Phase 3 · 05_dbt and `../dataeng/dbt_project/models/`.

**3. Silver to Gold — marts and aggregates.** Mart models are Kimball-style fact + dimension tables, materialized as Iceberg tables in `s3a://lakehouse/gold/`. Compaction runs on a daily schedule via a Dagster maintenance asset calling Spark. Gold is the only layer Metabase and FastAPI ever query.

**4. Serving.** Metabase connects to Trino via JDBC. Dashboards query Gold only. The FastAPI service exposes read-only endpoints that translate REST parameters into parameterized Trino queries. RBAC and column masking live in Trino — the BI and API layers use separate roles so that unprivileged views of PII columns return masked values.

**5. Orchestration.** Dagster's asset graph mirrors the Bronze→Silver→Gold layering. Schedules trigger ingestion; sensors react to object-landing events in MinIO; asset checks enforce freshness SLOs and fail loudly when breached. Retries with exponential backoff cover network-bound assets (API pulls, Trino queries).

**6. Observability.** Prometheus scrapes Dagster, the Trino coordinator, and the dlt pipeline metrics endpoint. Grafana dashboards show pipeline health — run status, freshness lag, rows per run, test pass rate. At least one alert rule is wired to a receiver (webhook, file, or fake email). When a deliberate failure is injected (`project_brief.md` §Acceptance Criteria), the alert must fire within 5 minutes.

**7. CI/CD.** GitHub Actions runs on every PR: ruff / pre-commit, `dbt compile`, `dbt test` against a CI profile, and an integration smoke test. Merges to main are blocked on failure. A deploy job rebuilds the compose stack and applies it. Reference: `../dataeng/.github/workflows/dbt-ci.yml` and `../dataeng/.github/workflows/pipeline-validation.yml`.

## Concrete instantiation

The concrete starting point for all of this is the Phase 3 full-stack compose file:

- `../phase_3_core_tools/compose/full-stack/docker-compose.yml` — services, pinned versions, volumes, networks
- `../phase_3_core_tools/compose/full-stack/README.md` — bootstrap steps and service URLs
- `../dataeng/docker-compose.yml` — the sibling reference this was built from

Copy that compose file into your capstone repository as the starting point. Add Prometheus + Grafana using `../dataeng/prometheus/prometheus.yml` and `../dataeng/grafana/provisioning/` as references. Add the Dagster project using `../dataeng/dagster/lakehouse/` as the reference layout. Add the dbt project using `../dataeng/dbt_project/` as the reference. Your work is the integration and the hardening — the scaffolding exists, per the course's reuse-first rule (`../docs/REUSE_POLICY.md` §Reuse-first rule).
