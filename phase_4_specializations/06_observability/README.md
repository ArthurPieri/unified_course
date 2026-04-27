# Module 06: Observability — Metrics, Logs, Traces for Data Pipelines (8h)

> Phase 4 closes with the question every on-call data engineer eventually faces: *is the pipeline actually healthy, and will I know before the business does?* This module covers the three pillars of observability (metrics, logs, traces) via OpenTelemetry's definitions, the two classical dashboard methodologies (RED and USE), the Prometheus pull model you already have running in the Phase 3 stack, Grafana dashboarding, and what specifically to monitor on a lakehouse data pipeline — freshness, row counts, schema changes, task duration. The module also ties alerting philosophy to Google SRE book Chapter 6: alert on symptoms that matter to users, not every twitchy counter.

## Learning goals
- Define the three pillars of observability (metrics, logs, traces) using OpenTelemetry's signal vocabulary.
- Contrast the RED method (Rate, Errors, Duration) with the USE method (Utilization, Saturation, Errors) and pick the right one for a given target, citing Google's SRE book Ch. 6.
- Explain Prometheus's pull model, scrape config, and the four core metric types, citing the Prometheus docs.
- Configure a Grafana datasource and dashboard from provisioning YAML, using the Phase 3 stack's files as the reference.
- Identify the data-pipeline-specific signals to monitor: freshness, row counts, null rates, schema changes, task duration, queue depth.
- Distinguish alerting on SLIs/SLOs ("user-visible symptom") from alerting on causes ("a box is hot"), and justify the preference for symptom alerts from the SRE book.
- Describe Dagster asset freshness checks and how they map to the "freshness" pipeline SLI.

## Prerequisites
- `phase_3_core_tools/` stack running (so you have Prometheus and Grafana reachable on `localhost:9090` and `localhost:3000`).
- Familiarity with Docker Compose and YAML.

## Reading order
1. This README
2. `quiz.md`
3. Google SRE book, Ch. 6 — *Monitoring Distributed Systems* (free: <https://sre.google/sre-book/monitoring-distributed-systems/>)

## Concepts

### The three pillars: metrics, logs, traces
OpenTelemetry defines three core **signals** produced by observability instrumentation: **metrics** (numeric measurements aggregated over time), **logs** (timestamped records with structured or unstructured payloads), and **traces** (ordered spans describing the progression of a single request across services). Each signal answers a different question: metrics say *what* is happening at scale, logs say *why* a specific event happened, and traces say *where* time went inside a single request. You need all three for a complete picture; picking one and skipping the others leaves blind spots.
Ref: [OpenTelemetry — Observability primer: signals](https://opentelemetry.io/docs/concepts/signals/) · [OpenTelemetry — Metrics](https://opentelemetry.io/docs/concepts/signals/metrics/) · [OpenTelemetry — Logs](https://opentelemetry.io/docs/concepts/signals/logs/) · [OpenTelemetry — Traces](https://opentelemetry.io/docs/concepts/signals/traces/)

### RED vs. USE methods
RED (**Rate, Errors, Duration**) is a request-centric view: for every service, dashboard the request rate, the error rate, and the latency distribution. USE (**Utilization, Saturation, Errors**) is a resource-centric view: for every resource (CPU, memory, disk, network), show how busy it is, whether work is queuing up, and whether it is producing errors. The two complement each other — RED is the right framing for a user-facing service; USE is the right framing for the machines and queues underneath. Google's SRE book Chapter 6 lists the **four golden signals** (latency, traffic, errors, saturation) which is close to RED plus saturation.
Ref: [*Site Reliability Engineering*, Beyer et al., Ch. 6 — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)

### Prometheus: the pull model
Prometheus is a time-series database that *pulls* metrics from instrumented targets over HTTP on a configurable interval. Targets expose a `/metrics` endpoint in a line-based text format; Prometheus scrapes them, stores samples, and serves queries via PromQL. The pull model makes target health observable (a scrape failure is itself a signal), decouples publishers from the server, and simplifies service discovery. The Phase 3 stack's `prometheus.yml` configures a 15-second `scrape_interval` and scrapes Prometheus itself, a Trino health probe, and MinIO's native Prometheus endpoint.
Ref: [Prometheus — Overview](https://prometheus.io/docs/introduction/overview/) · [Prometheus — Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)

### Prometheus metric types
Prometheus defines four core metric types: **counter** (monotonic, only goes up, resets on restart — requests served, bytes processed), **gauge** (goes up and down — queue depth, memory in use), **histogram** (samples observations into configurable buckets plus a sum and count — request latency), and **summary** (similar to histogram but computes configurable quantiles client-side). Choosing the right type is a correctness concern: using a gauge where you need a counter makes `rate()` meaningless, and using a summary where you need cross-dimension percentile aggregation makes your p99 uncomputable.
Ref: [Prometheus — Metric types](https://prometheus.io/docs/concepts/metric_types/)

### Grafana datasources and dashboards
Grafana reads from any number of **datasources** (Prometheus, PostgreSQL, Loki, Tempo, …) and renders **dashboards** composed of panels with queries. Dashboards and datasources can be checked into git via provisioning YAML, which Grafana reads from `/etc/grafana/provisioning/` at boot. The Phase 3 stack configures Prometheus as the default datasource in `datasources.yml`, and auto-loads dashboard JSON files via `dashboards.yml`. This is the "dashboards as code" pattern — no click-ops, no dashboards lost when a container restarts.
Ref: [Grafana — Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/) · [Grafana — Data sources](https://grafana.com/docs/grafana/latest/datasources/)

### What to monitor for data pipelines
Data pipelines have signals that generic service monitoring misses. At minimum: **freshness** (how stale is the latest row in the target table vs. the source event time), **row counts** (per-run ingestion volume; a sudden drop is a silent failure), **null / invalid rates** per column (silent schema drift), **schema changes** (a producer added or removed a field), **task duration** (runtime of each DAG task or dbt model), **queue depth** (how many runs are waiting), and **SLA breach counts**. Most of these are emitted by the orchestrator (Dagster, Airflow) as metrics or asset-check results; the rest come from the transformation layer (dbt test results) or the table format (Iceberg metadata tables).
Ref: [Dagster — Asset checks](https://docs.dagster.io/concepts/assets/asset-checks) · [Dagster — Declarative automation and freshness](https://docs.dagster.io/concepts/automation/declarative-automation) · [dbt — Tests](https://docs.getdbt.com/docs/build/data-tests)

### Dagster asset freshness
Dagster models data as **software-defined assets** and lets you attach **freshness checks** that answer "is this asset up-to-date relative to its expected cadence?". A freshness check fails if the asset has not been materialized within a configured window, which maps directly to a pipeline freshness SLI. The Dagster docs describe freshness as a first-class concept with automated scheduling and declarative automation driven off staleness.
Ref: [Dagster — Freshness checks](https://docs.dagster.io/concepts/assets/asset-checks#freshness-checks) · [Dagster — Software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets)

### Alerting on symptoms, not causes
The SRE book Chapter 6 is explicit: alert on **symptoms that users experience** (latency is high, errors are rising, data is stale) rather than on **causes that may not matter** (CPU is hot, a pod restarted, a disk is 80% full). Symptom alerts have low false positive rates because they fire only when something users care about is actually wrong, and they generalize across implementation changes. Cause-based alerts tend to fire during routine operations and train responders to ignore pages, which is the path to missed incidents. The SLI/SLO framing formalizes this: define a user-visible indicator, set an error budget, and alert when burn-rate threatens the budget.
Ref: [*SRE Book*, Ch. 6 — Symptoms vs. Causes](https://sre.google/sre-book/monitoring-distributed-systems/#symptoms-versus-causes) · [*SRE Book*, Ch. 6 — The four golden signals](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals)

### Stack configuration reference
The Phase 3 compose stack already ships a working Prometheus + Grafana configuration. Read it to ground the concepts above:
- `compose/full-stack/` Prometheus scrape configs for Prometheus self, Trino health, MinIO native metrics. Ref: [Prometheus — Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/).
- Grafana datasource provisioning: Prometheus-as-default datasource, PostgreSQL secondary, declared `editable: false` so changes are tracked in git. Ref: [Grafana — Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/).
- File-based dashboard provider that loads JSON from `/etc/grafana/provisioning/dashboards/json`. Ref: [Grafana — Dashboards](https://grafana.com/docs/grafana/latest/dashboards/).
- A reference lakehouse overview dashboard. Based on the companion lakehouse project.

## Labs
This module is configuration- and reading-heavy; the hands-on work happens in the Phase 3 stack you already have running. Recommended exercises (no new lab directory):
- Open `http://localhost:9090/targets` and confirm all scrape targets are `UP`. Identify which job scrapes MinIO.
- Open Grafana at `http://localhost:3000`, log in, and find the "Data Lakehouse" folder provisioned by `dashboards.yml`.
- Write a PromQL query that returns MinIO request rate as `rate(minio_s3_requests_total[5m])` and build a one-panel dashboard for it.
- Write a freshness SLI: a gauge that is 1 if the latest row in an Iceberg table is less than 1 hour old, else 0.

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Prometheus target `DOWN` | Target container not healthy or wrong port | `docker compose ps`; check `scrape_configs.static_configs.targets` | [Prometheus configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) |
| Grafana "No data" on a Prometheus panel | Wrong datasource uid or time range | Verify datasource in `datasources.yml`; zoom time range | [Grafana data sources](https://grafana.com/docs/grafana/latest/datasources/) |
| `rate()` always returns 0 | Metric is a gauge, not a counter | Switch to counter or use `delta()` | [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/) |
| Every minor blip pages on-call | Alerts on causes, not symptoms | Re-derive alerts from user-visible SLIs | [SRE Book Ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) |
| No alert fires when a nightly ETL is 6 h late | No freshness check on the target asset | Add a Dagster freshness check | [Dagster freshness](https://docs.dagster.io/concepts/assets/asset-checks#freshness-checks) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Name the three OpenTelemetry signals and one question each answers.
- [ ] State RED and USE and pick which to apply to (a) a Trino coordinator (b) a Kafka broker's disk.
- [ ] Explain Prometheus's pull model and the four metric types.
- [ ] Edit `datasources.yml` to add a second Prometheus datasource and explain why `editable: false` is a feature not a bug.
- [ ] List the six pipeline-specific signals and name the tool that emits each.
- [ ] Justify alerting on symptoms rather than causes with a concrete example.
