# References — 07_metabase

## Metabase docs (metabase.com)

- Introduction: https://www.metabase.com/docs/latest/
- Connecting to databases: https://www.metabase.com/docs/latest/databases/connecting
- Starburst / Trino driver: https://www.metabase.com/data_sources/starburst
- Query builder introduction: https://www.metabase.com/docs/latest/questions/query-builder/introduction
- Writing native SQL: https://www.metabase.com/docs/latest/questions/native-editor/writing-sql
- Models: https://www.metabase.com/docs/latest/data-modeling/models
- Dashboards introduction: https://www.metabase.com/docs/latest/dashboards/introduction
- Dashboard filters: https://www.metabase.com/docs/latest/dashboards/filters
- Caching query results: https://www.metabase.com/docs/latest/configuring-metabase/caching
- Permissions overview: https://www.metabase.com/docs/latest/permissions/introduction
- Data permissions: https://www.metabase.com/docs/latest/permissions/data
- Embedding introduction: https://www.metabase.com/docs/latest/embedding/introduction
- Metabase releases: https://github.com/metabase/metabase/releases

## Trino (upstream database)

- Trino Iceberg connector: https://trino.io/docs/current/connector/iceberg.html
- Trino resource groups: https://trino.io/docs/current/admin/resource-groups.html
- Trino Web UI: https://trino.io/docs/current/admin/web-interface.html

## Sibling-dir sources (cited inline)

- `../../../../dataeng/docker-compose.yml:L170-L189` — Metabase + metabase-db service blocks in the reference compose (profiles: visualization, full).
- `../compose/full-stack/docker-compose.yml:L229-L265` — Metabase + metabase-db blocks in the course stack (depends_on: trino healthy).
- `../00_stack_overview/README.md` — topology, ports, service responsibility table.
- `../02_trino/README.md` — Trino architecture and catalog model (Metabase is a Trino client).
- `../05_dbt/README.md` — the gold models Metabase points at.

## Course-internal

- `../README.md` — Phase 3 phase hub and exit criteria.
- `../references.md` — phase-level aggregator.
- `../../references/sibling_sources.md` — reuse map (grep "metabase").
