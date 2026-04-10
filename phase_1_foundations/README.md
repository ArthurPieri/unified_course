% 

# Phase 1 — Foundations (60h)

Operating-level fluency with the six tools every data engineer uses daily: Linux, networking, Python, Docker, SQL/PostgreSQL, Git. Nothing here is theoretical — each module ends in a lab you run on your own machine.

## Prerequisites
- [Phase 0 complete](../phase_0_orientation/) — hardware check passed, profile chosen (full or light).

## Module order

| # | Module | Hours | Type |
|---|---|---|---|
| 01 | [Linux & Bash Scripting](01_linux_bash/) | 16 | reuse — `../linux_fundamentals/` |
| 02 | [Networking Fundamentals](02_networking/) | 6 | reuse — `../linux_fundamentals/` Part C |
| 03 | [Python Engineering for Data](03_python/) | 12 | **GAP** — primary docs + PEPs |
| 04 | [Docker & Compose for Data](04_docker/) | 12 | reuse — `../dataeng/docker-compose.yml` + Docker docs |
| 05 | [SQL Depth with PostgreSQL](05_sql_postgres/) | 10 | primary — postgresql.org/docs |
| 06 | [Git Workflows for Data Teams](06_git/) | 4 | **GAP** — git-scm.com, Pro Git |

Total: 60h. Each module has README → labs → quiz.

## Labs in this phase
| Lab | Module | Goal |
|---|---|---|
| lab_01_bash_scripting | 01 | Defensive healthcheck.sh over a Compose stack |
| lab_L1_compose_healthcheck | 04 | Postgres + app in Compose, healthcheck + service_healthy gating |
| lab_02_python_project | 03 | Scaffold `src/` project, ruff + mypy + pytest + pre-commit |
| lab_03_nyc_taxi_sql | 05 | Load NYC taxi into Postgres, window functions, EXPLAIN ANALYZE |
| lab_04_git_workflow | 06 | Trunk-based flow with rebase, pre-commit, force-with-lease |

## Exit criteria — Checkpoint Q1
Before leaving Phase 1, you should be able to:
- [ ] Read `ls -l`, `ps`, `ss`, `dig`, `curl -v` output and form a hypothesis
- [ ] Write a defensive bash script (`set -euo pipefail`) that chains commands safely
- [ ] Scaffold a Python project with `pyproject.toml`, run `ruff`, `mypy`, `pytest`
- [ ] Write a Dockerfile and a multi-service Compose file with healthchecks
- [ ] Write a window function query and read a PostgreSQL query plan
- [ ] Resolve a rebase conflict and use `push --force-with-lease`

Take [checkpoint_Q1.md](checkpoint_Q1.md) — 20 questions, pass = 16/20.

## References
Each module has its own `references.md` citing primary sources. The phase-wide index is [references/docs.md](../references/docs.md) and [references/sibling_sources.md](../references/sibling_sources.md).

## Next
[Phase 2 — Core Domain](../phase_2_core_domain/) (data modeling, ETL/ELT, distributed systems, quality, streaming, lakehouse bridge).
