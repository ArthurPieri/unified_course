# Unified Data Engineering Course

A vendor-agnostic open-source data engineering curriculum with three optional vendor specialization branches (AWS DEA-C01, Azure DP-700, Snowflake SOL/COF/DEA).

## Outcome

Completing the core (Phases 0–6) plus one vendor branch prepares a learner to enter the job market as a **strong junior to early mid-level data engineer** with hands-on tool proficiency and one industry certification.

See `UNIFIED_COURSE_PLAN.md` for the full syllabus and `IMPLEMENTATION_PLAN.md` for historical context.

## Phase order

| Phase | Topic | Hours | Path |
|---|---|---|---|
| 0 | Orientation + self-assessment | 5–8 | [phase_0_orientation/](phase_0_orientation/) |
| 1 | Foundations (Linux, Python, Docker, SQL, Git) | 60–75 | [phase_1_foundations/](phase_1_foundations/) |
| 2 | Core domain concepts + lakehouse bridge | 50–65 | [phase_2_core_domain/](phase_2_core_domain/) |
| 3 | Core tools (MinIO, Iceberg, Trino, Spark, dbt, Dagster) | 100–140 | [phase_3_core_tools/](phase_3_core_tools/) |
| 4 | Specializations (CDC, Kafka, security, perf, observability) | 60–75 | [phase_4_specializations/](phase_4_specializations/) |
| 5 | Advanced (CI/CD, K8s, Airflow, IAM, FinOps) | 50–65 | [phase_5_advanced/](phase_5_advanced/) |
| 6 | Capstone (optional; fast-track available) | 50–70 | [phase_6_capstone/](phase_6_capstone/) |

## Vendor branches (pick one)

- [vendors/aws/](vendors/aws/) — AWS DEA-C01 (100–130h)
- [vendors/azure/](vendors/azure/) — Azure DP-700 (110–140h)
- [vendors/snowflake/](vendors/snowflake/) — SOL-C01 → COF-C02 → DEA-C02 (150–200h)

## How to use

1. Start with `phase_0_orientation/` — self-assessment + hardware check.
2. Follow phases in order. Each phase has a `README.md` hub with module order.
3. Each module has `labs/` subfolders with hands-on exercises.
4. Check your progress in `status/phase_N.md` or the root `STATUS.md`.
5. Every non-obvious claim cites a primary source — see [docs/REUSE_POLICY.md](docs/REUSE_POLICY.md).

## Central references

- [references/books.md](references/books.md) — canonical books
- [references/docs.md](references/docs.md) — official tool/spec docs
- [references/tools.md](references/tools.md) — tool versions used
- [references/glossary.md](references/glossary.md) — terms
- [references/sibling_sources.md](references/sibling_sources.md) — reused content from sibling dirs
