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

## Sibling reuse
- `../../../dataeng/docker-compose.yml:L8-L23` — baseline Postgres service with `.env`, `mem_limit`, `pg_isready` healthcheck
- `../../../dataeng/docker-compose.yml:L26-L43` — MinIO with profile + HTTP healthcheck
- `../../../dataeng/docker-compose.yml:L62-L88` — Hive metastore with long-form `depends_on: service_healthy` + `start_period`
- `../../../dataeng/docker-compose.yml:L91-L112` — Trino with `mem_limit`, `JAVA_TOOL_OPTIONS`, `curl`-based healthcheck
- `../../../dataeng/docker-compose.yml:L236-L243` — named-volume declarations

## Port facts
- [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) — Postgres `5432/tcp`, HTTP `80/tcp`, HTTPS `443/tcp`
