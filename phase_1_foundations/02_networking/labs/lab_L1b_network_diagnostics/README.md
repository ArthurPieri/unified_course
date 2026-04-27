# Lab L1b: Network Diagnostics in a Docker Compose Stack

## Goal
Diagnose and fix three deliberately broken network configurations in a multi-service Docker Compose stack using `curl`, `dig`, `ss`, and container inspection.

## Prerequisites
- Docker + Compose v2
- `curl` and `dig` installed on the host (or use `docker exec` into containers)
- Module 02 (Networking Fundamentals) README read

## Setup

Save the following as `docker-compose.yml` in this directory:

```yaml
services:
  web:
    image: nginx:1.27-alpine
    ports: ["8080:80"]
    networks: [frontend]

  api:
    image: python:3.11-slim
    command: >
      python -c "
      from http.server import HTTPServer, BaseHTTPRequestHandler
      import json
      class H(BaseHTTPRequestHandler):
          def do_GET(self):
              self.send_response(200)
              self.send_header('Content-Type','application/json')
              self.end_headers()
              self.wfile.write(json.dumps({'status':'ok'}).encode())
      HTTPServer(('0.0.0.0', 5000), H).serve_forever()
      "
    networks: [backend]

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: lab
      POSTGRES_PASSWORD: lab
      POSTGRES_DB: lab
    networks: [backend]
```

```bash
docker compose up -d
```

## Steps

### Scenario 1: Cross-network isolation

1. Try to reach the `api` service from the `web` container:
   ```bash
   docker exec $(docker compose ps -q web) sh -c "apk add --no-cache curl && curl -s http://api:5000/"
   ```
   **Expected:** Failure — `web` is on `frontend`, `api` is on `backend`. They cannot resolve each other's names.

2. **Diagnose:** Inspect the networks:
   ```bash
   docker network ls | grep -E "frontend|backend"
   docker inspect $(docker compose ps -q web) | grep -A5 Networks
   docker inspect $(docker compose ps -q api) | grep -A5 Networks
   ```

3. **Fix:** Add `api` to the `frontend` network (or add a shared network). Update the compose file:
   ```yaml
   services:
     api:
       networks: [frontend, backend]
   networks:
     frontend:
     backend:
   ```
   Restart and verify:
   ```bash
   docker compose down && docker compose up -d
   docker exec $(docker compose ps -q web) sh -c "curl -s http://api:5000/"
   ```
   **Expected:** `{"status":"ok"}`

### Scenario 2: Port binding confusion

1. From the host, try to reach the API:
   ```bash
   curl -s http://localhost:5000/
   ```
   **Expected:** Connection refused — port 5000 is not published to the host.

2. **Diagnose:** Check which ports are published:
   ```bash
   docker compose ps --format "table {{.Service}}\t{{.Ports}}"
   ss -tlnp | grep -E "5000|8080"
   ```
   Port 8080 is bound (nginx), port 5000 is not.

3. **Fix:** Add `ports: ["5000:5000"]` to the `api` service, restart, and verify:
   ```bash
   curl -s http://localhost:5000/
   ```
   **Expected:** `{"status":"ok"}`

### Scenario 3: DNS resolution inside containers

1. From inside the `api` container, resolve `db`:
   ```bash
   docker exec $(docker compose ps -q api) python -c "import socket; print(socket.gethostbyname('db'))"
   ```
   **Expected:** Returns the container IP (e.g., `172.19.0.3`).

2. Now try resolving `web` from `api` (before the Scenario 1 fix):
   ```bash
   docker exec $(docker compose ps -q api) python -c "import socket; print(socket.gethostbyname('web'))"
   ```
   **Expected:** `socket.gaierror` — `web` is on a different network.

3. Check the DNS resolver inside the container:
   ```bash
   docker exec $(docker compose ps -q api) cat /etc/resolv.conf
   ```
   Note the `nameserver 127.0.0.11` — Docker's embedded DNS server for user-defined networks.

### Scenario 4: Database connectivity trace

1. Verify `db` is listening:
   ```bash
   docker exec $(docker compose ps -q db) ss -tlnp | grep 5432
   ```
   **Expected:** `LISTEN` on `0.0.0.0:5432`.

2. Connect from `api` to `db`:
   ```bash
   docker exec $(docker compose ps -q api) python -c "
   import socket
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.settimeout(3)
   result = s.connect_ex(('db', 5432))
   print('Connection successful' if result == 0 else f'Failed with code {result}')
   s.close()
   "
   ```
   **Expected:** `Connection successful`

3. Try the same from `web` (should fail if networks are still separate):
   ```bash
   docker exec $(docker compose ps -q web) sh -c "nc -z -w3 db 5432 && echo OK || echo FAIL"
   ```

## Verify
- [ ] Scenario 1: Confirmed that services on different networks cannot resolve each other by name
- [ ] Scenario 1: After adding a shared network, cross-service HTTP call succeeds
- [ ] Scenario 2: Confirmed that unpublished container ports are unreachable from the host
- [ ] Scenario 2: After publishing the port, `curl localhost:5000` returns JSON
- [ ] Scenario 3: Docker's embedded DNS (`127.0.0.11`) resolves service names within the same network
- [ ] Scenario 4: TCP connectivity from `api` to `db:5432` succeeds on the shared `backend` network

## Cleanup
```bash
docker compose down -v
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `curl: command not found` in alpine | `apk add --no-cache curl` inside the container |
| `nc: command not found` | Use `python` socket check instead, or `apk add netcat-openbsd` |
| All services can reach each other immediately | Check that the compose file defines separate `frontend`/`backend` networks |
| Port conflict on 8080 | Change `ports: ["8081:80"]` for the web service |

## Stretch goals
- Add a `tcpdump` capture on the backend network and observe the TCP three-way handshake between `api` and `db`.
- Modify `db` to bind only to `127.0.0.1` inside the container and observe that `api` can no longer connect.
- Add a fourth service on `network_mode: host` and verify it can reach host ports but not container DNS names.

## References
See [`../../references.md`](../../references.md) (module-level).
