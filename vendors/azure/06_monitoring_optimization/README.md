# Module 06 — Monitoring and Optimization

> DP-700 exam weight: Domain 3 (Monitor and optimize, 30–35%). Roughly 15–20 hours.

## Learning goals

- Use Azure Monitor, Log Analytics, and KQL to investigate pipeline failures, Spark job issues, and storage access patterns.
- Navigate the Fabric monitoring hub and capacity metrics app to diagnose workspace-level issues.
- Tune Delta Lake / Fabric lakehouse performance: OPTIMIZE, ZORDER, V-Order, partitioning, file sizing.
- Diagnose and fix data skew and data spill in Spark jobs.
- Configure alerts, action groups, and activator triggers for operational events.
- Read query plans (Spark `.explain()`, Synapse DMVs, Fabric Warehouse query insights) to find bottlenecks.

## Prerequisites

- Completion of modules 01–05 (you need something running to monitor).

## Concepts

### Azure Monitor and Log Analytics

Azure Monitor is the umbrella: **metrics** (numeric, near real-time, 93-day retention) and **logs** (structured, KQL-queryable via Log Analytics). Per-resource **diagnostic settings** route platform logs to a Log Analytics workspace, Storage account, or Event Hub. Default retention varies by table (commonly 30 days; interactive retention up to 730 days, archive up to 12 years). Foundational KQL operators: `where`, `summarize`, `project`, `extend`, `ago()`, `bin()`, `render timechart`, `join kind=`.
Ref: [Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/overview) · [Log Analytics](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-overview)

### Pipeline monitoring

ADF/Synapse/Fabric pipelines emit runs visible in the service's Monitor blade (45-day retention) and, when diagnostic settings are configured, stream to Log Analytics tables `ADFPipelineRun`, `ADFActivityRun`, `ADFTriggerRun`. Copy Activity exposes DIUs used, parallel copies, throughput (MB/s), and a duration breakdown (queue / transfer / post-copy). Fabric pipeline runs land in the **Fabric monitoring hub**, which unifies pipeline, notebook, dataflow, and semantic model refresh runs.
Ref: [Monitor ADF pipelines](https://learn.microsoft.com/en-us/azure/data-factory/monitor-visually) · [Fabric monitoring hub](https://learn.microsoft.com/en-us/fabric/admin/monitoring-hub)

### Service-specific tables

- **Synapse**: `SQLSecurityAuditEvents`, `ExecRequests`, `SparkApplications`.
- **Databricks**: `DatabricksClusters`, `DatabricksJobs`, Unity Catalog audit `system.access.audit`.
- **Stream Analytics**: Execution logs, Authoring logs.
- **Event Hubs**: `AzureMetrics`, `ArchiveLogs`.
- **Fabric capacity metrics app**: separate Power BI app installed per capacity, shows background CU seconds, throttling, smoothing.

Ref: [Fabric capacity metrics app](https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app)

### Small-file compaction and layout

- **`OPTIMIZE table`** bin-packs files to ~256 MB – 1 GB per file.
- **`OPTIMIZE table ZORDER BY (col1, col2)`** co-locates data on up to 3–4 columns; diminishing returns beyond.
- **V-Order** (Fabric default) adds ~15% write time in exchange for faster reads across Power BI, SQL endpoint, and Spark.
- **`delta.autoOptimize.optimizeWrite`** and **`autoCompact`** (Databricks) automate compaction on write.
- **Spark coalesce / repartition**: `coalesce(n)` no shuffle, reduce only; `repartition(n)` full shuffle, can increase or decrease.

Ref: [Delta optimization and V-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order)

### Data skew

**Symptom**: one Spark task takes 10–100× longer than others in the Spark UI. **Fixes**: enable Adaptive Query Execution (`spark.sql.adaptive.enabled=true`) and skew join handling (`spark.sql.adaptive.skewJoin.enabled=true`); manually **salt** the skewed key (append a random suffix and post-join reduce); **broadcast** the small side if one table fits. In Synapse dedicated pools, use `DBCC PDW_SHOWSPACEUSED` to detect distribution skew and re-hash on a higher-cardinality column.
Ref: [Adaptive Query Execution](https://learn.microsoft.com/en-us/azure/databricks/optimizations/aqe)

### Data spill and memory issues

**Spill (memory)** and **Spill (disk)** show up in Spark UI stage details when executor memory is insufficient. Fixes: increase `spark.executor.memory`, increase `spark.sql.shuffle.partitions` (default 200, raise to 400–800 for large jobs), filter earlier to reduce shuffle volume. **Driver OOM** is usually caused by `.collect()` / `.toPandas()` or too-large broadcast threshold.
Ref: [Azure Databricks Spark](https://learn.microsoft.com/en-us/azure/databricks/getting-started/spark/)

### Query tuning — Fabric Warehouse and Synapse

- **Fabric Warehouse**: statistics are maintained automatically on columnar storage; use query insights DMVs (`queryinsights.exec_requests_history`) to find slow queries; there are no user-visible distributions or indexes.
- **Synapse dedicated pool**: CCI rowgroup health (`sys.dm_pdw_nodes_column_store_row_groups`), DMVs (`sys.dm_pdw_exec_requests`, `sys.dm_pdw_request_steps`), look for `ShuffleMove` / `BroadcastMove` operations indicating data movement. Use `OPTION (LABEL = 'name')` to tag queries for later analysis.
- **Result set caching**: Synapse `ALTER DATABASE db SET RESULT_SET_CACHING ON`, auto-invalidated on data change or after 48 h. Materialized views precomputed and auto-used by the optimizer.

Ref: [Synapse DMVs](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-manage-monitor) · [Fabric Warehouse query insights](https://learn.microsoft.com/en-us/fabric/data-warehouse/query-insights)

### Stream monitoring

**Watermark delay** is the single most important ASA metric — growing delay means the job is falling behind. Other key metrics: **SU% Utilization**, **Backlogged Events**, **Out-of-Order Events**. For Spark Structured Streaming, compare input rate vs processing rate in the query monitor; if batch duration > trigger interval, the job is falling behind. In Fabric Real-Time Intelligence, Eventstream state and KQL database ingestion latency are visible in the monitoring hub.
Ref: [Stream Analytics monitoring](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-monitoring)

### Alerts and action groups

- **Metric alerts**: 1-minute evaluation, near-real-time.
- **Log alerts**: ≥5-minute evaluation plus log-ingestion delay (typically 2–5 min).
- **Action groups**: email, SMS (1 per 5 min), webhook, Azure Function, Logic App.
- **Dynamic thresholds**: ML-based baselines for metrics with regular patterns.
- **Fabric activator**: data-driven alerts reacting to values inside Power BI reports or Eventstreams.

Ref: [Azure alerts overview](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview)

## Labs

| Lab | Goal | Est. time | Source |
|---|---|---|---|
| L06.1 KQL pipeline monitoring | Write KQL queries for failed runs, slowest queries, throughput anomalies | 60 m | [KQL tutorial](https://learn.microsoft.com/en-us/kusto/query/tutorial) |
| L06.2 Data skew fix | Reproduce skew, observe in Spark UI, fix with AQE + salting | 45 m | [Adaptive Query Execution](https://learn.microsoft.com/en-us/azure/databricks/optimizations/aqe) |
| L06.3 OPTIMIZE + ZORDER | Measure query time before and after `OPTIMIZE ZORDER BY (col)` | 30 m | [Microsoft Learn: Delta Lake](https://learn.microsoft.com/en-us/azure/databricks/delta/) |
| L06.4 Alert setup | Configure a metric alert on pipeline failures with an action group | 30 m | [Create metric alert](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-metric) |

## Common failures

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| "Pipeline succeeded" in ADF Monitor but downstream data wrong | External activity (Databricks, stored proc) reported success even though the external job failed | Parse activity output, check notebook logs, build explicit validation step | [Monitor ADF pipelines](https://learn.microsoft.com/en-us/azure/data-factory/monitor-visually) |
| Growing ASA watermark delay | Under-provisioned SUs or hot partition | Scale SUs up; repartition input by a higher-cardinality key | [Stream Analytics monitoring](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-monitoring) |
| Delta table has 50 k small files, queries slow | Micro-batch writers without compaction | Run `OPTIMIZE`; enable auto-optimize write/compact | [Delta optimization and V-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order) |
| Fabric capacity throttled | Background CU usage exceeded capacity | Identify offending item in capacity metrics app; schedule heavy jobs off-peak or upsize the capacity | [Fabric capacity metrics](https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app) |

## References

See [references.md](./references.md). Quiz in [quiz.md](./quiz.md).

## Checkpoint

- [ ] I can write a KQL query for "failed pipeline runs in the last 24 hours grouped by pipeline name".
- [ ] I can diagnose data skew from a Spark UI screenshot.
- [ ] I know when to OPTIMIZE, when to ZORDER, and when to leave V-Order alone.
- [ ] I can explain watermark delay and why it is the critical ASA metric.
