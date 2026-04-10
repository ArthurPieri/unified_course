# Phase 1 — Build Status

Last updated: 2026-04-10

## Modules
- [x] 01_linux_bash — drafted 2026-04-10 (README + references + quiz + lab_01_bash_scripting; reused ../linux_fundamentals/course/01-linux-fundamentals.md and 02-system-administration.md; primary docs: GNU bash, coreutils, man7.org, jq, docker docs)
- [x] 02_networking — drafted 2026-04-10 (README + references + quiz; RFCs 1918/1034/1035/9293/768/9110/9112/8446, IANA port registry, Docker networking docs, sibling linux_fundamentals Part C)
- [x] 03_python — drafted (GAP — primary docs + dataeng/pyproject.toml + dataeng/tests/conftest.py)
- [x] 04_docker — drafted 2026-04-10 (README + references + quiz + lab_L1_compose_healthcheck; primary docs: docs.docker.com; reused ../dataeng/docker-compose.yml with line citations L8-L23, L26-L43, L62-L88, L91-L112, L236-L243)
- [x] 05_sql_postgres — drafted 2026-04-10 (README + references + quiz + lab_03_nyc_taxi_sql; primary docs: postgresql.org/docs/current — tutorial-window, queries-with, using-explain, indexes, sql-copy, pgstatstatements)
- [x] 06_git — drafted 2026-04-10 (GAP — README + references + quiz + lab_04_git_workflow; primary docs: git-scm.com, Pro Git, GitHub docs, pre-commit.com, dataeng CI example)

## Labs
- [x] lab_01_bash_scripting — drafted 2026-04-10
- [x] lab_L1_compose_healthcheck — drafted 2026-04-10
- [x] lab_02_python_project — drafted 2026-04-10
- [x] lab_03_nyc_taxi_sql — drafted 2026-04-10
- [x] lab_04_git_workflow — drafted 2026-04-10

## Artifacts
- [x] phase_1_foundations/README.md (phase hub)
- [x] phase_1_foundations/checkpoint_Q1.md (20-Q checkpoint)

## Decisions recorded
- Python module is GAP (no sibling source); uses PEPs 518/621 as primary for project layout
- Git module is GAP; uses git-scm.com + Pro Git (Chacon & Straub) as primary
- Docker module reuses `../dataeng/docker-compose.yml` with line-range citations
- SQL module uses Postgres 16 as universal sandbox (not MySQL — per UNIFIED_COURSE_PLAN §Tool pin)
- Networking module scope is "read curl -v + dig + ss output" — not CCNA depth

## Blockers
none

## Next action
Stage 3: Phase 2 core domain already in flight (4 parallel agents complete)
