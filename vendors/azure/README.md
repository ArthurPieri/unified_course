# Vendor Azure — DP-700 Branch Hub

> Target certification: **Microsoft Certified: Fabric Data Engineer Associate (DP-700)**.
> Estimated duration: **110–140 hours** (10–13 weeks at 10–12 h/week). See `../../UNIFIED_COURSE_PLAN.md` Branch B.
> Prerequisite: unified-course Phases 0–5 complete (or fast-track rubric met), plus a working understanding of Spark, Delta Lake, SQL, and medallion architecture from Phase 3.

DP-700 ("Implementing Data Engineering Solutions Using Microsoft Fabric") replaced the retired DP-203. Fabric is Microsoft's SaaS data platform that re-packages OneLake (ADLS Gen2 under the hood), Fabric Data Factory (ADF), Fabric Warehouse, Spark notebooks, and Real-Time Intelligence (Eventstreams + KQL) under a single capacity model. This branch teaches the exam-testable services directly and backfills the legacy Azure stack (Synapse, Databricks, ADF, Event Hubs, Stream Analytics, Purview) because DP-700 still expects candidates to recognize and migrate from them.

## Branch taxonomy

| # | Module | Domain coverage | Path |
|---|---|---|---|
| 00 | Exam profile & study plan | All | [00_exam_profile/](00_exam_profile/) |
| 01 | Storage — ADLS Gen2, OneLake, Fabric lakehouse | Ingest/Store | [01_storage_adls_fabric/](01_storage_adls_fabric/) |
| 02 | Ingestion — ADF, Synapse Pipelines, Fabric Data Factory, Dataflow Gen2 | Ingest/Transform | [02_ingestion_adf_fabric_pipelines/](02_ingestion_adf_fabric_pipelines/) |
| 03 | Compute — Synapse, Databricks, Fabric warehouse/lakehouse, T-SQL, KQL | Transform/Serve | [03_compute_synapse_databricks_fabric/](03_compute_synapse_databricks_fabric/) |
| 04 | Streaming — Event Hubs, Stream Analytics, Fabric Real-Time Intelligence | Ingest/Transform | [04_streaming_eventhubs_stream_analytics/](04_streaming_eventhubs_stream_analytics/) |
| 05 | Security — Entra ID, RBAC, ACLs, Purview, Managed Identity | Secure | [05_security_rbac_purview/](05_security_rbac_purview/) |
| 06 | Monitoring & optimization — Azure Monitor, Log Analytics, Fabric monitoring hub | Monitor/Optimize | [06_monitoring_optimization/](06_monitoring_optimization/) |

## Reading order

1. `00_exam_profile/README.md` — confirm domains, weighting, booking, prereqs
2. `01_storage_adls_fabric/` → `02_ingestion_adf_fabric_pipelines/` → `03_compute_synapse_databricks_fabric/`
3. `04_streaming_eventhubs_stream_analytics/` (depends on 01 storage + 03 compute)
4. `05_security_rbac_purview/` (needs familiarity with 01–03 services)
5. `06_monitoring_optimization/` (cross-cutting; study after you can build something to monitor)
6. `mock_exam_sources.md` — official practice assessment links only

Each module README is 600–1500 words (per `../../docs/REUSE_POLICY.md`) with learning goals, primary-source Microsoft Learn links, sibling-file citations with line ranges, 2–4 labs, gotchas, service comparisons, `references.md`, and an 8–10 question `quiz.md`.

## Citation policy (recap)

- **Microsoft Learn** (`learn.microsoft.com/en-us/fabric/`, `/azure/data-factory/`, `/azure/synapse-analytics/`, `/azure/databricks/`, `/azure/event-hubs/`, `/azure/stream-analytics/`, `/purview/`) — canonical.
- **Official DP-700 study guide** — domain scoping.
- **Microsoft Learn** — supplementary labs and concept references (see per-module `references.md` files).
- No blogs, no Medium, no Stack Overflow. Per `../../docs/REUSE_POLICY.md`.

## Cross-branch anchors

- Spark, Delta Lake, medallion, dbt/Dagster fundamentals: `../../phase_3_core_tools/` (vendor-neutral).
- AWS service analogs: `../aws/` (S3↔ADLS, Glue↔ADF, Kinesis↔Event Hubs, Athena↔Synapse serverless, EMR↔Databricks).
- Snowflake analogs: `../snowflake/` (Snowpipe↔Eventstream ingest, warehouses↔Fabric capacities).

## Lab environment

DP-700 labs use the **Microsoft Fabric free trial** (60-day, no credit card) for OneLake/Fabric-native exercises and the **Azure free tier** for ADF/Event Hubs/Stream Analytics where Fabric equivalents do not yet cover the exam depth. Supplementary hands-on exercises are available via [Microsoft Learn DP-700 training path](https://learn.microsoft.com/en-us/training/courses/dp-700t00) and the per-module lab links.

## Branch references

See [references.md](./references.md) for the aggregated primary-source index.
