# Vendor Branch: Snowflake (Tri-Cert)

Tri-certification path: **SOL-C01 -> COF-C02 -> DEA-C02**. Estimated 150-200 hours total, 15-22 weeks at 10-12 h/week. See `../../UNIFIED_COURSE_PLAN.md` Stage 9c.

## Which cert maps to which module

| Module | SOL-C01 (Platform) | COF-C02 (Core) | DEA-C02 (Data Engineer) |
|---|---|---|---|
| `00_exam_profile/` | all three exams side-by-side | | |
| `01_architecture/` | Domain 1.0 (35%) | Domain 1.0 (24%) | background |
| `02_loading/` | Domain 3.0 (40%) | Domain 4.0 (12%) | Domain 1.0 (28%) |
| `03_access/` | Domain 2.0 (15%) | Domain 2.0 (18%) | Domain 4.0 (14%) |
| `04_protection/` | Domain 4.0 (10%) | Domain 6.0 (12%) | Domain 3.0 (14%) |
| `05_performance/` | Domain 3.0 (warehouses) | Domain 3.0 (16%) | Domain 2.0 (19%) |
| `06_dea_advanced/` | — | Domain 5.0 intro | Domains 1.0, 5.0 (25%) |

Source for weights: *SnowPro Associate: Platform Study Guide, June 9 2025, p. 4*; *SnowPro Core Study Guide, August 22 2025, p. 5*; *SnowPro Advanced: Data Engineer Study Guide, March 6 2026, p. 4*.

## Tri-cert paths

### Path 1 — SOL-C01 only (platform fluency)
- **Audience:** analysts, BI developers, curious engineers wanting a résumé credential; people evaluating Snowflake.
- **Time:** ~45-60 h (study plan) including 5 h environment setup and 5 h practice. Rounds to **~50 h** for planning.
- **Scope:** modules `01_architecture`, `02_loading`, `03_access`, `04_protection`, plus warehouse sizing/Cortex from `05_performance`. Skip `06_dea_advanced`.
- **Cost:** $175 exam + ~$0-50 trial credits overrun buffer.
- **Source:** [Snowflake certification guide](https://www.snowflake.com/certifications/).

### Path 2 — SOL-C01 + COF-C02 (platform + core)
- **Audience:** Snowflake admins, data platform engineers, ELT developers who will operate Snowflake daily.
- **Time:** ~115-150 h. Study plan says Platform 45-60 h + Core 70-90 h minus 2-3 h bridge overlap; rounds to **~100-120 h** planning total (the "85% overlap with Path 1" figure in this branch refers only to the Platform portion that carries forward, not the overall hours).
- **Scope:** all six modules except `06_dea_advanced` optional sections (streams, tasks, semi-structured are required for Core; Snowpark, Dynamic Tables, Iceberg are DEA-only).
- **Cost:** $350 exams + ~$50 official Core practice exam + trial buffer.
- **Source:** [Snowflake certification guide](https://www.snowflake.com/certifications/).

### Path 3 — Full tri-cert (SOL + COF + DEA)
- **Audience:** data engineers pursuing the highest Snowflake credential; consultants; staff engineers.
- **Time:** **150-200 h** over 15-22 weeks. 45-60 h Platform + 70-90 h Core + 100-130 h DEA, minus bridge overlap (3 h P1->P2, 5 h P2->P3). Matches `UNIFIED_COURSE_PLAN.md:L954`.
- **Scope:** all six modules in full, including `06_dea_advanced` (streams, tasks, Dynamic Tables, Snowpark, UDFs, external functions, Iceberg).
- **Cost:** $725 exam subtotal ($175 + $175 + $375) + ~$100 in official practice exams + trial buffer. See the [Snowflake certification guide](https://www.snowflake.com/certifications/) for current pricing.
- **Overlap estimate:** Core provides ~50-75% of DEA foundations depending on domain. Phase 1 covers ~85% of Core Domain 1 and ~80% of Core Domain 2.

### Which path for whom

| If you are... | Pick |
|---|---|
| Time-boxed to one month, just need a Snowflake line on the résumé | Path 1 (SOL-C01) |
| Owning Snowflake ops for a team and not doing pipelines in Snowpark | Path 2 |
| A data engineer and Snowflake is your primary platform | Path 3 |
| Already have Core? | Jump straight to `06_dea_advanced` and use modules 02/04/05 as refreshers |

## Reading order

1. This README
2. `00_exam_profile/README.md` — schedule the right exam first
3. `01_architecture/` -> `02_loading/` -> `03_access/` -> `04_protection/` -> `05_performance/` (Platform + Core path)
4. `06_dea_advanced/` (DEA only)
5. `mock_exam_sources.md` before each exam

## Reuse disclosure

Modules `01_architecture`, `02_loading`, `03_access`, `04_protection` reference the official [Snowflake documentation](https://docs.snowflake.com/) and [Snowflake Quickstarts](https://quickstarts.snowflake.com/) for study notes and hands-on labs. Modules `05_performance` and `06_dea_advanced` cite the official PDF study guides and docs.snowflake.com as primary sources. See `./references.md`.

## References

See [references.md](./references.md).
