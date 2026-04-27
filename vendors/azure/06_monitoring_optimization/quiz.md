# Module 06 — Quiz (Monitoring & Optimization)

1. Which KQL operator groups rows and computes an aggregate in one step?
   - A. `project`
   - B. `summarize`
   - C. `where`
   - D. `extend`

2. Default retention for Azure Monitor metrics is:
   - A. 30 days
   - B. 90 days
   - C. 93 days
   - D. 1 year

3. You see one Spark task at 45 minutes while 199 others finish in seconds. The most likely cause is:
   - A. Insufficient cores
   - B. Data skew on the join key
   - C. Too many output files
   - D. Checkpoint corruption

4. Which setting enables automatic skew join handling in Spark?
   - A. `spark.sql.shuffle.partitions=200`
   - B. `spark.sql.adaptive.enabled=true` plus `spark.sql.adaptive.skewJoin.enabled=true`
   - C. `spark.driver.memory=16g`
   - D. `spark.executor.instances=20`

5. You have 10,000 small Delta files slowing queries. Which command should you run first?
   - A. `VACUUM RETAIN 0 HOURS`
   - B. `OPTIMIZE`
   - C. `DESCRIBE HISTORY`
   - D. `MERGE`

6. Which streaming metric is the single most important indicator that a Stream Analytics job is falling behind?
   - A. SU % Utilization
   - B. Input Events
   - C. Watermark Delay
   - D. Output Events

7. Fabric pipeline runs, notebook runs, and dataflow refreshes appear together in:
   - A. The Synapse Monitor blade
   - B. The Fabric monitoring hub
   - C. Azure Advisor
   - D. Purview Insights

8. The difference between a **metric** alert and a **log** alert is:
   - A. Log alerts are faster than metric alerts.
   - B. Metric alerts evaluate near real-time (~1 min); log alerts evaluate on a ≥5-min schedule plus ingestion delay.
   - C. They are identical.
   - D. Metric alerts cannot trigger action groups.

9. Your Spark driver throws `OutOfMemoryError`. The most likely cause?
   - A. Too many executors
   - B. A `.collect()` or `.toPandas()` call bringing a large dataset to the driver
   - C. Slow network
   - D. Stale Delta transaction log

10. In Fabric, a "sudden spike in background CU usage causing throttling" is diagnosed in:
    - A. Azure Cost Management
    - B. Fabric capacity metrics app
    - C. Purview
    - D. Azure Advisor

---

## Answer key

1. **B** — [KQL summarize](https://learn.microsoft.com/en-us/kusto/query/summarize-operator).
2. **C** — 93 days for metrics ([Azure Monitor metrics](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-platform-metrics)).
3. **B** — Data skew; see [Adaptive Query Execution](https://learn.microsoft.com/en-us/azure/databricks/optimizations/aqe).
4. **B** — [Adaptive Query Execution](https://learn.microsoft.com/en-us/azure/databricks/optimizations/aqe).
5. **B** — [Delta OPTIMIZE](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order).
6. **C** — Watermark delay; see [Stream Analytics monitoring](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-monitoring).
7. **B** — [Fabric monitoring hub](https://learn.microsoft.com/en-us/fabric/admin/monitoring-hub).
8. **B** — [Azure alerts overview](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview).
9. **B** — Driver OOM; see [Azure Databricks Spark](https://learn.microsoft.com/en-us/azure/databricks/getting-started/spark/).
10. **B** — [Fabric capacity metrics app](https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app).
