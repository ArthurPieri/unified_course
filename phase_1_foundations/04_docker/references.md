# References — 04_docker

## Primary docs (docs.docker.com)
- [Docker overview](https://docs.docker.com/get-started/overview/) — image/container/volume/network model
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) — all instructions, `CMD` vs `ENTRYPOINT`
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/) — `COPY --from=<stage>` pattern
- [Storage — volumes](https://docs.docker.com/storage/volumes/) — persistence model
- [Networking overview](https://docs.docker.com/network/) — bridge/host/overlay drivers
- [Compose file — services](https://docs.docker.com/reference/compose-file/services/) — full spec (image, volumes, mem_limit, cpus)
- [Compose — healthcheck](https://docs.docker.com/reference/compose-file/services/#healthcheck) — `test`, `interval`, `timeout`, `retries`, `start_period`
- [Compose — depends_on long syntax](https://docs.docker.com/reference/compose-file/services/#depends_on) — `condition: service_healthy`
- [Compose — profiles](https://docs.docker.com/compose/how-tos/profiles/) — optional services
- [Compose — environment variables & `.env`](https://docs.docker.com/compose/how-tos/environment-variables/)
- [Compose — networking](https://docs.docker.com/compose/how-tos/networking/)
- [docker logs](https://docs.docker.com/reference/cli/docker/container/logs/)
- [docker exec](https://docs.docker.com/reference/cli/docker/container/exec/)
- [docker inspect](https://docs.docker.com/reference/cli/docker/inspect/)
- [docker compose ps](https://docs.docker.com/reference/cli/docker/compose/ps/)
- [docker compose down](https://docs.docker.com/reference/cli/docker/compose/down/)

## Compose patterns (based on the companion lakehouse project)
- Baseline Postgres service: `.env` for credentials, `mem_limit: 512m`, `pg_isready` healthcheck
- MinIO with `profiles:` + HTTP healthcheck (`curl -f http://localhost:9000/minio/health/live`)
- Hive metastore with long-form `depends_on: service_healthy` + `start_period`
- Trino with `mem_limit: 5g`, `JAVA_TOOL_OPTIONS`, `curl`-based healthcheck
- Named-volume declarations for persistent data across `docker compose down`

## Port facts
- [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) — Postgres `5432/tcp`, HTTP `80/tcp`, HTTPS `443/tcp`
