# Module 03: Hardware Check (0.5h)

## Learning goals
- Measure your machine's usable RAM, CPU, and free disk
- Verify Docker Desktop (or Docker Engine) is installed and has enough memory allocated
- Decide: full profile, light profile, or cloud fallback

## Prerequisites
- [01_course_structure](../01_course_structure/)

## Reading order
1. This README
2. Run [`check.sh`](./check.sh) and read its output
3. If it flags a problem, read [../04_cloud_fallback/README.md](../04_cloud_fallback/README.md)

## Concepts

### Why this matters
Phase 3 runs a real open-source lakehouse in Docker Compose. Full profile working set is ~12GB RAM; light profile is ~6GB. Phases 1–2 run on anything. Finding out your machine can't hold the stack **after** you've spent 200 hours on Phases 1–2 is a preventable failure.

### Memory budgets (measured against stock Docker images, not theoretical)
| Profile | Services | RAM working set | Disk | Notes |
|---|---|---|---|---|
| Full | MinIO, HMS + Postgres, Trino, Spark, dbt, Dagster, Metabase | ~12GB | ~15GB | Recommended — matches the Phase 3 `docker-compose.yml` topology |
| Light | MinIO, Trino (JDBC Iceberg catalog), dbt, Dagster, Metabase | ~6GB | ~10GB | Drops HMS + Spark; Trino does all compute |
| Cloud fallback | Same as full, on GitHub Codespaces / Gitpod | n/a (remote) | n/a | Use when local RAM < 8GB |

Numbers are working-set (what you'll actually use); add Docker Desktop's own overhead (~2GB) and your OS + editor (~3GB) to get the real floor. **8GB machines run light only**; **<8GB use cloud fallback**.

### What Docker Desktop's memory setting does
On macOS and Windows, Docker Desktop runs containers inside a lightweight VM. The memory cap you set in Docker Desktop → Settings → Resources is the VM's max — containers share that pool. Default on fresh installs is often 8GB; Phase 3 full profile needs this raised to ≥12GB. On Linux, Docker Engine uses host memory directly and has no such setting.
Ref: [Docker Desktop — Resources settings](https://docs.docker.com/desktop/settings/)

### What the check script verifies
`check.sh` is a small bash script (works on macOS, Linux, WSL2) that reports:
1. **Physical RAM** (via `sysctl hw.memsize` on macOS, `/proc/meminfo` on Linux)
2. **Free disk** on the current partition
3. **Docker presence** (`docker --version`)
4. **Docker daemon responsiveness** (`docker info`)
5. **Docker memory limit** (`docker info --format '{{.MemTotal}}'`)
6. **Docker Compose v2 presence** (`docker compose version`)

Then it prints a verdict: FULL / LIGHT / CLOUD_FALLBACK.

Run it:
```bash
bash check.sh
```

Does **not** install anything. Does **not** modify your system. Read the script before you run it.

### Docker install (if the script says "Docker not found")
- **macOS / Windows:** Install [Docker Desktop](https://docs.docker.com/desktop/). Raise the memory cap to ≥12GB in Settings → Resources.
- **Linux:** Install [Docker Engine](https://docs.docker.com/engine/install/) and the [Compose v2 plugin](https://docs.docker.com/compose/install/linux/). Add your user to the `docker` group to avoid `sudo`.
- **WSL2 (Windows):** Docker Desktop's WSL2 backend is the supported path. Ref: [Docker Desktop WSL2 backend](https://docs.docker.com/desktop/features/wsl/)

## Common failures
| Symptom | Cause | Fix |
|---|---|---|
| `docker: command not found` | Docker not installed | Install Docker Desktop or Engine (see links above) |
| `Cannot connect to Docker daemon` | Daemon not running | Start Docker Desktop, or `sudo systemctl start docker` on Linux |
| Compose v1 syntax errors later | Using deprecated `docker-compose` (v1) | Install Compose v2 — invoked as `docker compose ...` (space, not hyphen). Ref: [Compose v2 migration](https://docs.docker.com/compose/migrate/) |
| Script says 12GB physical but Docker MemTotal shows 4GB | Docker Desktop cap too low | Raise in Settings → Resources → Memory |

## References
See [references.md](./references.md).

## Checkpoint
- [ ] Ran `check.sh` — recorded the verdict
- [ ] Docker is installed and responsive
- [ ] Docker memory allocation matches my chosen profile
- [ ] I know which Phase 3 profile I'll use
