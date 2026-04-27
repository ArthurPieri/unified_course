# Phase 4 — Build Status

Last updated: 2026-04-10

## Modules
- [x] 01_cdc_debezium — drafted 2026-04-10 (Debezium architecture, Postgres logical replication, Iceberg MERGE INTO sink)
- [x] 02_kafka_hands_on — drafted 2026-04-10 (topics/ISR, producer idempotence, consumer groups, delivery semantics, KRaft)
- [x] 03_semi_structured — drafted 2026-04-10 (Parquet Dremel levels, Iceberg schema evolution via field IDs, Avro resolution)
- [x] 04_security_governance — drafted 2026-04-10 (4-layer stack, mask/hash/token/encrypt, Trino rules.json, RBAC vs ABAC, GDPR tombstoning)
- [x] 05_performance_tuning — drafted 2026-04-10 (Trino EXPLAIN ANALYZE, Spark AQE, broadcast joins, Iceberg compaction + expire_snapshots)
- [x] 06_observability — drafted 2026-04-10 (OTel three pillars, Prometheus pull model, RED/USE, Dagster freshness, SRE Ch. 6)

## Labs
- [x] lab_L4a_cdc_pipeline — Postgres→Debezium→Kafka→Trino MERGE INTO Iceberg with time-travel verification
- [x] lab_L4b_pii_masking — Trino file-based access control with column masks, row filters, three principals
- [x] lab_L4c_perf_tuning — generate 10k tiny files, compact via optimize, re-time, expire snapshots (+ generate_data.py)
- [x] lab_L4d_kafka_windowed — KRaft compose, kafka-python producer with acks=all, tumbling-window consumer

## Artifacts
- [x] phase_4_specializations/README.md (phase hub)
- [x] phase_4_specializations/checkpoint_Q4.md (20-Q checkpoint)

## Decisions recorded
- Streaming is specialization depth, not core — labs are "literacy grade" scope per UNIFIED_COURSE_PLAN §batch-first default
- Performance tuning lab uses a synthetic `generate_data.py` (PEP 723 inline deps, pyarrow + MinIO via endpoint_override) to satisfy V2 Finding #4
- Security module references AWS IAM official docs
- Observability uses self-contained Prometheus/Grafana configs (moved out of Phase 3 compose)

## Blockers
none

## Next action
Stage 7 — Phase 5 (complete, pending commit)
