# Module 04 — Streaming: Event Hubs, Stream Analytics, Fabric Real-Time Intelligence

> DP-700 exam weight: Domain 2 streaming subtopic. Roughly 15–20 hours.

## Learning goals

- Describe Event Hubs architecture (namespace, hub, partition, consumer group, throughput units).
- Choose between Event Hubs, Stream Analytics, Fabric Eventstream, and Spark Structured Streaming for a scenario.
- Explain windowing semantics: tumbling, hopping, sliding, session, snapshot.
- Configure checkpoints and watermarks in Spark Structured Streaming for fault tolerance.
- Describe how Fabric Real-Time Intelligence (Eventstream + Eventhouse/KQL database) replaces Stream Analytics.

## Prerequisites

- `01_storage_adls_fabric/README.md`
- `03_compute_synapse_databricks_fabric/README.md` (for KQL)

## Concepts

### Azure Event Hubs — partitioned message log

Event Hubs is Azure's "Kafka-shaped" ingest service: a namespace hosts one or more event hubs; each hub is split into **partitions** (1–32 on standard tier, up to 2000 on dedicated/premium) that provide parallelism and per-partition ordering. Producers can send with or without a partition key — with a key, events with the same key land on the same partition, preserving ordering. **Throughput Units (TU)** on standard tier or **Processing Units (PU)** on premium define capacity. **Consumer groups** give independent cursors into the same partitions: two apps in different consumer groups can read the same events at different paces; two consumers in the *same* group on the same partition contend for the lease. **Event Hubs Capture** auto-archives to ADLS Gen2 / Blob Storage as Avro files, enabling cheap replay of historical streams.
Ref: [Event Hubs overview](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about) · [Event Hubs features](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-features) · `../../../azure_certified/IMPLEMENTATION-PLAN.md:L451-L465`

### Azure Stream Analytics (legacy) — SQL-like temporal queries

Stream Analytics (ASA) is a fully managed streaming query engine with input–query–output topology, billed in **Streaming Units (SU)**. Inputs: Event Hubs, IoT Hub, Blob/ADLS. Outputs: SQL/Cosmos/Storage/Event Hubs/Power BI. Query language is SQL with temporal extensions: `TIMESTAMP BY` for event-time, windowing functions, `LAG()`, `LAST()`, `LIMIT DURATION`. **Embarrassingly parallel** jobs require `input partitions = query PARTITION BY key = output partitions`.
Ref: [Stream Analytics introduction](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-introduction) · `../../../azure_certified/IMPLEMENTATION-PLAN.md:L352-L470`

### Windowing functions

| Window | Behavior | Trigger | Example |
|---|---|---|---|
| Tumbling | Fixed, non-overlapping, clock-driven | Each interval boundary | Count events every 5 min |
| Hopping | Fixed size, overlapping, clock-driven | Each hop interval | 10-min window, hop every 5 min |
| Sliding | Fixed duration, event-driven | When an event enters/exits | Alert if >100 events in any 10 min |
| Session | Variable; groups events separated by timeout | Gap exceeds threshold | User session analytics |
| Snapshot | Groups events with identical timestamps | Each unique timestamp | Aggregate simultaneous readings |

Clock-driven: tumbling, hopping. Event-driven: sliding, session. The distinction is the single most-tested streaming concept.
Ref: `../../../azure_certified/IMPLEMENTATION-PLAN.md:L355-L370` · `../../../azure_certified/flashcards/top-33-flashcards.md` Card 3 · [ASA windowing](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-window-functions)

### Spark Structured Streaming — transferable to Fabric notebooks

Structured Streaming treats a stream as an unbounded DataFrame. Write via `df.writeStream.format("delta").option("checkpointLocation", "/path/checkpoint").start()`. **Output modes**: `append` (new rows only, default; for windowed aggregations waits until past the watermark), `complete` (rewrite all result rows — only with aggregations), `update` (write changed rows). **Triggers**: `processingTime("10 seconds")`, `once=True` (single batch then stop), `availableNow=True` (catch up to now then stop — preferred for scheduled micro-batch). **Checkpoints** store offsets and aggregation state; they must be unique per query and placed in reliable storage (never local disk). **Watermarks** (`df.withWatermark("eventTime", "10 minutes")`) bound how long the engine waits for late events before finalizing a window — without them, stateful queries grow memory unboundedly.
Ref: [Structured Streaming in Fabric/Databricks](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/) · `../../../azure_certified/labs/03-structured-streaming.ipynb` · `../../../azure_certified/flashcards/top-33-flashcards.md` Card 10

### Fabric Real-Time Intelligence — the DP-700 replacement for ASA

Fabric Real-Time Intelligence bundles three items:
1. **Eventstream** — the ingest and routing surface (Event Hubs, IoT Hub, Kafka, Azure SQL CDC, Sample data) with no-code transformations and multiple destinations (Lakehouse, KQL Database, activator, custom endpoint).
2. **Eventhouse / KQL database** — the storage and query engine; KQL language; low-latency ingestion and analytics.
3. **Activator** — data-driven alerts and actions.

Together they replace the DP-203 combo of Event Hubs + Stream Analytics + Power BI for DP-700 scenarios. Expect questions about routing an Eventstream into both a Lakehouse (for batch/ML) and an Eventhouse (for real-time dashboards) simultaneously.
Ref: [Fabric Real-Time Intelligence](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview) · [Eventstream](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview)

### Replay, idempotency, and at-least-once

Event Hubs is at-least-once. Checkpoints make Spark Structured Streaming resumable across failures, but restarted jobs may re-emit a small window of events after the last committed offset — design sinks to be idempotent (Delta `MERGE` with a dedup key, upsert to SQL with primary key conflict handling). Replaying historical data: read Event Hubs Capture Avro files from ADLS as a batch job, or reset the consumer-group offset / use `startingPosition` / `startingOffsets` in Structured Streaming.
Ref: `../../../azure_certified/IMPLEMENTATION-PLAN.md:L494-L505` · `../../../azure_certified/flashcards/top-33-flashcards.md` Card 10

### Service comparison

| Concept | Legacy Azure | Fabric Real-Time Intelligence |
|---|---|---|
| Ingest | Event Hubs (+ Kafka protocol) | Eventstream (Event Hubs, Kafka, IoT Hub, Sample, Azure SQL CDC, custom endpoint) |
| Stream transforms | Stream Analytics query (SQL-like) | Eventstream no-code events processing + KQL update policies |
| Storage for analytics | Synapse / ADLS + Stream Analytics output | Eventhouse / KQL database |
| Alerts | Action Groups + Logic Apps | Activator (data-driven triggers) |
| Dashboards | Power BI on top of ASA output | Real-time dashboards on KQL database |

## Labs

| Lab | Goal | Est. time | Source |
|---|---|---|---|
| L04.1 Structured Streaming | Read Kafka/Event Hubs, windowed aggregation, Delta sink with checkpoint | 90 m | `../../../azure_certified/labs/03-structured-streaming.ipynb` |
| L04.2 Windowing exercises | Implement tumbling, hopping, sliding, session windows; explain differences | 45 m | `../../../azure_certified/IMPLEMENTATION-PLAN.md:L355-L370` |
| L04.3 Fabric Eventstream | Create an Eventstream, add a sample source, land in a Lakehouse + KQL DB | 60 m | [Fabric Eventstream quickstart](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/create) |
| L04.4 Replay from Capture | Read Event Hubs Capture Avro as a batch DataFrame and reprocess | 45 m | `../../../azure_certified/IMPLEMENTATION-PLAN.md:L495-L501` |

## Common failures

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Memory grows unboundedly on a stateful stream | No watermark on windowed aggregation | Add `withWatermark(eventTime, threshold)` | [Structured Streaming](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/) |
| Duplicate rows after restart | Idempotency not designed into sink | Use Delta `MERGE` on a dedup key, or upsert with PK | `../../../azure_certified/flashcards/top-33-flashcards.md` Card 10 |
| Only 8 partitions of a 32-partition hub processed | Query missing `PARTITION BY` prevents embarrassingly parallel execution | Add `PARTITION BY partitionKey` | `../../../azure_certified/IMPLEMENTATION-PLAN.md:L236-L241` |
| "Alert on >100 events in any 10-min window" using hopping window misses some bursts | Hopping is clock-driven, misses windows that straddle hop boundaries | Switch to sliding window (event-driven) | `../../../azure_certified/flashcards/top-33-flashcards.md` Card 3 |

## References

See [references.md](./references.md). Quiz in [quiz.md](./quiz.md).

## Checkpoint

- [ ] I can draw Event Hubs with producers, partitions, consumer groups, and Capture.
- [ ] I can pick the correct window type for a given business requirement.
- [ ] I can write a Structured Streaming job with a checkpoint and a watermark.
- [ ] I can describe what Eventstream + Eventhouse replace from the legacy Azure streaming stack.
