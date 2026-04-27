# Lab L1: Compose Healthcheck (Phase 1 exit gate)

## Goal
Stand up PostgreSQL (and optional pgAdmin) via Docker Compose using `.env` credentials, wait for a passing healthcheck, and verify both services with a bash script that exits non-zero on failure.

## Prerequisites
- Docker Engine + Compose v2 installed (`docker compose version` reports v2.x)
- `bash`, `curl` on the host
- 1 GB free RAM

## Setup

Create a new directory and drop in three files.

`docker-compose.yml` — pattern based on the companion lakehouse project's Postgres service:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-lab}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?POSTGRES_PASSWORD must be set}
      POSTGRES_DB: ${POSTGRES_DB:-lab}
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
    mem_limit: 512m
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-lab} -d ${POSTGRES_DB:-lab}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  pgadmin:
    image: dpage/pgadmin4:8.12
    profiles: ["admin"]
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL:-admin@example.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:?PGADMIN_PASSWORD must be set}
      PGADMIN_CONFIG_SERVER_MODE: "False"
    ports:
      - "5050:80"
    mem_limit: 512m
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:80/misc/ping || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 5
      start_period: 20s

volumes:
  pg_data:
```

`.env.example`:

```
POSTGRES_USER=lab
POSTGRES_PASSWORD=change_me
POSTGRES_DB=lab
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=change_me_too
```

`healthcheck.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

require_healthy() {
  local svc="$1"
  local state
  state=$(docker compose ps --format '{{.Name}} {{.Health}}' | awk -v s="$svc" '$1 ~ s {print $2; exit}')
  if [[ "$state" != "healthy" ]]; then
    echo "FAIL: $svc is '${state:-missing}' (expected 'healthy')" >&2
    exit 1
  fi
  echo "OK:   $svc healthy"
}

require_healthy postgres
echo "All required services healthy."
```

## Steps

1. Copy the env template and edit the password.
   ```bash
   cp .env.example .env
   $EDITOR .env
   chmod +x healthcheck.sh
   ```

2. Start the stack in the background.
   ```bash
   docker compose up -d
   ```
   Expected output (abridged):
   ```
    Network lab_default    Created
    Volume  lab_pg_data    Created
    Container lab-postgres-1  Started
   ```

3. Wait for the healthcheck and inspect status.
   ```bash
   docker compose ps
   ```
   Expected (after ~15s):
   ```
   NAME             IMAGE                COMMAND                  STATUS                   PORTS
   lab-postgres-1   postgres:16-alpine   "docker-entrypoint.s…"   Up 20 seconds (healthy)  0.0.0.0:5432->5432/tcp
   ```

4. Run the verification script.
   ```bash
   bash healthcheck.sh
   echo "exit=$?"
   ```
   Expected:
   ```
   OK:   postgres healthy
   All required services healthy.
   exit=0
   ```

5. Prove the script fails loudly when the DB is gone.
   ```bash
   docker compose stop postgres
   bash healthcheck.sh || echo "exit=$?"
   ```
   Expected:
   ```
   FAIL: postgres is 'missing' (expected 'healthy')
   exit=1
   ```
   Restart:
   ```bash
   docker compose start postgres
   ```

## Verify
- [ ] `docker compose ps` lists `postgres` with `(healthy)`
- [ ] `bash healthcheck.sh` exits `0` when running
- [ ] `bash healthcheck.sh` exits non-zero after `docker compose stop postgres`
- [ ] `.env` is present locally and matches a `.gitignore` entry (add `.env` to `.gitignore` before any `git add`)

## Cleanup
```bash
docker compose --profile admin down        # stops all, preserves volume
# full reset (destroys data):
# docker compose --profile admin down -v
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `POSTGRES_PASSWORD must be set` error on `up` | `.env` missing or empty — `cp .env.example .env` and edit |
| `postgres` stays `starting` forever | `docker logs lab-postgres-1` — usually a bad password or volume permissions |
| `pgadmin` unhealthy | Confirm profile flag: `docker compose --profile admin up -d` |
| Port 5432 already in use | Change host port: `"5433:5432"` |

## Stretch goals
- Start the admin UI only when you want it: `docker compose --profile admin up -d`, then visit `http://localhost:5050`. The `profiles:` key follows the same pattern used by MinIO and Trino services in a lakehouse stack. See [Compose — profiles](https://docs.docker.com/compose/how-tos/profiles/).
- Add a second check in `healthcheck.sh` that actually queries Postgres: `docker exec lab-postgres-1 psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c 'SELECT 1;' >/dev/null`.
- Add `cpus: "1.0"` to cap CPU alongside `mem_limit`.

## References
See `../../references.md` (module-level).
