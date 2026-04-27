# Module 01: Course Structure (1h)

## Learning goals
- Describe the 7-phase core track and when vendor branches come in
- Locate any topic in under 30 seconds using the directory map
- Explain the reuse-first + cite-everything policy
- Choose between the "full" and "light" Phase 3 stack profiles

## Prerequisites
- None

## Reading order
1. This README
2. [../../docs/REUSE_POLICY.md](../../docs/REUSE_POLICY.md)
3. [../../README.md](../../README.md)

## Concepts

### Core track (vendor-neutral)
Seven phases, ~700–900h total depending on pace:
- **Phase 0** — orientation (you are here)
- **Phase 1** — Linux, networking, Python, Docker, SQL, Git
- **Phase 2** — data modeling, ETL/ELT, distributed systems, quality, streaming concepts, lakehouse bridge
- **Phase 3** — full open-source lakehouse stack: MinIO + Iceberg + HMS + Trino + Spark + dlt + dbt + Dagster + Metabase
- **Phase 4** — specializations: CDC, Kafka, semi-structured, governance, performance tuning, observability
- **Phase 5** — advanced: CI/CD, Kubernetes basics, Airflow bridge, cloud concepts, IAM primer, FinOps, data serving
- **Phase 6** — capstone project + fast-track rubric

Full phase/hours breakdown: [../../UNIFIED_COURSE_PLAN.md](../../UNIFIED_COURSE_PLAN.md).

### Vendor branches
Three parallel, independent tracks taken **after** Phase 5 (Phase 6 capstone recommended, fast-track rubric acceptable):
- **AWS** — DEA-C01 (100–130h)
- **Azure** — DP-700 (110–140h)
- **Snowflake** — SOL-C01 → COF-C02 → DEA-C02 tri-cert (150–200h)

Pick one first. The core track is the prerequisite that makes any vendor branch tractable.

### Directory conventions
- `phase_N_*/NN_<name>/README.md` — module index (hub)
- `phase_N_*/NN_<name>/labs/lab_NN_*/` — labs live beside the module
- `phase_N_*/NN_<name>/quiz.md` — exit quiz (answers at bottom)
- `phase_N_*/NN_<name>/references.md` — links into the central `references/` index
- `references/` — single source of truth for docs, books, tools, glossary, content provenance
- `status/phase_N.md` — build state (so work can resume after interruptions)

### Reuse-first + cite-everything
Every module is either (a) built by adapting content from the original source curricula (see `references/sibling_sources.md` for provenance) and citing the source, or (b) a gap module written from scratch citing official documentation, specs, and canonical books only.

**Rejected sources:** blog posts, Medium, Stack Overflow, AI-generated secondary content. When the primary source is unavailable, the claim is omitted — not tagged `[UNVERIFIED]`.

Full policy: [../../docs/REUSE_POLICY.md](../../docs/REUSE_POLICY.md).

### Full vs. light Phase 3 profile
The Phase 3 stack runs locally in Docker Compose. It has two profiles:
- **Full** (~12GB RAM working set) — MinIO + HMS + Trino + Spark + dbt + Dagster + Metabase
- **Light** (~6GB RAM) — drops HMS, uses Iceberg JDBC catalog; drops Spark, uses Trino for all compute; keeps dbt + Dagster + Metabase

If `03_hardware_check` says your machine is <12GB usable after Docker overhead, use the light profile from Phase 3 onward. If <8GB, use the cloud fallback in `04_cloud_fallback`.

## Common failures
| Symptom | Cause | Fix |
|---|---|---|
| Can't find a topic | Not scanning the `references/` index first | `grep -n "<topic>" unified_course/references/*.md` |
| Phase 3 stack won't start | Using the full profile on 8GB RAM | Switch to light profile — [../../phase_3_core_tools/compose/light-profile/](../../phase_3_core_tools/compose/light-profile/) |
| Claim with no citation | Upstream doc was paywalled or secondary | Omit the claim — never write `[UNVERIFIED]` or fabricate |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on:
- [ ] I can name all 7 phases and one topic in each
- [ ] I know where module READMEs, labs, and the central references live
- [ ] I have picked full or light profile for Phase 3
- [ ] I have read `docs/REUSE_POLICY.md` and understand the "omit over guess" rule
