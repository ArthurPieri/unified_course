# Phase 4 — Specializations (60–75h)

Depth passes on six topics that make the difference between "the pipeline runs" and "the pipeline runs in production, under load, without leaking data": CDC, Kafka, semi-structured evolution, security/governance, performance tuning, and observability.

## Prerequisites
- [Phase 3 complete](../phase_3_core_tools/) — full lakehouse stack up, dbt + Dagster + Trino + Spark + Iceberg fluency.

## Module order

| # | Module | Hours | Lab |
|---|---|---|---|
| 01 | [CDC with Debezium](01_cdc_debezium/) | 8 | [L4a CDC pipeline](01_cdc_debezium/labs/lab_L4a_cdc_pipeline/) |
| 02 | [Kafka Hands-on](02_kafka_hands_on/) | 8 | [L4d Kafka windowed](02_kafka_hands_on/labs/lab_L4d_kafka_windowed/) |
| 03 | [Semi-structured & Schema Evolution](03_semi_structured/) | 6 | — |
| 04 | [Security & Governance](04_security_governance/) | 8 | [L4b PII masking](04_security_governance/labs/lab_L4b_pii_masking/) |
| 05 | [Performance Tuning](05_performance_tuning/) | 10 | [L4c perf tuning](05_performance_tuning/labs/lab_L4c_perf_tuning/) |
| 06 | [Observability](06_observability/) | 6 | — |

Module hours: 46h. With realistic buffer for CDC debugging, Kafka cluster setup, and performance lab iteration: **60–75h** (5–7 weeks at 10–12h/week).

## Exit criteria — Checkpoint Q4
Before leaving Phase 4, you should be able to:
- [ ] Configure a Debezium Postgres source connector with `wal_level=logical`, tail a topic, and `MERGE INTO` an Iceberg target
- [ ] Pick Kafka delivery semantics (at-most/at-least/exactly-once) per use case and defend the trade-off
- [ ] Evolve a Parquet/Iceberg schema safely (add, drop, rename via field ID, type promotion) and know which changes are unsafe
- [ ] Apply Trino file-based access control with column masks and row filters; justify RBAC vs ABAC
- [ ] Diagnose a slow Trino query from `EXPLAIN ANALYZE`, compact tiny files with `ALTER TABLE EXECUTE optimize`, and expire old Iceberg snapshots
- [ ] Wire Prometheus + Grafana, distinguish symptoms from causes, and attach a Dagster freshness check

Take [checkpoint_Q4.md](checkpoint_Q4.md) — 20 questions, pass = 16/20.

## References
See per-module `references.md`. The phase draws heavily on *DDIA* Ch. 11, Debezium architecture docs, Kafka design docs, Apache Iceberg spec, Trino file-based access control, Spark AQE docs, and the Google SRE Book Ch. 6.

## Next
[Phase 5 — Advanced](../phase_5_advanced/) (CI/CD, Kubernetes, Airflow bridge, cloud concepts, IAM, FinOps, data serving).
