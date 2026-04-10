# References — Module 06: Observability

## Primary docs — OpenTelemetry
- [OpenTelemetry — Observability primer: signals](https://opentelemetry.io/docs/concepts/signals/) — the three-pillar vocabulary.
- [OpenTelemetry — Metrics signal](https://opentelemetry.io/docs/concepts/signals/metrics/) — instrument types, aggregation.
- [OpenTelemetry — Logs signal](https://opentelemetry.io/docs/concepts/signals/logs/) — structured logs and the logs data model.
- [OpenTelemetry — Traces signal](https://opentelemetry.io/docs/concepts/signals/traces/) — spans, context propagation.

## Primary docs — Prometheus
- [Prometheus — Overview](https://prometheus.io/docs/introduction/overview/) — pull model, architecture.
- [Prometheus — Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) — `scrape_configs`, intervals, relabeling.
- [Prometheus — Metric types](https://prometheus.io/docs/concepts/metric_types/) — counter, gauge, histogram, summary.
- [Prometheus — Querying basics (PromQL)](https://prometheus.io/docs/prometheus/latest/querying/basics/) — range vectors, `rate()`, selectors.

## Primary docs — Grafana
- [Grafana — Data sources](https://grafana.com/docs/grafana/latest/datasources/) — datasource concepts.
- [Grafana — Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/) — file-based datasource and dashboard provisioning.
- [Grafana — Dashboards](https://grafana.com/docs/grafana/latest/dashboards/) — panels, variables, time ranges.

## Primary docs — Dagster
- [Dagster — Asset checks](https://docs.dagster.io/concepts/assets/asset-checks) — including freshness checks.
- [Dagster — Software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets) — the asset mental model.
- [Dagster — Declarative automation](https://docs.dagster.io/concepts/automation/declarative-automation) — freshness-driven scheduling.

## Primary docs — dbt
- [dbt — Tests](https://docs.getdbt.com/docs/build/data-tests) — schema tests as pipeline signals.

## Books
- [*Site Reliability Engineering*, Beyer et al., Ch. 6 — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) — golden signals, symptoms vs. causes, SLI/SLO framing.

## Sibling sources
- `../dataeng/prometheus/prometheus.yml:L4-L44` — Phase 3 stack Prometheus scrape config (global interval, Prometheus self-scrape, Trino health probe, MinIO native metrics).
- `../dataeng/grafana/provisioning/datasources/datasources.yml:L6-L25` — Grafana datasource provisioning: Prometheus default, PostgreSQL secondary, `editable: false`.
- `../dataeng/grafana/provisioning/dashboards/dashboards.yml:L6-L15` — file-based dashboard provider for `/etc/grafana/provisioning/dashboards/json`.
- `../dataeng/grafana/provisioning/dashboards/json/lakehouse-overview.json` — reference lakehouse overview dashboard.
- `../../references/sibling_sources.md:L39-L40` — sibling mapping for Phase 4 · 06_observability → prometheus + grafana config paths.
