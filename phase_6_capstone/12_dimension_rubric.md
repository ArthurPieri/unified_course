# 12-Dimension Capstone Rubric

This is the scoring rubric for the full capstone described in [`project_brief.md`](project_brief.md). Dimensions are drawn from the required components and assessment criteria in `../UNIFIED_COURSE_PLAN.md` §Phase 6 (L537–L556) and from the operational concerns called out across Phases 4 and 5.

## How to use it

Score each of the 12 dimensions 0–3:

- **3 — Exceeds.** The capstone demonstrates this dimension at a level you could defend to a senior engineer in an interview. An operator could rely on it.
- **2 — Meets.** Present, correct, non-trivial. Would survive a code review with minor comments.
- **1 — Partial.** Started but incomplete, or present in a cosmetic form. Would not survive a code review.
- **0 — Missing.** Absent, broken, or present only as a placeholder.

**Exit bar.** To declare the capstone complete, every dimension must be ≥ 2. A single dimension at 1 is the next week's priority. A dimension at 0 means the capstone is not yet done, regardless of how well the others score.

**Self-review is allowed and encouraged.** Write the scores into `rubric_self_review.md` in your capstone repository with one-sentence evidence per score. If you cannot cite a file path or a screenshot as evidence, that dimension is not at the score you claim.

---

## 1. Ingestion correctness

Whether Bronze-layer data faithfully represents the source, in the right shape, with the right volume. Reference: `../UNIFIED_COURSE_PLAN.md` L537–L538.

| Score | What it looks like |
|---|---|
| 0 | No ingestion, or Bronze is empty, or row counts obviously disagree with source |
| 1 | One ingestion mode working (e.g., batch only); no reconciliation check |
| 2 | At least two ingestion modes (batch + append or batch + CDC); source-vs-Bronze row count check present |
| 3 | Batch + append + CDC all working; reconciliation check runs automatically and fails the pipeline on mismatch; handles late data |

## 2. Storage design — partitioning and file sizing

Whether the Iceberg tables are laid out for the actual query pattern, not defaults. Reference: Phase 3 Iceberg module, `../phase_3_core_tools/01_minio_iceberg_hms/`.

| Score | What it looks like |
|---|---|
| 0 | No partitioning; single giant file; or partition strategy makes query pattern slower |
| 1 | Partitioned by date with no thought to cardinality or file size |
| 2 | Partition columns chosen to match the most common query predicate; target file size set explicitly |
| 3 | Compaction job scheduled; partition evolution documented; query plan verified in Trino EXPLAIN before finalizing the layout |

## 3. Transformation logic and tests

Whether dbt models are correct, readable, and verified. Reference: `../UNIFIED_COURSE_PLAN.md` L541.

| Score | What it looks like |
|---|---|
| 0 | Models do not run; no tests; or tests are all `not_null` on already-non-null columns |
| 1 | Staging → marts exists; a handful of schema tests; no unit tests |
| 2 | Staging → intermediate → marts layering; contracts on marts; data tests plus at least one unit test; dbt docs generated |
| 3 | Unit tests cover non-trivial branches (NULL handling, joins, dedup); singular tests enforce business rules; snapshot for at least one SCD-2 dimension; dbt project passes `dbt build` from scratch |

## 4. Orchestration — schedules, sensors, retries

Whether Dagster drives the pipeline the way a scheduler should. Reference: `../UNIFIED_COURSE_PLAN.md` L543.

| Score | What it looks like |
|---|---|
| 0 | No orchestrator, or Dagster exists but everything runs as a single monolithic op |
| 1 | Software-defined assets declared; one schedule; no sensors; no retry policies |
| 2 | Asset graph matches the Bronze→Silver→Gold flow; schedule + at least one sensor; retry policies on network-touching assets |
| 3 | Backfill tested; partitioned assets; asset checks wired to freshness policies; manual kicks, schedules, and sensors all verified to produce identical state |

## 5. Data quality gates

Whether bad data is blocked from reaching Gold, not merely logged. Reference: `../UNIFIED_COURSE_PLAN.md` L556 and Phase 2 · 04_data_quality.

| Score | What it looks like |
|---|---|
| 0 | No quality checks, or checks exist but pipeline continues on failure |
| 1 | `dbt test` runs after build; no circuit breaker — test failures do not stop downstream |
| 2 | Quality checks are an orchestration gate: Silver does not publish if tests fail; at minimum a row-count anomaly check |
| 3 | Quality SLAs documented; anomaly detection on key metrics; quarantine path for rejected rows with a rerun procedure |

## 6. Security and PII handling

Whether unauthorized reads of sensitive data are actually blocked, not just documented. Reference: `../UNIFIED_COURSE_PLAN.md` L544.

| Score | What it looks like |
|---|---|
| 0 | No PII analysis; credentials in plaintext in the repo |
| 1 | PII columns identified in a markdown file; no enforcement |
| 2 | Masking/redaction enforced in Trino/Spark views; RBAC roles defined; secrets in a secret store or env file outside git |
| 3 | Per-column decision log; audit trail of accesses; demonstrated unauthorized-read failure against the privileged column; secret rotation procedure documented |

## 7. Observability and alerting

Whether you would know the pipeline is broken before the stakeholder does. Reference: `../UNIFIED_COURSE_PLAN.md` L545, L553.

| Score | What it looks like |
|---|---|
| 0 | No metrics; no dashboard; no alerts |
| 1 | Prometheus scraping container metrics only; Grafana dashboard with a couple of panels |
| 2 | Pipeline-health metrics (run status, freshness, rows-per-run); one alert rule on a real failure condition; alert goes somewhere real |
| 3 | Injected failure detected within 5 minutes per capstone acceptance criterion; runbook link in alert annotation; alert has been tested to actually fire and resolve |

## 8. CI/CD and deployability

Whether the project can be rebuilt from source control without tribal knowledge. Reference: `../UNIFIED_COURSE_PLAN.md` L547 and Phase 5 · 01_cicd.

| Score | What it looks like |
|---|---|
| 0 | No CI; deployment is undocumented shell history |
| 1 | CI runs lint on PRs; no dbt test in CI; deployment is `docker compose up` with no docs |
| 2 | CI runs lint + `dbt compile` + `dbt test` + at least one integration test; merges blocked on failure; deployment procedure in README |
| 3 | CI matrix covers multiple Python/dbt versions; deployment is a single command; rollback procedure documented; branch protection enforced on main |

## 9. Documentation and onboarding

Whether a stranger can run this on Monday. Reference: `../UNIFIED_COURSE_PLAN.md` L555.

| Score | What it looks like |
|---|---|
| 0 | README is a dataset description; no run instructions |
| 1 | README has `docker compose up` but misses prerequisites, bootstrap steps, or credentials |
| 2 | Stranger can clone, run, and query in under 30 minutes from README alone; architecture diagram present; dbt docs generated |
| 3 | Onboarding tested with a real stranger; README includes troubleshooting section for the most likely failures; architecture diagram matches reality |

## 10. Cost awareness

Whether the design would survive contact with a cloud bill. Reference: Phase 5 · 06_finops.

| Score | What it looks like |
|---|---|
| 0 | No consideration of file size, query scan volume, or compute footprint |
| 1 | Mentioned in README without numbers |
| 2 | File sizes and scan volumes measured; partitioning chosen to reduce scans; idle services can be scaled to zero |
| 3 | Explicit cost model (rows × bytes × query frequency) for hypothetical cloud deployment; documented trade-offs between compute and storage; at least one cost optimization with before/after numbers |

## 11. Error handling and idempotency

Whether rerunning a failed step is safe. Reference: Phase 4 advanced orchestration, `../UNIFIED_COURSE_PLAN.md` L542.

| Score | What it looks like |
|---|---|
| 0 | Reruns produce duplicates; failures leave the pipeline in a broken intermediate state |
| 1 | Some assets are idempotent by luck (e.g., dbt materialized as view); no deliberate design |
| 2 | Every asset is either idempotent or has a documented rerun procedure; dead-letter handling for ingestion; retries with backoff |
| 3 | Chaos test: kill any single container mid-run, restart, and the pipeline converges to the same final state as a clean run |

## 12. Architecture Decision Records

Whether non-obvious decisions are documented. Reference: `../UNIFIED_COURSE_PLAN.md` L548, Phase 5 · 01_cicd lab on ADRs (`../phase_5_advanced/01_cicd/`).

| Score | What it looks like |
|---|---|
| 0 | No ADRs, or ADRs are marketing copy ("we chose X because it is best") |
| 1 | One ADR exists; lists a decision without alternatives or consequences |
| 2 | At least three ADRs using a minimal template (context / decision / consequences / alternatives); each names a real trade-off accepted |
| 3 | ADRs cross-link; superseded decisions are preserved with a superseded-by link; one ADR shows a decision you reversed after measurement |

---

## Scoring worksheet

Copy this block into your capstone repo as `rubric_self_review.md`:

```
| # | Dimension | Score | Evidence (file path or screenshot) |
|---|---|---|---|
| 1 | Ingestion correctness | |
| 2 | Storage design | |
| 3 | Transformation + tests | |
| 4 | Orchestration | |
| 5 | Data quality gates | |
| 6 | Security + PII | |
| 7 | Observability + alerting | |
| 8 | CI/CD + deployability | |
| 9 | Documentation + onboarding | |
| 10 | Cost awareness | |
| 11 | Error handling + idempotency | |
| 12 | ADRs | |
```

Minimum passing score per dimension is 2. Average ≥ 2.5 is a strong capstone; average ≥ 2.0 with no zeros or ones is a complete capstone. Anything below that is a draft.
