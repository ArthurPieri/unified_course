# Phase 0 — Build Status

Last updated: 2026-04-10

## Modules
- [x] 01_course_structure — drafted 2026-04-10
- [x] 02_self_assessment — drafted 2026-04-10 (20-Q quiz with answer key)
- [x] 03_hardware_check — drafted 2026-04-10 (includes `check.sh` hardware probe)
- [x] 04_cloud_fallback — drafted 2026-04-10

## Labs
(none — Phase 0 is orientation)

## Artifacts
- [x] phase_0_orientation/README.md (phase hub)
- [x] phase_0_orientation/quiz.md (10-Q exit quiz with answer key)
- [x] phase_0_orientation/references.md (consolidated refs)
- [x] phase_0_orientation/03_hardware_check/check.sh (bash probe — mac/linux/wsl2)

## Decisions recorded
- `check.sh` uses `sysctl hw.memsize` (macOS) and `/proc/meminfo` (Linux); no Windows-native path — WSL2 users run it under Linux
- Full profile threshold: 12 GB physical RAM + 12 GB Docker cap + 30 GB free disk
- Light profile threshold: 8 GB physical RAM + 6 GB Docker cap + 15 GB free disk
- Cloud fallback references Codespaces AND Gitpod with pricing page "re-verify current numbers" caveat (free tiers shift)
- Quiz answer keys cite only primary sources (PostgreSQL docs, PEP 518, RFCs, git-scm, GNU coreutils, bash manual)

## Blockers
none

## Next action
Stage 2 — Phase 1 foundations (4 parallel agents: Linux/net · Python · Docker/SQL · Git)
