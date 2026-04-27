# Module 07: Metabase — BI frontend (4h)

> The visualization layer of the Phase 3 lakehouse. Metabase sits on top of Trino, exposes a click-through question builder, a SQL editor, and dashboards, and is the service your non-engineer stakeholders actually open. This module is short by design — the heavy concepts live upstream in `02_trino/` and `05_dbt/`, and Metabase is "a BI tool wired to your gold tables" rather than a new compute engine. The service block is pinned at `../compose/full-stack/docker-compose.yml:L245-L265`.

## Learning goals

- Configure Metabase's Trino driver connection (host, port, catalog, schema, user) against the Phase 3 stack.
- Build the same metric three ways — simple question, custom (GUI) question, native SQL — and explain when each is appropriate.
- Save a native SQL question as a **model** with typed columns so downstream questions can treat it like a table.
- Build a dashboard with a filter widget that propagates to every card, and drill through a card back to its underlying question.
- State what Metabase caches, at which level, and how staleness is bounded.
- Read Metabase's permission model at the level of collections, groups, and database access, and name the one failure mode each permission layer guards against.

## Prerequisites

- [../02_trino/](../02_trino/) — you must know what a Trino catalog is, how the `iceberg.silver.trips` identifier resolves, and how to read a simple plan.
- [../05_dbt/](../05_dbt/) — Metabase reads the gold models dbt produces; understanding what "gold" means here is non-negotiable.

## Reading order

1. This README
2. `../compose/full-stack/docker-compose.yml:L245-L265`
3. [quiz.md](quiz.md)

No dedicated lab. Metabase is exercised in the Phase 3 integration exercise: from a running stack, point Metabase at Trino, import a gold table, build one dashboard, and verify the filter drill-through.

## Concepts

### Metabase in one paragraph

Metabase is an open-source BI frontend: a web app you point at one or more databases, and through which users ask questions (return rows), build visualizations (charts), and pin those charts into dashboards. It is not a query engine — every question compiles to SQL and runs on the upstream database, which in our stack is Trino. The app itself stores only its own metadata (users, questions, dashboards, collections, caches) in its own application database — in the course stack that is the `metabase-db` Postgres service. Ref: [Metabase — Introduction](https://www.metabase.com/docs/latest/).

### Adding Trino as a database

The Trino driver ships with the Metabase OSS distribution (previously maintained by Starburst). In the Admin → Databases → Add page, you enter: **host** `trino` (the service name on the `lakehouse_net` bridge), **port** `8080`, **catalog** `iceberg`, **schema** `gold` (or whichever schema exposes your marts), and a **username** used for query attribution and resource-group matching. TLS and authentication are off on the single-node course stack; in production you configure TLS + password or OAuth. Once saved, Metabase scans table metadata and makes the schema browsable in the query builder. Ref: [Metabase — Adding and managing databases](https://www.metabase.com/docs/latest/databases/connecting), [Metabase — Starburst / Trino driver](https://www.metabase.com/data_sources/starburst).

### Three ways to ask a question

A **simple question** is a one-table, one-aggregation shortcut — pick a table, pick a summary (`count`, `sum(amount)`), optionally group by a dimension. It maps to `SELECT dim, agg FROM t GROUP BY dim`. A **custom question** uses the GUI query builder: joins, multi-level filters, custom expressions, and multi-stage aggregations, all still generated as SQL by Metabase. A **native SQL question** is hand-written SQL in the built-in editor, with `{{variable}}` template tags for parameters. Use the GUI when a non-SQL author will maintain the question, and native SQL when the logic needs window functions, CTEs, or Trino-specific functions the builder does not expose. Ref: [Metabase — Asking questions](https://www.metabase.com/docs/latest/questions/query-builder/introduction), [Metabase — The native SQL editor](https://www.metabase.com/docs/latest/questions/native-editor/writing-sql).

### Models

A **model** is a saved question (usually a native SQL one) that other questions can build on as if it were a table. You pick which columns to expose, give each a semantic type (`Category`, `Currency`, `Creation timestamp`, ...), and optionally a display name and description. Downstream simple/custom questions then see the model in the data picker alongside real tables. Models are the Metabase-side place to freeze a contract — the SQL underneath can change, but the exposed columns and types stay stable. Ref: [Metabase — Models](https://www.metabase.com/docs/latest/data-modeling/models).

### Dashboards, filters, drill-through

A dashboard is a grid of cards, each card a question. A **dashboard filter** is a widget (date range, category, text) that is wired to one or more cards by mapping the filter to a field or a native SQL variable; changing the filter re-runs every wired card with the new parameter. **Drill-through** is Metabase's click behaviour on a chart: clicking a bar or a cell opens the underlying question with the clicked dimension added to its filters, letting a user go from "revenue by month" to "the 17 rows behind March" in one click. Ref: [Metabase — Dashboards](https://www.metabase.com/docs/latest/dashboards/introduction), [Metabase — Dashboard filters](https://www.metabase.com/docs/latest/dashboards/filters).

### Caching: question and dashboard

Metabase can cache query results in its application database to reduce load on Trino. Caching is configured at three levels: **instance-wide defaults** (Admin → Performance), **per-database overrides**, and **per-question / per-dashboard overrides**. A cache entry is keyed on the exact rendered SQL plus its parameters, so two questions with different filter values cache independently. Cached results are served until the TTL expires or the cache is invalidated manually; there is no automatic invalidation on upstream data change, so a cached dashboard can show stale data after a dbt build until its TTL rolls over. Ref: [Metabase — Caching query results](https://www.metabase.com/docs/latest/configuring-metabase/caching).

### Permissions at a glance

Metabase's permission model has three layers. **Collections** group questions, dashboards, and models, and each collection grants `view` / `curate` to **groups** of users. **Data permissions** are set per group per database: `Can view` (allowed to query), `No self-service` (only see cards others built), or `Block`. A separate **native query** permission toggles whether a group can write raw SQL against a given database — a classic tightening point, because the GUI builder can be constrained in ways raw SQL cannot. For the lakehouse, the usual setup is: analysts get curate on the "Analytics" collection and native SQL on the `iceberg` database limited to the `gold` schema. Ref: [Metabase — Permissions overview](https://www.metabase.com/docs/latest/permissions/introduction), [Metabase — Data permissions](https://www.metabase.com/docs/latest/permissions/data).

### Embedding

Metabase supports two embedding modes: **public links** (unauthenticated share URLs, off by default) and **signed embedding** where a backend signs a JWT that scopes which dashboard and which parameter values a viewer may access. Embedding is the mechanism used when a dashboard needs to live inside another product's UI. One-line summary; the details are a Phase 5 concern. Ref: [Metabase — Embedding introduction](https://www.metabase.com/docs/latest/embedding/introduction).

### Metabase vs alternatives

Metabase vs Superset vs Looker is a tool-choice question, not a technical one: all three speak SQL to Trino and render charts in a browser. Metabase wins on time-to-first-dashboard and non-engineer usability, Superset on open-source extensibility, and Looker on its modelling layer (LookML). This course standardises on Metabase because it is the fastest to stand up against the course stack; the lakehouse stays usable with any of them.
Ref: [Metabase — Introduction](https://www.metabase.com/docs/latest/).

## Labs

No dedicated module lab. Metabase is used in the Phase 3 integration exercise described in `../README.md` (exit criteria).

## Common failures

| Symptom | Cause | Fix | Source |
|---|---|---|---|
| "Driver not found" when adding a Trino database | Running an old Metabase minor that predates the bundled Trino driver | Upgrade to the pinned `metabase/metabase:v0.51.x` from `../compose/full-stack/docker-compose.yml:L245-L246` | [Metabase releases](https://github.com/metabase/metabase/releases) |
| `Access Denied` on the `iceberg` catalog from Metabase | Wrong `user` on the Trino connection, or resource-group selector blocking the account | Set the connection `user` to one with query rights and re-check the Trino `resource-groups.json` | [Trino resource groups](https://trino.io/docs/current/admin/resource-groups.html) |
| Dashboard still shows yesterday's numbers after dbt runs | Cache TTL has not expired; Metabase does not invalidate on upstream writes | Shorten the cache TTL, or click "Clear cache" on the dashboard; schedule the clear from Dagster | [Metabase — Caching](https://www.metabase.com/docs/latest/configuring-metabase/caching) |
| Analyst can run any SQL against any schema | Native query permission granted instance-wide | Restrict native query permission to the `gold` schema on the `iceberg` database for the analyst group | [Metabase — Data permissions](https://www.metabase.com/docs/latest/permissions/data) |
| Question fails only when saved as a model | Model expects stable column types; a native SQL change introduced `NULL` / type drift | Pin the column types in the model metadata, or fix the SQL to cast explicitly | [Metabase — Models](https://www.metabase.com/docs/latest/data-modeling/models) |

## References

See [references.md](./references.md).

## Checkpoint

Before moving on, you can:

- [ ] Add the Phase 3 Trino service to Metabase with the right host, port, catalog, schema, and user.
- [ ] Build the same metric as a simple question, a custom question, and a native SQL question, and say when each is the right choice.
- [ ] Save a native SQL question as a model with typed columns and use it from a custom question.
- [ ] Build a dashboard with a filter wired to multiple cards and drill through from a chart to the underlying rows.
- [ ] State what Metabase caches and how a stale dashboard can occur after a successful dbt build.
- [ ] Name the three permission layers (collections, data permissions, native query) and one failure each prevents.
