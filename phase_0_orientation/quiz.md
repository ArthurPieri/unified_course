# Phase 0 Exit Quiz (10 questions)

Pass = 8/10. Below that, re-read the module you missed.

---

**Q1.** Name the 7 phases of the core track in order.

**Q2.** Where do vendor branches (AWS / Azure / Snowflake) appear in the curriculum, and what are their prerequisites?

**Q3.** The course policy on secondary sources (blogs, Medium, Stack Overflow) is:
A) Use sparingly, tag with `[UNVERIFIED]`
B) Accept any source a search engine returns
C) Reject — omit the claim if no primary source exists
D) Convert into primary sources by rewriting

**Q4.** The Phase 3 full-profile working-set RAM target is approximately:
A) 2 GB B) 6 GB C) 12 GB D) 32 GB

**Q5.** The Phase 3 light profile drops which two services compared to full?

**Q6.** On macOS, `check.sh` reads physical RAM via:
A) `/proc/meminfo` B) `sysctl hw.memsize` C) `wmic` D) `free -m`

**Q7.** Docker Compose v1 (`docker-compose`) vs. v2 (`docker compose`): this course uses:
A) v1 B) v2 C) Either D) Neither

**Q8.** Your machine has 6 GB RAM. Which path is correct?
A) Run full profile anyway
B) Run light profile locally
C) Run light profile in cloud fallback
D) Upgrade hardware before Phase 1

**Q9.** The central glossary, docs index, and content provenance record all live under:
A) `docs/` B) `references/` C) `status/` D) `phase_0_orientation/`

**Q10.** Before Phase 3, a learner must have completed:
A) Only Phase 0
B) Phases 0–2
C) Phases 0–5
D) A vendor branch

---

## Answers

1. Phase 0 Orientation → Phase 1 Foundations → Phase 2 Core Domain → Phase 3 Core Tools → Phase 4 Specializations → Phase 5 Advanced → Phase 6 Capstone. Ref: [../README.md](README.md), [../UNIFIED_COURSE_PLAN.md](../UNIFIED_COURSE_PLAN.md)
2. After Phase 5 (Phase 6 capstone recommended OR fast-track rubric met). Ref: [01_course_structure](01_course_structure/README.md) §Vendor branches
3. C. Ref: [../docs/REUSE_POLICY.md](../docs/REUSE_POLICY.md)
4. C — ~12 GB working set (plus Docker/OS overhead). Ref: [03_hardware_check](03_hardware_check/README.md)
5. HMS (Hive Metastore) and Spark. Ref: [01_course_structure](01_course_structure/README.md) §Full vs. light Phase 3 profile
6. B. Ref: [03_hardware_check/check.sh](03_hardware_check/check.sh)
7. B — Compose v2, invoked as `docker compose` (space). Ref: [Docker Compose migrate guide](https://docs.docker.com/compose/migrate/)
8. C — 6 GB is below the 8 GB threshold; machines with <8 GB RAM should use cloud fallback (Codespaces or Gitpod). Ref: [03_hardware_check](03_hardware_check/README.md) — "8 GB machines run light only; <8 GB use cloud fallback"
9. B. Ref: [../README.md](../README.md)
10. B — Phase 3 only requires Phases 0–2 complete. Phases 4–5 build on Phase 3. Vendor branches need Phases 0–5. Ref: [../UNIFIED_COURSE_PLAN.md](../UNIFIED_COURSE_PLAN.md) §Phase prerequisites
