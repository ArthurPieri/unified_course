# Module 04: Docker & Compose for Data (12h)

> Containers are the delivery mechanism for every tool in this course. Phase 3's full lakehouse stack is ~10 services in one Compose file — you need fluency with images, volumes, networks, healthchecks, and `.env` secrets before you touch it.

## Learning goals
- Explain the image/container/volume/network model and why each exists
- Write a Dockerfile using `FROM`, `COPY`, `RUN`, `ENV`, `WORKDIR`, and a correct `CMD`/`ENTRYPOINT` pair
- Author a `docker-compose.yml` with services, pinned versions, `.env` secrets, `mem_limit`, and a `healthcheck`
- Use `depends_on` with `condition: service_healthy` to sequence startup
- Activate optional services via Compose `profiles`
- Debug a broken stack with `docker logs`, `docker exec`, `docker inspect`, `docker compose ps`

## Prerequisites
- [../01_linux_bash/](../01_linux_bash/) — shell, processes, env vars
- [../02_networking/](../02_networking/) — ports, localhost, DNS

## Reading order
1. This README
2. [labs/lab_L1_compose_healthcheck/README.md](labs/lab_L1_compose_healthcheck/README.md)
3. [quiz.md](quiz.md)

## Concepts

### The four objects: image, container, volume, network
An **image** is an immutable filesystem + metadata built from a Dockerfile. A **container** is a running (or stopped) instance of an image — its writable layer disappears when you `docker rm` it. A **volume** is persistent storage managed by Docker, mounted into a container path; data survives container removal. A **network** is a virtual L2/L3 segment that lets containers reach each other by service name. Compose creates a default bridge network per project so `trino` can reach `postgres` at hostname `postgres`.
Ref: [Docker overview](https://docs.docker.com/get-started/overview/) · [Storage — volumes](https://docs.docker.com/storage/volumes/) · [Networking overview](https://docs.docker.com/network/)

### Dockerfile essentials
`FROM` chooses a base image (pin the tag — never `:latest` in production). `WORKDIR` sets the cwd for subsequent instructions. `COPY` pulls files from the build context into the image. `RUN` executes a shell command at build time and bakes the result into a new layer. `ENV` sets environment variables visible at build and run time. `CMD` provides default arguments; `ENTRYPOINT` sets the executable. When both are present, `CMD` becomes arguments to `ENTRYPOINT` — this is the correct pattern for wrappers that accept flags.
Ref: [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)

### Multi-stage builds
A single Dockerfile can declare multiple `FROM` stages. Later stages `COPY --from=<stage>` only the artifacts they need, so build tools (compilers, `pip`, `uv`) never ship in the final image. Smaller images pull faster, expose less surface, and cache better.
Ref: [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

### Compose services, version pinning, and `.env`
Compose declares a set of services in one YAML file. Every `image:` tag should be pinned to a specific version — for example, `postgres:16-alpine`, `trinodb/trino:470`, `apache/hive:4.0.1`, `metabase/metabase:v0.51.0`. `postgres:latest` is a moving target; a silent major-version bump can break schemas. Secrets come from a `.env` file sitting next to `docker-compose.yml`; Compose reads it automatically. Reference secrets with `${VAR}` or `${VAR:-default}` in the YAML so the file itself stays committable. The `.env` file must be in `.gitignore` — commit a `.env.example` with placeholder values instead.
Ref: [Compose file — services](https://docs.docker.com/reference/compose-file/services/) · [Compose — environment variables](https://docs.docker.com/compose/how-tos/environment-variables/)

### Healthchecks and `depends_on: condition: service_healthy`
A healthcheck is a command Compose runs inside the container at a fixed `interval`; a non-zero exit for `retries` in a row marks the container `unhealthy`. `start_period` gives slow boots a grace window where failing probes do not count against `retries`. Other services that declare `depends_on: <name>: condition: service_healthy` are held back until the dependency reports healthy — this is how a lakehouse stack guarantees a metastore does not start before its backing database is accepting connections. Canonical probes: `pg_isready` for Postgres, an HTTP request (`curl -f http://localhost:9000/minio/health/live`) for MinIO, a TCP check with `nc -z` for thrift-style services.
Ref: [Compose — healthcheck](https://docs.docker.com/reference/compose-file/services/#healthcheck) · [Compose — depends_on long syntax](https://docs.docker.com/reference/compose-file/services/#depends_on)

### Profiles
`profiles:` marks a service as optional — it only starts when you run `docker compose --profile <name> up`. A lakehouse stack can use profiles to slice services into storage/metadata/query/orchestration/visualization subsets (e.g., MinIO under `storage`, Trino under `query`). A service with no `profiles` key runs unconditionally — for example, a baseline `postgres` service with no profile starts on every invocation.
Ref: [Compose — profiles](https://docs.docker.com/compose/how-tos/profiles/)

### Resource limits
`mem_limit` caps a container's RAM; the kernel's OOM killer terminates processes that exceed it. Typical limits for a lakehouse stack: Postgres at 512m, a Hive metastore at 1g, Trino at 5g. Without limits a runaway Spark driver can freeze a 16GB laptop. `cpus:` sets a fractional CPU share. Both keys belong at the service level.
Ref: [Compose file — services (mem_limit, cpus)](https://docs.docker.com/reference/compose-file/services/)

### Troubleshooting loop
`docker compose ps` shows state and health per service. `docker logs <container>` streams stdout/stderr — add `-f` to follow and `--tail 100` to limit. `docker exec -it <container> sh` drops you into a running container for live inspection. `docker inspect <container>` dumps full JSON state including mounts, network aliases, and the resolved healthcheck command. When a service is stuck `starting`, the healthcheck is the first thing to check.
Ref: [docker logs](https://docs.docker.com/reference/cli/docker/container/logs/) · [docker exec](https://docs.docker.com/reference/cli/docker/container/exec/) · [docker inspect](https://docs.docker.com/reference/cli/docker/inspect/) · [docker compose ps](https://docs.docker.com/reference/cli/docker/compose/ps/)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L1_compose_healthcheck` | Stand up Postgres + pgAdmin with healthchecks, `.env` credentials, and a bash verification script (Phase 1 exit gate) | 90m | [labs/lab_L1_compose_healthcheck/](labs/lab_L1_compose_healthcheck/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `depends_on` ignored — dependent service crashes on boot | Short-form `depends_on: [name]` waits for start, not health | Use long-form with `condition: service_healthy` | [Compose depends_on](https://docs.docker.com/reference/compose-file/services/#depends_on) |
| `.env` values missing at runtime | `.env` not in the same directory as `docker-compose.yml` | Place `.env` beside the compose file or pass `--env-file` | [Compose env vars](https://docs.docker.com/compose/how-tos/environment-variables/) |
| Data disappears after `docker compose down -v` | `-v` deletes named volumes | Omit `-v` for normal stops; only use when you want a clean slate | [docker compose down](https://docs.docker.com/reference/cli/docker/compose/down/) |
| Container `unhealthy` but app works | Healthcheck command not installed in the image | Use `CMD-SHELL` with a tool known to exist (`pg_isready`, `wget`, `curl`) | [Compose — healthcheck](https://docs.docker.com/reference/compose-file/services/#healthcheck) |
| Port already in use | Another process bound the host port | Change host side of `"HOST:CONTAINER"` mapping | [Compose networking](https://docs.docker.com/compose/how-tos/networking/) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Explain images vs containers vs volumes vs networks in one sentence each
- [ ] Write a Compose service with pinned image, `.env` secret, `mem_limit`, and healthcheck
- [ ] Gate service B on service A's health with long-form `depends_on`
- [ ] Put a service behind a `--profile` flag
- [ ] Debug an `unhealthy` container using `docker logs` and `docker inspect`
