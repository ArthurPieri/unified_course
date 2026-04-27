# Quiz — Module 06: Observability

8 multiple-choice questions. Answer key at the bottom.

---

**Q1.** What are OpenTelemetry's three core signals, and which question does each primarily answer?

A. Events, alerts, dashboards — "what, when, where".
B. Metrics, logs, traces — "what at scale", "why a specific event", "where did time go in a request".
C. CPU, memory, disk — "how busy, how full, how fast".
D. SLIs, SLOs, SLAs — "indicator, objective, agreement".

---

**Q2.** The RED method dashboards which three quantities for a service, and the USE method dashboards which three for a resource?

A. RED: Requests, Errors, Dependencies. USE: Up, Saturation, Errors.
B. RED: Rate, Errors, Duration. USE: Utilization, Saturation, Errors.
C. RED: Reliability, Efficiency, Durability. USE: Uptime, Speed, Errors.
D. RED: Rate, Endpoints, Duration. USE: Utilization, Saturation, Events.

---

**Q3.** Which statement about Prometheus's scrape model is correct?

A. Targets push samples to Prometheus on each change.
B. Prometheus pulls metrics from targets over HTTP on a configurable interval; a failed scrape is itself an observable signal.
C. Prometheus requires a sidecar exporter for every target.
D. Prometheus stores raw event payloads alongside counters.

---

**Q4.** Which Prometheus metric type is correct for "bytes processed by the ingestion job since start-up", and why?

A. Gauge — the value can go up or down.
B. Counter — the value is monotonically increasing and `rate()` on a range vector gives throughput.
C. Histogram — you need quantile aggregation.
D. Summary — you need client-side quantiles.

---

**Q5.** Per the Phase 3 stack's `datasources.yml`, the Prometheus datasource is marked `editable: false`. Why is this a feature?

A. It prevents the Grafana UI from diverging from the version-controlled provisioning file.
B. It reduces Grafana's CPU load.
C. It is required for Prometheus queries to work.
D. It hides the datasource from users.

---

**Q6.** Which of the following is a *data-pipeline-specific* signal that generic service monitoring typically misses?

A. CPU utilization of the orchestrator host.
B. HTTP request rate on the Grafana UI.
C. Freshness of the target table relative to the source event time.
D. TCP retransmit count on the worker node.

---

**Q7.** Google's SRE book Chapter 6 argues you should primarily alert on:

A. Any cause — CPU hot, restart, disk 80% — because it might turn into a symptom.
B. Symptoms that users experience (latency, errors, freshness) rather than causes that may not matter.
C. Every log line tagged ERROR.
D. Only on-call manager escalations.

---

**Q8.** In Dagster, how do you express "this asset must be materialized within the last N hours or the pipeline is unhealthy"?

A. A freshness check attached to the asset (an asset check), which fails when the asset's staleness exceeds the configured window.
B. A manual Slack ping from on-call.
C. A cron job that counts rows.
D. A Grafana panel only.

---

## Answer key

1. **B** — Metrics, logs, traces — the OpenTelemetry signals concept page. ([OTel signals](https://opentelemetry.io/docs/concepts/signals/))
2. **B** — RED = Rate/Errors/Duration (request-centric); USE = Utilization/Saturation/Errors (resource-centric); both referenced in SRE book Ch. 6's golden-signals framing. ([SRE book Ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/))
3. **B** — Pull model; scrape failures are observable. ([Prometheus overview](https://prometheus.io/docs/introduction/overview/))
4. **B** — Monotonic counts belong in a counter; `rate()` is defined on counters. ([Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/))
5. **A** — Provisioned resources are pinned to file; UI changes would drift from git. ([Grafana provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/))
6. **C** — Freshness is the canonical data-pipeline SLI; generic monitoring misses it because it requires joining orchestrator state with source event time. ([Dagster freshness checks](https://docs.dagster.io/concepts/assets/asset-checks))
7. **B** — Symptoms, not causes. ([SRE Book Ch. 6 — Symptoms vs. Causes](https://sre.google/sre-book/monitoring-distributed-systems/#symptoms-versus-causes))
8. **A** — Dagster freshness checks on assets. ([Dagster asset checks](https://docs.dagster.io/concepts/assets/asset-checks))
