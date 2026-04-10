# Module 02: Trino (6h)

> Trino is the interactive SQL front door of the Phase 3 lakehouse. It does not store data — it reads Iceberg tables registered in the Hive Metastore and pushes bytes from MinIO through its own distributed execution engine. This module covers Trino's architecture, the connector/catalog model, the Iceberg connector wiring used in `../compose/full-stack/docker-compose.yml:L101-L125`, and the minimum operational skills (EXPLAIN, Web UI, resource groups, failure triage) you need before the Phase 3 labs hand you a 50-million-row table.

## Learning goals
- Describe Trino's coordinator/worker split and the plugin-based connector model, and explain why Trino is a query engine, not a database.
- Navigate the `catalog.schema.table` namespace and write a single query that joins across two connectors.
- Configure and troubleshoot the Iceberg connector against a Hive Metastore (`iceberg.properties`).
- Read `EXPLAIN` and `EXPLAIN ANALYZE` output well enough to find the scan, the join strategy, and the stage that dominates wall time.
- Locate a running query in the Web UI (`:8080`) and identify the stage with the slowest tasks.
- State the three-line rule for choosing Trino vs Spark for a given workload.

## Prerequisites
- [../00_stack_overview/](../00_stack_overview/) — topology and port map.
- [../01_minio_iceberg_hms/](../01_minio_iceberg_hms/) — MinIO bucket layout and HMS Thrift endpoint.
- [../../phase_1_foundations/05_sql_postgres/](../../phase_1_foundations/05_sql_postgres/) — SELECT, JOIN, CTEs, window functions, `EXPLAIN` reading.

## Reading order
1. This README
2. `../compose/full-stack/docker-compose.yml:L101-L125` (Trino service block)
3. `../../../../dataeng/trino/catalog/iceberg.properties` (sibling catalog config)
4. [quiz.md](quiz.md)

Labs L3a (MinIO + Iceberg + HMS) and L3c (dbt on Trino) exercise Trino end-to-end; no dedicated lab lives in this module.

## Concepts

### Distributed SQL engine, not a database
Trino is a distributed SQL query engine that runs federated analytical queries over external data sources. It owns no storage and no catalog of its own: every table it touches belongs to a *connector* that maps an external system (Iceberg, Hive, Kafka, PostgreSQL, JMX, ...) into Trino's relational model. The coordinator parses and plans the query, schedules stages onto workers, and streams results back; workers read splits from the connector and execute the plan fragments. This is a share-nothing, in-memory, pipelined engine — data flows stage-to-stage without intermediate on-disk shuffles, which is why Trino is tuned for interactive latency and not for long ETL.
Ref: [Trino concepts](https://trino.io/docs/current/overview/concepts.html) · [Trino overview](https://trino.io/docs/current/overview/use-cases.html)

### Coordinator and workers
The coordinator is the single node clients talk to (JDBC, CLI, REST at `:8080`). It holds the query queue, the metadata cache, the resource group rules, and the scheduler. Workers execute tasks — one task per stage per worker — and exchange pages over HTTP. In the Phase 3 single-node compose the `trino` service is both coordinator and worker (`coordinator=true`, `node-scheduler.include-coordinator=true` in `../../../../dataeng/trino/config.properties:L1-L2`); a production cluster would set `coordinator=false` on the worker nodes and point them at the coordinator via `discovery.uri`.
Ref: [Trino cluster concepts](https://trino.io/docs/current/overview/concepts.html#cluster) · [Trino configuration](https://trino.io/docs/current/installation/deployment.html#configuring-trino)

### Connectors and the catalog namespace
Every SQL identifier in Trino is three parts: `catalog.schema.table`. A *catalog* is one instance of one connector, configured by a properties file under `/etc/trino/catalog/<name>.properties`; the filename becomes the catalog name. The Phase 3 stack mounts `./conf/trino/catalog` read-only into the container (`../compose/full-stack/docker-compose.yml:L114`) and ships a single `iceberg` catalog. Because each catalog is just another connector instance, a single query can join a table in `iceberg.silver.trips` with one in `postgres.public.zones` — Trino pushes the scans to each source, pulls rows back, and joins them in its own memory. This is *query federation*, and it is the feature that distinguishes Trino from Spark SQL and from every native database.
Ref: [Trino connectors](https://trino.io/docs/current/connector.html) · [Trino catalogs](https://trino.io/docs/current/overview/concepts.html#catalog)

### The Iceberg connector
The Iceberg connector reads and writes [Apache Iceberg](https://iceberg.apache.org/spec/) tables. It resolves a table by asking a *catalog backend* — Hive Metastore, JDBC, REST, Glue, Nessie, or Snowflake — for the current `metadata.json` location, then reads that JSON to learn the current snapshot, manifest list, and data-file paths. Every query runs against a single snapshot, which is how Iceberg delivers serializable reads without locking. The Phase 3 configuration (`../../../../dataeng/trino/catalog/iceberg.properties:L1-L11`) sets `iceberg.catalog.type=hive_metastore`, `hive.metastore.uri=thrift://hive-metastore:9083`, and the native S3 filesystem (`fs.native-s3.enabled=true`) pointed at MinIO with path-style access — the same S3A pattern documented in `../00_stack_overview/README.md:L100-L111`.
Ref: [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) · [Iceberg Hive catalog](https://iceberg.apache.org/docs/latest/hive/)

### SQL surface and Trino-specific bits
Standard DML (`SELECT`, `JOIN`, `GROUP BY`, CTEs, window functions) is covered in [../../phase_1_foundations/05_sql_postgres/](../../phase_1_foundations/05_sql_postgres/); Trino implements them with minor dialect differences (double-quoted identifiers, `VARCHAR` over `TEXT`, standard `DATE '2024-01-01'` literals). Two things are worth highlighting here. First, Trino has a rich function library — array, map, JSON, URL, geospatial, approximate aggregates (`approx_distinct`, `approx_percentile`) — that labs will lean on. Second, `UNNEST` is the primary tool for exploding arrays and maps back to rows.
Ref: [Trino SQL statement syntax](https://trino.io/docs/current/sql.html) · [Trino functions and operators](https://trino.io/docs/current/functions.html)

### `EXPLAIN` and `EXPLAIN ANALYZE`
`EXPLAIN <query>` returns the logical and distributed plan without running it: you see the plan tree, the estimated row counts, and the exchange boundaries that define stages. `EXPLAIN ANALYZE <query>` runs the query and annotates each plan node with wall time, CPU time, input rows, and output rows — the authoritative view of where a query actually spent its time. For Iceberg scans, the nodes you will recognize are `TableScan` (with pushdown predicates listed), `ScanFilterProject`, `HashJoin` vs `ReplicatedJoin`, and `RemoteExchange` (the network shuffle between stages). Deep performance tuning is deferred to Phase 4; at this stage the goal is to read the plan and name the hot stage.
Ref: [EXPLAIN](https://trino.io/docs/current/sql/explain.html) · [EXPLAIN ANALYZE](https://trino.io/docs/current/sql/explain-analyze.html)

### Web UI at `:8080`
The coordinator serves a web UI at `http://localhost:8080`. The landing page lists running, queued, and finished queries; drilling into a query shows its stages, the per-stage task count, the rows/bytes processed, and the live plan. When a query hangs, the UI is the first place to look: a stage stuck at 0 rows input usually means the connector cannot fetch splits (HMS down, S3 creds wrong); a stage with one task at 100% CPU while the others idle is classic skew.
Ref: [Trino Web UI](https://trino.io/docs/current/admin/web-interface.html)

### Resource groups and queueing
Resource groups are the coordinator-side policy layer for admission control: they define how many queries can run concurrently, how many can queue, and how CPU/memory is shared across user groups. A group is matched against incoming queries by user, source, or client tags via a selector rule file (`resource-groups.json`), then enforced by the coordinator. The Phase 3 single-node compose does not configure resource groups — defaults apply — but you should know the mechanism exists so that when a shared cluster in Phase 5 starts rejecting your dbt run with `QUERY_QUEUE_FULL`, you recognize the cause.
Ref: [Trino resource groups](https://trino.io/docs/current/admin/resource-groups.html)

### Trino vs Spark: three-line rule
Use **Trino** when the workload is interactive, read-mostly, and dominated by SQL over tables that already exist — dashboards, ad-hoc analysis, BI tool backends, dbt `view` or light `table` models. Use **Spark** when the workload is a long batch transform that needs Python/Scala, UDFs, ML, wide shuffles, or writes that rewrite large Iceberg partitions. Both speak Iceberg through the same HMS, so the same table can be written by Spark and read by Trino in the same minute — that is the whole point of the shared catalog.
Ref: [Trino use cases](https://trino.io/docs/current/overview/use-cases.html) · [Iceberg multi-engine](https://iceberg.apache.org/docs/latest/)

## Labs
No dedicated lab. Trino is exercised in:

| Lab | Where | What it does |
|---|---|---|
| `lab_L3a_minio_iceberg_hms` | [../01_minio_iceberg_hms/labs/](../01_minio_iceberg_hms/) | First Trino `CREATE TABLE`, `INSERT`, `SELECT` against Iceberg/HMS/MinIO. |
| `lab_L3c_dbt_trino` | [../05_dbt/labs/](../05_dbt/) | dbt-trino builds bronze/silver/gold Iceberg models through the Trino coordinator. |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `Catalog 'iceberg' does not exist` | Catalog properties file missing from `/etc/trino/catalog/` or misnamed | Confirm the mount in `../compose/full-stack/docker-compose.yml:L114` and that the file is named `<catalog>.properties` | [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) |
| `Failed to connect to HMS` / `Thrift` timeouts | HMS not healthy when Trino tried; HMS URI wrong | Wait for `docker compose ps` to show HMS healthy; verify `hive.metastore.uri=thrift://hive-metastore:9083` | [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) · [Iceberg Hive catalog](https://iceberg.apache.org/docs/latest/hive/) |
| `Access Denied` / `403` on S3 reads | MinIO credentials not exported into the container env | Set `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` in `.env`; confirm `${ENV:...}` expansion in `iceberg.properties` | `../../../../dataeng/trino/catalog/iceberg.properties:L10-L11` |
| Queries hang forever on `:8080` with stages stuck at 0 rows | Split generation is blocked on the connector (HMS or S3) | Check HMS and MinIO logs; open the Web UI stage view for the blocked stage | [Trino Web UI](https://trino.io/docs/current/admin/web-interface.html) |
| `Query exceeded per-node memory limit` | `query.max-memory-per-node` too low for the join | Raise the limit in `config.properties` and restart Trino | [Trino properties reference](https://trino.io/docs/current/admin/properties-general.html) |
| `QUERY_QUEUE_FULL` on a shared cluster | Resource group queue saturated | Wait, or reshape the query; escalate to the group owner to revisit selectors | [Resource groups](https://trino.io/docs/current/admin/resource-groups.html) |
| Session property `SET SESSION iceberg.xyz = ...` rejected | Property name must be `<catalog>.<property>` | Use the catalog-qualified form, e.g. `SET SESSION iceberg.compression_codec = 'ZSTD'` | [Session properties](https://trino.io/docs/current/sql/set-session.html) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Explain, in three sentences, why Trino is a query engine and not a database.
- [ ] Write a query that joins `iceberg.silver.trips` with a table in a second catalog.
- [ ] Point at the line in `iceberg.properties` that tells the connector which HMS to use and which S3 endpoint to talk to.
- [ ] Run `EXPLAIN ANALYZE` on a JOIN and name the stage with the highest wall time.
- [ ] Open the Trino Web UI, find a running query, and identify its slowest task.
- [ ] State the rule for picking Trino vs Spark for a given workload.
