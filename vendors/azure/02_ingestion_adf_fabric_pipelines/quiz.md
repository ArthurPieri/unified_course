# Module 02 — Quiz (Ingestion)

1. Your team needs to copy data from on-premises SQL Server into ADLS Gen2. Which Integration Runtime do you need?
   - A. Azure IR
   - B. Self-hosted IR
   - C. Azure-SSIS IR
   - D. No IR; Azure IR can reach on-premises resources.

2. Which activity in ADF transforms data?
   - A. Copy Activity
   - B. Lookup Activity
   - C. Mapping Data Flow
   - D. Wait Activity

3. In Fabric Data Factory, the transformation surface that uses Power Query M on Spark compute is called:
   - A. Mapping Data Flow
   - B. Dataflow Gen1
   - C. Dataflow Gen2
   - D. Notebook activity

4. You need a pipeline that runs once per day, processes that day's partition, and backfills missed windows if it falls behind. Which trigger?
   - A. Schedule
   - B. Tumbling window
   - C. Event-based (Storage)
   - D. Manual

5. A watermark-based incremental pipeline has three key activities. In what order?
   - A. Copy → Lookup → Stored Procedure
   - B. Lookup → Copy → Stored Procedure
   - C. Stored Procedure → Copy → Lookup
   - D. Copy → Stored Procedure → Lookup

6. The watermark pipeline fails after Copy but before updating the control table. On the next run:
   - A. Nothing is reprocessed; the pipeline resumes from the next row.
   - B. Some rows are re-copied, so the sink should be idempotent (e.g., `MERGE`).
   - C. The pipeline is permanently broken and must be recreated.
   - D. Only metadata is reprocessed.

7. In Fabric Data Factory, what is the recommended way to connect to an on-premises SQL Server?
   - A. Self-hosted IR
   - B. On-premises data gateway
   - C. ExpressRoute (mandatory)
   - D. Azure IR with private endpoint

8. Which Fabric feature replaces the Synapse/ADF concept of "linked service + external table on ADLS Gen2" for virtualization?
   - A. Dataflow Gen2
   - B. Copy Activity
   - C. OneLake shortcut
   - D. Managed VNet

9. The expression `@concat('bronze/', formatDateTime(utcnow(), 'yyyy/MM/dd'))` is an example of:
   - A. A Spark SQL function.
   - B. ADF / Fabric pipeline dynamic content.
   - C. Power Query M.
   - D. KQL.

10. Which statement about Copy Activity is TRUE?
    - A. It can join two sources.
    - B. It moves data and supports 90+ connectors, column mapping, and fault tolerance, but not transformations.
    - C. It always uses a self-hosted IR.
    - D. It cannot read from Parquet.

---

## Answer key

1. **B** — Self-hosted IR for on-premises sources ([IR concepts](https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime)).
2. **C** — Mapping Data Flow ([Data flows](https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-overview)).
3. **C** — [Dataflow Gen2](https://learn.microsoft.com/en-us/fabric/data-factory/dataflows-gen2-overview).
4. **B** — Tumbling window supports backfill ([Triggers](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipeline-execution-triggers)).
5. **B** — Watermark pattern requires idempotent sink; see [Azure Data Factory incremental copy](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-overview).
6. **B** — At-least-once semantics; design for idempotency. See [Azure Data Factory incremental copy](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-overview).
7. **B** — [On-premises data gateway for Fabric](https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-onprem).
8. **C** — [OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts).
9. **B** — [Expressions and functions](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-expression-language-functions).
10. **B** — [Copy activity](https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-overview).
