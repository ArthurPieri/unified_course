# Lab 01: Defensive Bash Healthcheck for a Compose Stack

## Goal
Write a `healthcheck.sh` script that verifies three things — a running PostgreSQL container, an HTTP endpoint, and a mounted data directory — and returns a meaningful exit code so cron, CI, or a supervisor can act on it.

## Prerequisites
- Docker Desktop (or Docker Engine) with `docker compose` available. Ref: [Docker Compose](https://docs.docker.com/compose/).
- `bash` ≥ 4, `curl`, `jq` installed. Ref: [jq manual](https://jqlang.github.io/jq/manual/).
- You completed the module README. Ref: [`../../README.md`](../../README.md).

## Setup

Create a lab directory and a minimal Compose file:

```bash
mkdir -p ~/labs/lab_01_bash && cd ~/labs/lab_01_bash
mkdir -p ./data
cat > docker-compose.yml <<'YAML'
services:
  postgres:
    image: postgres:16-alpine
    container_name: lab01_pg
    environment:
      POSTGRES_PASSWORD: lab
      POSTGRES_USER: lab
      POSTGRES_DB: lab
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U lab"]
      interval: 5s
      timeout: 3s
      retries: 5
    ports:
      - "5432:5432"
    volumes:
      - ./data:/var/lib/postgresql/data
YAML
docker compose up -d
docker compose ps
```

Expected (abridged):
```
NAME        IMAGE               STATUS                   PORTS
lab01_pg    postgres:16-alpine  Up 10 seconds (healthy)  0.0.0.0:5432->5432/tcp
```
Ref: [Compose file: healthcheck](https://docs.docker.com/reference/compose-file/services/#healthcheck).

## Steps

1. Create `healthcheck.sh` with a defensive prelude and three checks:

```bash
cat > healthcheck.sh <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

URL="${URL:-https://example.com}"
MOUNT="${MOUNT:-./data}"
CONTAINER="${CONTAINER:-lab01_pg}"

fail=0
report() { printf '%-10s %s\n' "$1" "$2"; }

check_postgres() {
  local status
  status=$(docker inspect --format '{{.State.Health.Status}}' "$CONTAINER" 2>/dev/null || echo "missing")
  if [[ "$status" == "healthy" ]]; then
    report PASS "postgres ($CONTAINER) healthy"
  else
    report FAIL "postgres ($CONTAINER) status=$status"
    fail=1
  fi
}

check_url() {
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "$URL" || echo "000")
  if [[ "$code" =~ ^2[0-9][0-9]$ ]]; then
    report PASS "url $URL -> $code"
  else
    report FAIL "url $URL -> $code"
    fail=1
  fi
}

check_mount() {
  if [[ -d "$MOUNT" && -w "$MOUNT" ]]; then
    report PASS "mount $MOUNT writable"
  else
    report FAIL "mount $MOUNT missing or not writable"
    fail=1
  fi
}

for svc in postgres url mount; do
  "check_${svc}"
done

exit "$fail"
BASH
chmod +x healthcheck.sh
```
Ref: [Bash Reference Manual: The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) · [Docker CLI: docker inspect](https://docs.docker.com/reference/cli/docker/inspect/).

2. Run it against a healthy stack:

```bash
./healthcheck.sh; echo "exit=$?"
```

Expected:
```
PASS       postgres (lab01_pg) healthy
PASS       url https://example.com -> 200
PASS       mount ./data writable
exit=0
```

3. Break one service and re-run:

```bash
docker compose stop postgres
./healthcheck.sh; echo "exit=$?"
```

Expected:
```
FAIL       postgres (lab01_pg) status=missing
PASS       url https://example.com -> 200
PASS       mount ./data writable
exit=1
```

4. Restart and confirm recovery:

```bash
docker compose start postgres
sleep 10
./healthcheck.sh; echo "exit=$?"
```
Expected: three PASS lines and `exit=0`.

## Verify
- [ ] Healthy stack → three PASS lines and exit code `0`.
- [ ] Postgres stopped → one FAIL, two PASS, exit code `1`.
- [ ] Removing the `./data` directory → mount FAIL and exit code `1`.
- [ ] Running under `bash -x ./healthcheck.sh` prints each command before execution (useful for debugging). Ref: [Bash: The Set Builtin (`-x`)](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html).

## Cleanup

```bash
docker compose down -v
cd ~ && rm -rf ~/labs/lab_01_bash
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `docker: command not found` | Install Docker Desktop / Engine. Ref: [Docker Desktop install](https://docs.docker.com/desktop/) |
| `jq: command not found` | `brew install jq` / `apt install jq`. Ref: [jq manual](https://jqlang.github.io/jq/manual/) |
| Script says `healthy` but `curl` fails | Corporate proxy or DNS — test with `curl -v https://example.com` first |
| `unbound variable` error | `set -u` caught a typo in a variable name, or an env var you expected is not set — use `"${VAR:-default}"` |
| macOS `sed -i` fails | BSD sed needs an empty backup suffix: `sed -i '' ...` |

## Stretch goals
- Add a `--json` flag that emits structured output. Hint: build an array of check results and pipe through `jq -c` to serialize. Ref: [jq manual](https://jqlang.github.io/jq/manual/).
- Add a `--timeout SECS` flag that applies to every check (wrap each check with `timeout "$TIMEOUT"`). Ref: [GNU coreutils: timeout](https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html).
- Wire it into cron to run every 5 minutes and append results to `/var/log/healthcheck.log`. Ref: `../../../01_linux_bash/README.md` (cron section).

## References
See [`../../references.md`](../../references.md) (module-level).
