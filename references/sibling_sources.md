# Content Provenance and Attribution

This document records the source material that was adapted during construction of this course. The repo is now **self-contained** — all content lives within `unified_course/`. No external sibling repositories are required at build time or study time.

Originally written: 2026-04-10 | Converted to provenance record: 2026-04-27

---

## Source repositories

The following repositories provided source material that was adapted, restructured, and integrated into this unified curriculum. Content was lifted, edited for consistency, and cited inline where applicable.

### LFCA curriculum
Six markdown modules covering Linux fundamentals, system administration, cloud computing basics, security fundamentals, DevOps basics, and project management. Provided foundational material for Phase 1 (Linux/bash) and contributed to Phase 4 (security governance) and Phase 5 (CI/CD, cloud concepts).

### Open-source lakehouse stack
A working lakehouse stack including Docker Compose configurations, dbt project (models, tests, snapshots, macros), Dagster orchestration (assets, resources, schedules, sensors), dlt pipelines, Prometheus/Grafana configs, Kubernetes (Kind) configs, and test suites. Primary source for Phase 3 (core tools), Phase 4 (observability), and Phase 5 (Kubernetes, CI/CD).

### AWS DEA-C01 study plan
Twelve-week study plan with weekly notes covering ingestion, streaming, transformation, orchestration, data stores, cataloging, lifecycle, automation, monitoring, security, and cross-domain integration. Includes 11 hands-on labs and two mock exam sets. Source for the Vendor AWS branch.

### Azure DP-700 curriculum
Implementation plan for DP-700 (Fabric Data Engineer Associate) with flashcards, PySpark/Delta Lake notebooks, Fabric pipeline labs, security/monitoring labs, T-SQL and KQL exercises, and practice exam material. Source for the Vendor Azure branch.

### Snowflake tri-cert (SOL-C01, COF-C02, DEA-C02)
Phase 1 platform content including architecture, identity/access, data loading, data protection study notes and SQL labs. Exam guide PDFs for all three certifications. Study plan covering the progressive certification path. Source for the Vendor Snowflake branch.

---

## Content gaps filled from primary sources

Some modules had no corresponding source material in the original repositories and were written from scratch using official documentation and canonical books:

| Module | Primary sources used |
|---|---|
| Phase 1 · 03_python | python.org docs, PEP 518, uv docs |
| Phase 1 · 06_git | git-scm.com reference manual |
| Phase 2 · 01_data_modeling | *Kimball DW Toolkit Ch. 1-3, 5*; *Inmon Building the DW Ch. 1-3*; *Linstedt Data Vault 2.0* |
| Phase 2 · 03_distributed_systems | *Kleppmann DDIA Ch. 5, 6, 9*; Raft/Paxos papers |
| Phase 2 · 06_lakehouse_bridge (DuckDB) | duckdb.org/docs |
| Phase 3 · 03_pyspark | spark.apache.org/docs/latest + iceberg.apache.org/docs/latest/spark-getting-started |
| Phase 4 · advanced-orchestration | docs.dagster.io (sensors, multi-asset, retry policies) |
| Phase 5 · 05_iam_primer | localstack.cloud + AWS IAM User Guide |

---

## Citation policy

For current citation rules, see [../docs/REUSE_POLICY.md](../docs/REUSE_POLICY.md). All content within this repo cites its sources inline — either official documentation, canonical books, or vendor certification materials.
