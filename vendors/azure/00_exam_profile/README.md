# Module 00 — DP-700 Exam Profile

> Entry point for the Azure branch. Read this before touching any other module so time allocation matches domain weights.

## Learning goals

- State the DP-700 exam code, format, duration, number of questions, passing score, cost, and renewal cadence — each number anchored to a Microsoft source.
- Recite the three DP-700 domains and their weights from memory.
- Map each branch module (01–06) to one or more DP-700 domains.
- Choose a study track (beginner / intermediate / fast-track) based on a self-assessment.
- Identify the prerequisites Microsoft recommends and which are mandatory.

## Exam at a glance

| Field | Value | Source |
|---|---|---|
| Exam code | DP-700 | [Exam DP-700 page](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/) |
| Full title | Implementing Data Engineering Solutions Using Microsoft Fabric | ibid. |
| Credential | Microsoft Certified: Fabric Data Engineer Associate | [Certification page](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/) |
| Question count | ~40–60 (Microsoft does not publish an exact number; varies per delivery) | Exam page |
| Duration | 100 minutes of exam time (total seat time ~130 min with instructions and surveys) | Exam page |
| Question types | Multiple choice, multiple response, drag-and-drop, case studies, build list, active screen, labs may appear | [Exam formats](https://learn.microsoft.com/en-us/credentials/certifications/certification-exams) |
| Passing score | 700 / 1000 (scaled) | Exam page |
| Languages | English (additional languages added over time — see exam page for current list) | Exam page |
| Delivery | Pearson VUE test center or online proctored | Exam page |
| Prerequisite | **None required.** AZ-900 Azure Fundamentals and DP-900 Azure Data Fundamentals are recommended but not mandatory. | [DP-700 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700) |
| Renewal | Free online assessment on Microsoft Learn annually | [Certification renewal](https://learn.microsoft.com/en-us/credentials/certifications/renew-your-microsoft-certification) |

> **Do not hard-code the exam fee.** Pricing is regional and changes; read the current value on the exam page at booking time.

## Domains and weights

Source: [DP-700 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700). Weights are given as ranges by Microsoft; the midpoint is shown for budgeting only.

| # | Domain | Weight | Branch modules |
|---|---|---|---|
| 1 | Implement and manage an analytics solution | 30–35% | 00 (workspace, deployment pipelines, version control), 05 (security/governance), 06 (monitoring hub) |
| 2 | Ingest and transform data | 30–35% | 01 (OneLake/lakehouse storage), 02 (pipelines, Dataflow Gen2, shortcuts, mirroring), 03 (Spark notebooks, T-SQL, KQL transforms), 04 (Eventstream ingest) |
| 3 | Monitor and optimize an analytics solution | 30–35% | 06 (Monitor, Log Analytics, Fabric monitoring hub, performance tuning) |

**Budgeting rule of thumb** (at 120 h total): ~40 h per domain. Domain 2 is the heaviest if you include lab hours; Domain 3 is the most dense in "trivia" (watermark delays, DMVs, KQL for pipeline monitoring).

## Skills measured — headline topics (per study guide)

Domain 1 — Implement and manage an analytics solution:
- Configure Microsoft Fabric workspace settings (capacity, domain, Spark, workspace identity).
- Implement lifecycle management (deployment pipelines, Git integration, database projects).
- Configure security and governance (workspace roles, item permissions, sensitivity labels, row/column/object-level security, dynamic data masking).
- Orchestrate processes (Fabric pipelines, notebooks as activities, scheduling).

Domain 2 — Ingest and transform data:
- Design and implement loading patterns (batch, streaming, CDC, incremental, full).
- Ingest and transform batch data (Spark notebooks, Dataflow Gen2 / Power Query M, T-SQL on Warehouse, stored procedures).
- Ingest and transform streaming data (Eventstream, KQL, Spark Structured Streaming, windowing).

Domain 3 — Monitor and optimize an analytics solution:
- Monitor Fabric items (monitoring hub, refresh, capacity metrics app, Spark history).
- Identify and resolve errors (pipeline run history, notebook logs, Eventstream state, KQL database health).
- Optimize performance (Delta/OneLake small-file compaction, V-Order, partitioning, warehouse statistics, query plans).

## Recommended prep order (11 weeks, standard track)

| Week | Modules | Sibling + MS Learn anchors |
|---|---|---|
| 1 | 00 + start 01 | [ADLS Gen2 introduction](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction) (storage), Fabric overview MS Learn |
| 2 | 01 finish | `labs/01-delta-lake-fundamentals.ipynb`, OneLake docs |
| 3 | 02 | `labs/04-batch-and-pipeline-patterns.md:L7-L450`, Dataflow Gen2 docs |
| 4–5 | 03 | `labs/02-spark-transformations.ipynb`, `labs/06-tsql-exercises.md:L7-L560` |
| 6 | 04 | `labs/03-structured-streaming.ipynb`, Eventstream + KQL docs |
| 7 | 05 | `labs/05-security-monitoring-optimization.md:L11-L750` |
| 8 | 06 | `labs/05-security-monitoring-optimization.md:L750-L2051`, `labs/07-kql-exercises.md` |
| 9 | Review + first Microsoft Learn practice assessment | `../mock_exam_sources.md` |
| 10 | Gap fixes, flashcards | [DP-700 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700) + per-module `quiz.md` files |
| 11 | Second practice assessment, book exam | Exam page |

Fast-track (if you already hold DP-203 skills + current Azure experience): weeks 1–6 compressed to weeks 1–3, then go straight to weeks 9–11. Budget ~50 h.

## Study tracks (self-assess)

Rate yourself 0–3 on: SQL, Python, Spark, Azure portal, data warehousing, lakehouse/medallion.

- **0–6:** Extended track, 140 h. Start with DP-900 learning path before module 01.
- **7–12:** Standard 11-week track (table above), ~110 h.
- **13–18:** Fast-track, 50 h, focus on Fabric-specific deltas (OneLake, Dataflow Gen2, Eventstream, KQL, V-Order, deployment pipelines).

## Common failures

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Over-studying Synapse dedicated pool internals | Confused DP-203 prep material with DP-700 scope | Use DP-700 Study Guide as the only scoping doc; treat Synapse as "migrate-from" context | [DP-700 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700) |
| Skipping Dataflow Gen2 / Power Query M | Not in DP-203 | Week 3 module 02 — Dataflow Gen2 is heavily tested | [Fabric Data Factory docs](https://learn.microsoft.com/en-us/fabric/data-factory/) |
| Ignoring KQL | KQL is both a query engine (Eventhouse) and a monitoring language (Log Analytics) | Study both contexts in modules 04 and 06 | [KQL reference](https://learn.microsoft.com/en-us/kusto/query/) |
| Assuming OneLake is separate storage | OneLake is a logical layer on ADLS Gen2 | Memorize "One copy, OneLake" and shortcut semantics | [OneLake overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview) |

## Labs

| Lab | Goal | Est. time | Link |
|---|---|---|---|
| Set up Fabric trial capacity | Create workspace, enable Fabric, validate OneLake access | 30 m | [MS Learn — start a Fabric trial](https://learn.microsoft.com/en-us/fabric/get-started/fabric-trial) |
| First lakehouse | Create lakehouse, upload file, query with SQL endpoint | 45 m | [MS Learn — create a lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/create-lakehouse) |

## References

See [references.md](./references.md). Quiz in [quiz.md](./quiz.md).

## Checkpoint

- [ ] I can recite the three DP-700 domains and their weights without looking.
- [ ] I have booked (or scheduled a booking date for) DP-700 via Pearson VUE.
- [ ] I have an active Microsoft Fabric trial capacity.
- [ ] I have taken the Microsoft Learn practice assessment at least once as a baseline.
