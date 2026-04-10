# Sibling Sources — Reusable Content Index

Authoritative index of content already written in sibling directories. **Module-building agents grep this file before writing new content** — reuse first, write only for gaps.

Last scanned: 2026-04-10

## Legend
- Paths are relative to `unified_course/`
- Topic tags are lowercase, dash-separated
- "Maps to" uses course phase/module paths from `UNIFIED_COURSE_PLAN.md`
- Citation format: `../<sibling>/<path>:L<start>-L<end>`

---

## `../linux_fundamentals/` — LFCA curriculum (6 modules + PDFs)

| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../linux_fundamentals/course/01-linux-fundamentals.md` | notes | linux, bash, filesystem, permissions | LFCA Domain 1 — shell, FHS, users/groups, process control | Phase 1 · 01_linux_bash |
| `../linux_fundamentals/course/02-system-administration.md` | notes | sysadmin, systemd, logs, cron | Services, journaling, scheduling | Phase 1 · 01_linux_bash |
| `../linux_fundamentals/course/03-cloud-computing.md` | notes | cloud-concepts, iaas, paas | LFCA cloud fundamentals | Phase 5 · 04_cloud_concepts |
| `../linux_fundamentals/course/04-security-fundamentals.md` | notes | security, ssh, firewall, encryption | Baseline security practices | Phase 1 · 02_networking / Phase 4 · 04_security_governance |
| `../linux_fundamentals/course/05-devops-fundamentals.md` | notes | devops, ci-cd, iac | CI/CD intro, containers intro | Phase 5 · 01_cicd |
| `../linux_fundamentals/course/06-project-management.md` | notes | agile, scrum, itil | Soft-skills / PM basics | Phase 0 · 01_course_structure (optional) |
| `../linux_fundamentals/IMPLEMENTATION_PLAN.md` | plan | lfca, curriculum | Original LFCA study plan | reference only |

**No PDFs currently checked in** (prior summary referenced 3 PDFs — not present in current tree). Cite only the markdown modules above.

---

## `../dataeng/` — Working lakehouse stack (primary Phase 3 source)

### Compose, infra, config
| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../dataeng/docker-compose.yml` | compose | docker, minio, iceberg, hms, trino, spark, dagster, metabase | **Full-stack reference compose** — pinned versions, volumes, networks | Phase 3 · compose/full-stack |
| `../dataeng/pyproject.toml` | config | python, uv, deps | Python project layout + pinned deps | Phase 1 · 03_python |
| `../dataeng/README.md` | notes | lakehouse, stack-overview | Stack topology, service map | Phase 3 · 00_stack_overview |
| `../dataeng/prometheus/prometheus.yml` | config | prometheus, observability | Scrape config | Phase 4 · 06_observability |
| `../dataeng/grafana/provisioning/**` | config | grafana, dashboards | Datasource + dashboard provisioning | Phase 4 · 06_observability |
| `../dataeng/k8s/kind-config.yaml` | config | kubernetes, kind | Local K8s cluster config | Phase 5 · 02_kubernetes_basics |
| `../dataeng/k8s/trino-values.yaml` | helm | kubernetes, trino | Trino Helm values | Phase 5 · 02_kubernetes_basics |
| `../dataeng/k8s/README.md` | notes | kubernetes | Kind+Trino deployment notes | Phase 5 · 02_kubernetes_basics |

### dbt project (fully working)
| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../dataeng/dbt_project/dbt_project.yml` | dbt | dbt, project-config | Project wiring | Phase 3 · 05_dbt |
| `../dataeng/dbt_project/profiles.yml` | dbt | dbt, trino-adapter | dbt-trino connection | Phase 3 · 05_dbt |
| `../dataeng/dbt_project/models/sources.yml` | dbt | dbt, sources | Source declarations | Phase 3 · 05_dbt |
| `../dataeng/dbt_project/models/staging/stg_taxi_trips.sql` | dbt | dbt, staging | Staging model pattern | Phase 3 · 05_dbt · lab L3c |
| `../dataeng/dbt_project/models/staging/stg_taxi_zones.sql` | dbt | dbt, staging | Staging dim source | Phase 3 · 05_dbt · lab L3c |
| `../dataeng/dbt_project/models/intermediate/int_trips_enriched.sql` | dbt | dbt, intermediate | Join + enrichment pattern | Phase 3 · 05_dbt |
| `../dataeng/dbt_project/models/marts/dim_zones.sql` | dbt | dbt, dimension, kimball | Dimension table | Phase 2 · 01_data_modeling · Phase 3 · 05_dbt |
| `../dataeng/dbt_project/models/marts/fct_trip_metrics.sql` | dbt | dbt, fact, kimball | Fact table | Phase 2 · 01_data_modeling · Phase 3 · 05_dbt |
| `../dataeng/dbt_project/models/marts/fct_daily_revenue.sql` | dbt | dbt, fact, aggregate | Aggregate fact | Phase 3 · 05_dbt |
| `../dataeng/dbt_project/snapshots/snap_taxi_zones.sql` | dbt | dbt, scd-type-2 | Snapshot/SCD Type 2 | Phase 2 · 01_data_modeling |
| `../dataeng/dbt_project/tests/assert_positive_revenue.sql` | dbt | dbt, singular-test | Custom data test | Phase 2 · 04_data_quality |
| `../dataeng/dbt_project/unit_tests/test_revenue_calculation.yml` | dbt | dbt, unit-test | Unit test pattern | Phase 2 · 04_data_quality |
| `../dataeng/dbt_project/macros/generate_schema_name.sql` | dbt | dbt, macros | Custom macro | Phase 3 · 05_dbt |

### Dagster project (fully working)
| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../dataeng/dagster/dagster.yaml` | config | dagster | Instance config | Phase 3 · 06_dagster |
| `../dataeng/dagster/workspace.yaml` | config | dagster | Code location wiring | Phase 3 · 06_dagster |
| `../dataeng/dagster/Dockerfile` | docker | dagster, docker | Runtime image | Phase 3 · 06_dagster |
| `../dataeng/dagster/lakehouse/assets/ingestion.py` | python | dagster, assets, dlt | Software-defined ingestion assets | Phase 3 · 06_dagster / Phase 4 · advanced-orchestration |
| `../dataeng/dagster/lakehouse/assets/transformation.py` | python | dagster, assets, dbt | dbt-to-asset bridge | Phase 3 · 06_dagster |
| `../dataeng/dagster/lakehouse/assets/quality.py` | python | dagster, assets, dq | Quality-check assets | Phase 2 · 04_data_quality |
| `../dataeng/dagster/lakehouse/assets/maintenance.py` | python | dagster, iceberg, compaction | Table maintenance jobs | Phase 3 · 06_dagster |
| `../dataeng/dagster/lakehouse/resources/dbt_resource.py` | python | dagster, dbt | Resource wiring | Phase 3 · 06_dagster |
| `../dataeng/dagster/lakehouse/resources/dlt_resource.py` | python | dagster, dlt | Resource wiring | Phase 3 · 06_dagster |
| `../dataeng/dagster/lakehouse/resources/trino_resource.py` | python | dagster, trino | Resource wiring | Phase 3 · 06_dagster |
| `../dataeng/dagster/lakehouse/schedules/daily_pipeline.py` | python | dagster, schedules | Schedule pattern | Phase 3 · 06_dagster |
| `../dataeng/dagster/lakehouse/sensors/minio_sensor.py` | python | dagster, sensors, minio | Object-landing sensor | Phase 4 · advanced-orchestration |

### dlt pipelines
| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../dataeng/dlt_pipelines/taxi_pipeline.py` | python | dlt, ingest, rest-api | End-to-end dlt pipeline | Phase 3 · 04_dlt · lab L3b |
| `../dataeng/dlt_pipelines/.dlt/config.toml` | config | dlt | Pipeline config | Phase 3 · 04_dlt |

### Tests / CI
| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../dataeng/tests/conftest.py` | python | pytest, fixtures | Test fixtures | Phase 1 · 03_python |
| `../dataeng/tests/test_dagster/test_assets.py` | python | dagster, testing | Asset unit tests | Phase 3 · 06_dagster |
| `../dataeng/tests/test_dlt_pipelines/test_taxi_pipeline.py` | python | dlt, testing | dlt pipeline tests | Phase 3 · 04_dlt |
| `../dataeng/tests/test_integration/test_end_to_end.py` | python | integration-test | Full-stack smoke test | Phase 3 · checkpoint_Q3 |
| `../dataeng/.github/workflows/dbt-ci.yml` | ci | github-actions, dbt | dbt CI pipeline | Phase 5 · 01_cicd |
| `../dataeng/.github/workflows/pipeline-validation.yml` | ci | github-actions | Full pipeline CI | Phase 5 · 01_cicd |

### Docs
| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../dataeng/docs/cloud-migration/README.md` | notes | cloud, migration | Lakehouse-to-cloud port notes | Phase 5 · 04_cloud_concepts |
| `../dataeng/enhanced-plan.md` | plan | dataeng, curriculum | Original dataeng build plan | reference only |

---

## `../aws_certified/` — DEA-C01 week-by-week curriculum + 11 labs

| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../aws_certified/data-engineer-associate-01.pdf` | PDF | dea-c01, exam-guide | Official AWS DEA-C01 exam guide | Vendor AWS · 00_exam_profile |
| `../aws_certified/docs/study-plan.md` | plan | dea-c01, curriculum | 12-week study plan | Vendor AWS · 00_exam_profile |
| `../aws_certified/docs/week-01-ingestion-fundamentals.md` | notes | aws, ingestion, kinesis, dms | Ingestion fundamentals | Vendor AWS · 02_ingestion |
| `../aws_certified/docs/week-02-streaming-ingestion.md` | notes | aws, kinesis, msk, streaming | Streaming services | Vendor AWS · 02_ingestion |
| `../aws_certified/docs/week-03-data-transformation.md` | notes | aws, glue, emr, spark | Transformation services | Vendor AWS · 03_compute |
| `../aws_certified/docs/week-04-orchestration.md` | notes | aws, mwaa, step-functions | Orchestration | Vendor AWS · 04_orchestration |
| `../aws_certified/docs/week-05-data-store-selection.md` | notes | aws, s3, redshift, dynamodb | Store selection | Vendor AWS · 01_storage |
| `../aws_certified/docs/week-06-cataloging-data-lakes.md` | notes | aws, glue-catalog, lakeformation | Cataloging, data lakes | Vendor AWS · 01_storage |
| `../aws_certified/docs/week-07-lifecycle-schema.md` | notes | aws, s3-lifecycle, schema-evolution | Lifecycle, schema | Vendor AWS · 01_storage |
| `../aws_certified/docs/week-08-automation-analysis.md` | notes | aws, athena, quicksight | Automation, analysis | Vendor AWS · 03_compute |
| `../aws_certified/docs/week-09-monitoring-quality.md` | notes | aws, cloudwatch, dq | Monitoring, quality | Vendor AWS · 05_security + Phase 4 · 06_observability |
| `../aws_certified/docs/week-10-security-governance.md` | notes | aws, iam, kms, lake-formation | Security, governance | Vendor AWS · 05_security · Phase 5 · 05_iam_primer |
| `../aws_certified/docs/week-11-cross-domain.md` | notes | aws, integration | Cross-service patterns | Vendor AWS · 06_cost_finops |
| `../aws_certified/docs/week-12-mock-exam-1.md` | mock-exam | dea-c01 | Mock exam set 1 | Vendor AWS · mock_exam_sources |
| `../aws_certified/docs/week-12-mock-exam-2.md` | mock-exam | dea-c01 | Mock exam set 2 | Vendor AWS · mock_exam_sources |
| `../aws_certified/labs/week-01-lab-ingestion.md` | lab | aws, s3, kinesis | Ingestion lab | Vendor AWS · labs |
| `../aws_certified/labs/week-02-lab-streaming.md` | lab | aws, kinesis | Streaming lab | Vendor AWS · labs |
| `../aws_certified/labs/week-03-lab-transformation.md` | lab | aws, glue | Glue lab | Vendor AWS · labs |
| `../aws_certified/labs/week-04-lab-orchestration.md` | lab | aws, mwaa | MWAA lab | Vendor AWS · labs |
| `../aws_certified/labs/week-05-lab-datastores.md` | lab | aws, redshift | Datastore lab | Vendor AWS · labs |
| `../aws_certified/labs/week-06-lab-datalake.md` | lab | aws, lakeformation | Data lake lab | Vendor AWS · labs |
| `../aws_certified/labs/week-07-lab-lifecycle.md` | lab | aws, s3-lifecycle | Lifecycle lab | Vendor AWS · labs |
| `../aws_certified/labs/week-08-lab-automation.md` | lab | aws, athena | Automation lab | Vendor AWS · labs |
| `../aws_certified/labs/week-09-lab-monitoring.md` | lab | aws, cloudwatch | Monitoring lab | Vendor AWS · labs |
| `../aws_certified/labs/week-10-lab-security.md` | lab | aws, iam, kms | Security lab | Vendor AWS · labs · Phase 5 · 05_iam_primer |
| `../aws_certified/labs/week-11-lab-capstone.md` | lab | aws, capstone | Capstone lab | Vendor AWS · labs |

**LocalStack strategy** for IAM primer (Phase 5 · 05): mine week-10-lab-security.md for IAM policy examples and adapt to LocalStack.

---

## `../azure_certified/` — DP-700 curriculum + Fabric labs

| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../azure_certified/IMPLEMENTATION-PLAN.md` | plan | dp-700, curriculum | DP-700 build plan | Vendor Azure · 00_exam_profile |
| `../azure_certified/flashcards/top-33-flashcards.md` | flashcards | dp-700, fabric, synapse | Top 33 concept flashcards | Vendor Azure · 00_exam_profile |
| `../azure_certified/labs/01-delta-lake-fundamentals.ipynb` | notebook | delta-lake, pyspark | Delta Lake intro (Databricks-tied) | Vendor Azure · 01_storage (adapt) |
| `../azure_certified/labs/02-spark-transformations.ipynb` | notebook | pyspark, dataframe | Spark transforms | Vendor Azure · 03_compute |
| `../azure_certified/labs/03-structured-streaming.ipynb` | notebook | spark-streaming | Structured Streaming | Vendor Azure · 02_ingestion |
| `../azure_certified/labs/04-batch-and-pipeline-patterns.md` | lab | fabric, adf, pipelines | Batch + pipeline patterns | Vendor Azure · 04_orchestration |
| `../azure_certified/labs/05-security-monitoring-optimization.md` | lab | azure, security, monitor | Security, monitor, tune | Vendor Azure · 05_security |
| `../azure_certified/labs/06-tsql-exercises.md` | lab | tsql, synapse | T-SQL exercises | Vendor Azure · 03_compute |
| `../azure_certified/labs/07-kql-exercises.md` | lab | kql, adx | KQL for log analytics | Vendor Azure · 03_compute |
| `../azure_certified/labs/datasets-guide.md` | notes | datasets | Dataset sourcing guide | Vendor Azure · labs |
| `../azure_certified/practice-questions/practice-exam.md` | mock-exam | dp-700 | Practice exam (verify — do not reuse questions that look fabricated) | Vendor Azure · mock_exam_sources |
| `../azure_certified/study-tracker.md` | tracker | dp-700 | Study tracker | reference only |

**Note on notebooks:** they are Databricks/Fabric-tied. The Phase 3 · 03_pyspark module must be written vendor-neutral (local Spark 3.5.x + Iceberg) — do not reuse notebook infra, only reuse transformation logic patterns.

---

## `../snowflake_eng/` — Tri-cert source (SOL-C01 · COF-C02 · DEA-C02)

| Path | Type | Topics | Description | Maps to |
|---|---|---|---|---|
| `../snowflake_eng/SnowProCoreStudyGuide.pdf` | PDF | cof-c02, exam-guide | Official SnowPro Core guide | Vendor Snowflake · COF-C02 |
| `../snowflake_eng/SnowProPlatformStudyGuide.pdf` | PDF | sol-c01, exam-guide | Platform cert guide | Vendor Snowflake · SOL-C01 |
| `../snowflake_eng/SnowProDataEngineerStudyGuide.pdf` | PDF | dea-c02, exam-guide | Data Engineer cert guide | Vendor Snowflake · DEA-C02 |
| `../snowflake_eng/STUDY_PLAN.md` | plan | snowflake, curriculum | Tri-cert study plan | Vendor Snowflake · 00_exam_profile |
| `../snowflake_eng/phase1_platform/README.md` | notes | snowflake, platform | Phase 1 overview | Vendor Snowflake · 01_architecture |
| `../snowflake_eng/phase1_platform/ENVIRONMENT_SETUP.md` | notes | snowflake, setup | Trial-account setup | Vendor Snowflake · 00_exam_profile |
| `../snowflake_eng/phase1_platform/study_notes/domain_1_0_architecture.md` | notes | snowflake, architecture, micropartitions | Domain 1 study notes | Vendor Snowflake · 01_architecture |
| `../snowflake_eng/phase1_platform/study_notes/domain_2_0_identity.md` | notes | snowflake, rbac, iam | Domain 2 identity/access | Vendor Snowflake · 03_access |
| `../snowflake_eng/phase1_platform/study_notes/domain_3_0_data_loading.md` | notes | snowflake, copy-into, snowpipe | Domain 3 loading | Vendor Snowflake · 02_loading |
| `../snowflake_eng/phase1_platform/study_notes/domain_4_0_data_protection.md` | notes | snowflake, time-travel, cloning | Domain 4 protection | Vendor Snowflake · 04_protection |
| `../snowflake_eng/phase1_platform/labs/lab_01_architecture_and_ui.sql` | sql-lab | snowflake, ui | Architecture + UI lab | Vendor Snowflake · labs |
| `../snowflake_eng/phase1_platform/labs/lab_02_data_loading.sql` | sql-lab | snowflake, copy-into | Data loading lab | Vendor Snowflake · labs |
| `../snowflake_eng/phase1_platform/labs/lab_03_warehouses.sql` | sql-lab | snowflake, warehouses | Warehouse sizing/scaling lab | Vendor Snowflake · 05_performance |
| `../snowflake_eng/phase1_platform/labs/lab_04_identity_and_access.sql` | sql-lab | snowflake, rbac | Identity + access lab | Vendor Snowflake · 03_access |
| `../snowflake_eng/phase1_platform/labs/lab_05_data_protection.sql` | sql-lab | snowflake, time-travel, failsafe | Data protection lab | Vendor Snowflake · 04_protection |

**Snowflake Phases 2-3** (COF-C02 and DEA-C02 deep content) do not yet exist in `../snowflake_eng/`. Vendor Snowflake agent (Stage 9) must write those from the PDFs + vendor docs.

---

## Content gaps — topics with NO sibling source

Modules flagged as GAP must be written from scratch, citing only primary docs/specs/canonical books per `docs/REUSE_POLICY.md`.

| Module | Fallback sources |
|---|---|
| Phase 1 · 03_python | python.org docs, PEP 518, uv docs |
| Phase 1 · 06_git | git-scm.com reference manual |
| Phase 2 · 01_data_modeling | *Kimball DW Toolkit Ch. 1-3, 5*; *Inmon Building the DW Ch. 1-3*; *Linstedt Data Vault 2.0* |
| Phase 2 · 03_distributed_systems | *Kleppmann DDIA Ch. 5, 6, 9*; Raft/Paxos papers (cited by name only) |
| Phase 2 · 06_lakehouse_bridge (DuckDB) | duckdb.org/docs |
| Phase 3 · 03_pyspark | spark.apache.org/docs/latest + iceberg.apache.org/docs/latest/spark-getting-started |
| Phase 4 · advanced-orchestration patterns | docs.dagster.io (sensors, multi-asset, retry policies) |
| Phase 5 · 05_iam_primer | localstack.cloud + AWS IAM User Guide + `../aws_certified/labs/week-10-lab-security.md` as adaptation base |

---

## How to use this index

1. **Before writing any module**, grep this file for the module's phase/number:
   `grep -n "Phase 3 · 05_dbt" references/sibling_sources.md`
2. For each row that maps to your module, Read the cited file and integrate its content.
3. Cite reused content inline: `../dataeng/dbt_project/models/marts/fct_trip_metrics.sql:L1-L42`.
4. If no rows match, the module is a **GAP** — use the Content gaps table above and `docs/REUSE_POLICY.md` fallback order.
