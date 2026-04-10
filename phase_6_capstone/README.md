# Phase 6 — Vendor-Agnostic Capstone (50–70h)

Phase 6 is the integration phase. Phases 0–5 taught the parts; Phase 6 forces you to put them together on a single end-to-end project and defend the result. It is the last open-source checkpoint before the vendor branches (AWS, Azure, Snowflake) and the deliverable a hiring manager will actually look at.

This phase is **strongly recommended**, but the curriculum plan offers a **fast-track self-diagnostic** for learners who already have equivalent integration work from Phase 3–5 and want to enter a vendor branch immediately. Both paths are described below. The choice is yours, but the gate between them is concrete — not self-declared.

Source of truth for everything on this page: `../UNIFIED_COURSE_PLAN.md` §Phase 6 (L523–L572) and the adversarial review in `../UNIFIED_COURSE_PLAN_adversarial_analysis_v2.md` §Finding #3 (L97–L118).

## Two paths

| Path | When to take it | Deliverable | Time budget |
|---|---|---|---|
| **Full capstone** | You want a portfolio artifact, or your Phase 3–5 work is fragmented | End-to-end lakehouse on a realistic dataset, scored on the 12-dimension rubric | 50–70h over 4–6 weeks |
| **Fast-track** | You already have most of the capstone scattered across Phase 3–5 labs and only need to prove integration competence | 6 concrete self-diagnostic deliverables, each < 4h | ~20–24h total |

The full capstone is the recommended path (`../UNIFIED_COURSE_PLAN.md` L926). The fast-track exists because the v1 rubric was "cosmetic without a verification mechanism" (adversarial v2, L97–L103); this phase replaces the cosmetic checkboxes with six specific, verifiable artifacts drawn from adversarial v2 Option A (L116).

## Documents in this phase

| File | Purpose |
|---|---|
| [`project_brief.md`](project_brief.md) | Full capstone specification: dataset choice, required components, acceptance criteria |
| [`reference_architecture.md`](reference_architecture.md) | ASCII topology, component map, data flow narrative — the skeleton you fill in |
| [`12_dimension_rubric.md`](12_dimension_rubric.md) | 12-dimension grading rubric scored 0–3. Used for capstone self-review and for anyone reviewing your code |
| [`fast_track_rubric.md`](fast_track_rubric.md) | 6-deliverable alternative. Each has a concrete "what good looks like" and a self-check |
| [`references.md`](references.md) | Citation list for this phase |

There is no lab directory and no quiz. The entire phase is one deliverable (full capstone) or six small deliverables (fast-track). Assessment is the rubric, not a multiple-choice check.

## Exit criteria

You may leave Phase 6 (and enter a vendor branch — `../UNIFIED_COURSE_PLAN.md` L577) when **one** of the following is true:

1. **Full capstone path.** The capstone project is complete, pushed to a public Git repository, documented, and scores ≥ 2 on every dimension of [`12_dimension_rubric.md`](12_dimension_rubric.md). "Complete" means: `docker compose up` (or the equivalent Kubernetes manifest) brings the stack to green from a fresh clone; Dagster runs the full DAG end-to-end without manual steps; dbt tests are 100% passing; an injected failure is detected by the monitoring stack within 5 minutes; PII masking blocks an unauthorized read; and a stranger can onboard from the README alone. These are from `../UNIFIED_COURSE_PLAN.md` L550–L556.
2. **Fast-track path.** All six deliverables in [`fast_track_rubric.md`](fast_track_rubric.md) exist in a public repository, each has a self-check that passes, and you can demo any one of them in under 10 minutes without touching the code.

The rubric is the gate. Self-review is allowed. The plan explicitly warns that "weak learners skip the capstone believing they qualify when they don't, then fail vendor branch content because they never integrated skills" (adversarial v2, L107). If the rubric is uncomfortable to face, that is the signal to take the full capstone.

## Prerequisites

Phase 5 exit criteria met (`../UNIFIED_COURSE_PLAN.md` L527). Specifically, you should have working familiarity with:

- Phase 3 stack: MinIO + Iceberg + Hive Metastore, Trino, PySpark, dlt, dbt, Dagster, Metabase (`../phase_3_core_tools/`)
- Phase 4: Kafka/Debezium CDC, performance tuning, security + PII, observability
- Phase 5: CI/CD, Kubernetes basics, cloud concepts, IAM primer, cost/FinOps

The capstone does **not** introduce new tools. Every component is something you already touched. The skill being assessed is integration, documentation, and operational hardening — not tool discovery.

## How to use this phase

**If you choose the full capstone:**
1. Read [`project_brief.md`](project_brief.md) and pick one of the three datasets.
2. Read [`reference_architecture.md`](reference_architecture.md) and sketch your own version on paper. If yours differs, write an ADR explaining why.
3. Copy the Phase 3 compose stack (`../phase_3_core_tools/compose/full-stack/docker-compose.yml`) as your starting point. Do not start from an empty directory.
4. Work in weekly slices against the 12-dimension rubric. Score yourself honestly at the end of each week. Any dimension still at 0 or 1 is next week's priority.
5. Before declaring done, run the acceptance tests in `project_brief.md` from a fresh clone.

**If you choose the fast-track:**
1. Read [`fast_track_rubric.md`](fast_track_rubric.md) and verify that each deliverable maps to work you have already started.
2. For any deliverable you cannot produce in < 4 hours, that is your signal — the gap is real. Switch paths.
3. Produce each deliverable in a single repository with a top-level `fast_track/` directory and one subdirectory per deliverable.
4. Write a 1-paragraph self-review against each deliverable's "how to self-check."

## Tone note

Phase 6 is unglamorous. The interesting decisions were made in Phases 2–5. Phase 6 is wiring, monitoring, documentation, and the kind of operational work that separates someone who has done a tutorial from someone who has shipped a system. The measure of success is not how clever the architecture is — it is whether the next engineer can pick it up on Monday.

## Reference

- Capstone spec source: [`../UNIFIED_COURSE_PLAN.md`](../UNIFIED_COURSE_PLAN.md) L523–L572
- Fast-track rationale: [`../UNIFIED_COURSE_PLAN_adversarial_analysis_v2.md`](../UNIFIED_COURSE_PLAN_adversarial_analysis_v2.md) L97–L118
- Phase 3 compose stack (reference implementation base): [`../phase_3_core_tools/compose/full-stack/`](../phase_3_core_tools/compose/full-stack/)
- Reuse policy (citation rules for any new writing in this phase): [`../docs/REUSE_POLICY.md`](../docs/REUSE_POLICY.md)
- Glossary: [`../references/glossary.md`](../references/glossary.md)
