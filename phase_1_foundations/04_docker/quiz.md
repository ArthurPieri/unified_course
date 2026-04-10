# Quiz — 04_docker

Ten multiple-choice questions. Answers at the bottom.

---

**1.** Which Compose key waits for a dependency to pass its healthcheck before starting the dependent service?

A. `depends_on: [postgres]`
B. `depends_on: postgres: condition: service_started`
C. `depends_on: postgres: condition: service_healthy`
D. `links: [postgres]`

**2.** You set `image: postgres:latest` in compose. Why is this discouraged for a course stack?

A. `latest` images are always larger
B. The tag can silently advance to a new major version, breaking on-disk data formats
C. `latest` cannot be used with `depends_on`
D. `latest` disables healthchecks

**3.** A service has `healthcheck.start_period: 60s`, `interval: 10s`, `retries: 5`. Which statement is correct?

A. Failing probes during the 60s grace period do not count toward `retries`
B. The container is marked unhealthy after 60s regardless of probe result
C. `start_period` overrides `interval`
D. `start_period` is only valid on Swarm

**4.** In a Dockerfile, what is the effect of `ENTRYPOINT ["python"]` combined with `CMD ["app.py"]`?

A. Only `python` runs
B. Only `app.py` runs
C. The container runs `python app.py`; `docker run <img> other.py` runs `python other.py`
D. It is a syntax error

**5.** Which command runs a shell inside an already-running container named `pg`?

A. `docker run -it pg sh`
B. `docker exec -it pg sh`
C. `docker attach pg sh`
D. `docker shell pg`

**6.** What does `docker compose down -v` delete that plain `down` does not?

A. The images
B. The networks
C. The named volumes declared in the compose file
D. The `.env` file

**7.** Where should `DB_PASSWORD=s3cret` live so Compose picks it up without committing the secret?

A. In `docker-compose.yml` under `environment:`
B. In a `.env` file beside `docker-compose.yml`, listed in `.gitignore`
C. As a shell alias
D. Inside the image via `ENV DB_PASSWORD=s3cret`

**8.** A service has `profiles: ["admin"]`. Which command starts it?

A. `docker compose up -d`
B. `docker compose --profile admin up -d`
C. `docker compose up -d admin`
D. `docker compose run admin`

**9.** Why are multi-stage builds preferred for Python application images?

A. They make `CMD` optional
B. They let the final image omit build tools like compilers and `pip` caches, shrinking size and attack surface
C. They are required when using `.env`
D. They disable layer caching

**10.** Two services in the same Compose project need to talk. By default, how does service `app` reach service `db`?

A. Via the host's `localhost`
B. Via the container's IP, which must be hardcoded
C. Via the hostname `db` on the project's default bridge network
D. They cannot communicate without `network_mode: host`

---

## Answer key

1. **C** — Long-form `depends_on` with `condition: service_healthy` is the only form that blocks on health. [Compose depends_on](https://docs.docker.com/reference/compose-file/services/#depends_on)
2. **B** — Pinning (e.g., `postgres:16-alpine`) is the documented defense against silent upgrades; the dataeng reference stack pins every image (`../dataeng/docker-compose.yml:L9`). [Dockerfile reference — FROM](https://docs.docker.com/reference/dockerfile/#from)
3. **A** — `start_period` is explicitly a grace window where failing probes do not count. [Compose healthcheck](https://docs.docker.com/reference/compose-file/services/#healthcheck)
4. **C** — `CMD` supplies default args to `ENTRYPOINT`; `docker run` positional args replace `CMD`. [Dockerfile reference — ENTRYPOINT](https://docs.docker.com/reference/dockerfile/#entrypoint)
5. **B** — `docker exec` targets a running container; `docker run` starts a new one. [docker exec](https://docs.docker.com/reference/cli/docker/container/exec/)
6. **C** — `-v` removes named volumes declared in the file. [docker compose down](https://docs.docker.com/reference/cli/docker/compose/down/)
7. **B** — Compose auto-loads a sibling `.env`; the file must be gitignored. [Compose env vars](https://docs.docker.com/compose/how-tos/environment-variables/)
8. **B** — Profiled services only start when their profile is activated. [Compose profiles](https://docs.docker.com/compose/how-tos/profiles/)
9. **B** — Multi-stage lets the final stage `COPY --from=<builder>` only runtime artifacts. [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
10. **C** — Compose creates a default bridge network; services resolve each other by service name. [Compose networking](https://docs.docker.com/compose/how-tos/networking/)
