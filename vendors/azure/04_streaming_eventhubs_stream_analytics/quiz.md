# Module 04 — Quiz (Streaming)

1. You need to "alert if more than 100 events arrive in any 10-minute span." Which window type?
   - A. Tumbling
   - B. Hopping
   - C. Sliding
   - D. Session

2. Tumbling and hopping windows are:
   - A. Event-driven
   - B. Clock-driven
   - C. Always overlapping
   - D. Only available in Spark

3. Which feature archives Event Hubs messages to ADLS Gen2 as Avro files?
   - A. Event Hubs Capture
   - B. Stream Analytics output
   - C. Fabric mirroring
   - D. Dataflow Gen2

4. Two Spark Structured Streaming queries share the same checkpoint directory. What happens?
   - A. Both run fine.
   - B. One or both queries produce incorrect state or fail because checkpoint state is per-query.
   - C. Performance doubles.
   - D. They merge into one stream automatically.

5. Without a watermark, a Spark Structured Streaming windowed aggregation will:
   - A. Work fine.
   - B. Grow state memory unboundedly.
   - C. Emit nothing.
   - D. Switch to micro-batch mode.

6. Which output mode is required for windowed aggregations that must emit before the window closes?
   - A. `append`
   - B. `complete` or `update`
   - C. `snapshot`
   - D. `overwrite`

7. In Fabric Real-Time Intelligence, which item is the ingest+routing surface?
   - A. Eventhouse
   - B. Eventstream
   - C. KQL database
   - D. Activator

8. Two consumers in the same consumer group are reading from the same Event Hubs partition. What happens?
   - A. Both receive every event.
   - B. They round-robin events.
   - C. Only one consumer (the lease holder) processes the partition at a time.
   - D. The hub rejects the second consumer.

9. To make a Stream Analytics job embarrassingly parallel:
   - A. Add more SUs
   - B. Ensure input partitions = query `PARTITION BY` = output partitions
   - C. Use a sliding window
   - D. Disable checkpointing

10. Your streaming job must be idempotent against replays after failure. The recommended sink pattern is:
    - A. Append-only plain Parquet
    - B. Delta Lake `MERGE` on a dedup key
    - C. CSV output
    - D. Blob Storage without any key

---

## Answer key

1. **C** — Sliding (event-driven) captures every 10-min span; `../../../../azure_certified/flashcards/top-33-flashcards.md` Card 3.
2. **B** — Clock-driven; [ASA windowing](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-window-functions).
3. **A** — [Event Hubs Capture](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-overview).
4. **B** — Checkpoints are per-query; `../../../../azure_certified/IMPLEMENTATION-PLAN.md:L483-L487`.
5. **B** — Unbounded state; [Structured Streaming](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/).
6. **B** — `complete` / `update`; `../../../../azure_certified/flashcards/top-33-flashcards.md` Card 10.
7. **B** — [Eventstream](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview).
8. **C** — One lease per partition per consumer group ([Event Hubs features](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-features)).
9. **B** — [ASA parallelization](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-parallelization).
10. **B** — Delta MERGE on dedup key; `../../../../azure_certified/flashcards/top-33-flashcards.md` Card 10.
