# References — 02_trino

## Local compose and config sources

- `../compose/full-stack/conf/trino/config.properties` — coordinator/worker collocated single-node config.
- `../compose/full-stack/conf/trino/catalog/iceberg.properties` — Iceberg connector properties with native S3 filesystem against MinIO.
- `../compose/full-stack/docker-compose.yml:L101-L125` — Phase 3 Trino service block (image `trinodb/trino:470`, port 8080, HMS dependency).
- `../00_stack_overview/README.md` — topology, port map, S3A configuration pattern reused by the Trino connector.

## Trino — architecture and concepts

- Trino overview and use cases: https://trino.io/docs/current/overview/use-cases.html
- Trino cluster concepts (coordinator, worker, connector, catalog): https://trino.io/docs/current/overview/concepts.html
- Deployment and configuration: https://trino.io/docs/current/installation/deployment.html
- General admin properties: https://trino.io/docs/current/admin/properties-general.html

## Trino — connectors

- Connector catalog (index of all connectors): https://trino.io/docs/current/connector.html
- Iceberg connector: https://trino.io/docs/current/connector/iceberg.html
- Hive connector (for comparison, not used in Phase 3): https://trino.io/docs/current/connector/hive.html
- PostgreSQL connector (federation example): https://trino.io/docs/current/connector/postgresql.html

## Trino — SQL surface

- SQL statement syntax: https://trino.io/docs/current/sql.html
- Functions and operators: https://trino.io/docs/current/functions.html
- `EXPLAIN`: https://trino.io/docs/current/sql/explain.html
- `EXPLAIN ANALYZE`: https://trino.io/docs/current/sql/explain-analyze.html
- `SET SESSION`: https://trino.io/docs/current/sql/set-session.html
- `SHOW CATALOGS` / `SHOW SCHEMAS` / `SHOW TABLES`: https://trino.io/docs/current/sql/show-catalogs.html

## Trino — operations

- Web UI: https://trino.io/docs/current/admin/web-interface.html
- Resource groups: https://trino.io/docs/current/admin/resource-groups.html
- Release notes (version pinning): https://trino.io/docs/current/release.html
- Trino releases on GitHub: https://github.com/trinodb/trino/releases

## Iceberg (engine-side context)

- Iceberg table spec: https://iceberg.apache.org/spec/
- Iceberg Hive catalog: https://iceberg.apache.org/docs/latest/hive/
- Iceberg multi-engine / compatibility matrix: https://iceberg.apache.org/multi-engine-support/

## Ecosystem references used by Phase 3 Trino

- dbt-trino adapter: https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup
- Metabase Trino/Starburst driver: https://www.metabase.com/data_sources/starburst
