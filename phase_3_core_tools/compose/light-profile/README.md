# Light-profile lakehouse compose (8 GB RAM)

Minimum viable Phase 3 stack for machines that cannot run the full lakehouse. Covers ~80% of Phase 3 learning objectives; what it does **not** cover is called out below.

## What runs

- **MinIO** — object store
- **iceberg-catalog-db** — tiny Postgres used by Trino's JDBC Iceberg catalog
- **Trino** — query engine, handles all reads and writes to Iceberg
- **Dagster** — single-container `dagster dev`, SQLite storage
- **Metabase** — BI frontend, embedded H2 app DB

Everything is on the default bridge network `lakehouse_net_light`.

## Differences from full-stack

| Aspect                | full-stack                           | light-profile                                  |
|-----------------------|--------------------------------------|------------------------------------------------|
| Iceberg catalog       | Hive Metastore (Thrift)              | Trino JDBC catalog (Postgres)                  |
| PySpark               | `spark` service with Iceberg jars    | **Removed** — no Spark at all                  |
| Dagster storage       | Postgres (dagster-db) + 2 containers | SQLite, single `dagster dev` container         |
| Metabase storage      | Postgres (metabase-db)               | Embedded H2 (dev only)                         |
| Total RAM cap         | ~15.75 GB                            | ~6.0 GB                                        |
| Services count        | 10                                   | 5                                              |

### What you lose

- **No PySpark labs.** The 12h Phase 3 PySpark block (`03_pyspark`) cannot run. Use a cloud dev environment (GitHub Codespaces, Gitpod) for those labs, or run them on a borrowed machine. This is stated explicitly in `UNIFIED_COURSE_PLAN.md:L267, L295-L303`.
- **No HMS experience.** You will not see Thrift metastore behaviour, HMS schema init, or JDBC-from-HMS-to-Postgres wiring. Read `01_minio_iceberg_hms` docs but skip the labs that require a live HMS.
- **Metabase on H2 is single-user dev only.** The Metabase docs warn against H2 for anything beyond trial: https://www.metabase.com/docs/latest/installation-and-operation/configuring-application-database. For this profile it is fine because the whole stack is a learning sandbox, but do not carry this pattern to shared environments.

### What still works

- Ingest with dlt into MinIO (raw layer)
- Create Iceberg tables via Trino DDL (JDBC catalog writes metadata to Postgres, data to `s3://lakehouse/`)
- dbt-trino transformations (bronze → silver → gold)
- Dagster orchestrates dlt + dbt runs
- Metabase connects to Trino for dashboards

This covers modules 00, 01 (concepts only), 02, 04, 05, 06, 07. Module 03 (PySpark) is the only hard gap.

## Start

```bash
# reuse the full-stack example; the shared vars are the same
cp ../full-stack/.env.example .env
# add light-profile vars:
echo "ICEBERG_CAT_USER=iceberg"    >> .env
echo "ICEBERG_CAT_PASSWORD=iceberg" >> .env
docker compose up -d
docker compose ps
```

Tear down:

```bash
docker compose down          # keeps volumes
docker compose down -v       # wipes volumes
```

## RAM budget

| Service             | Cap     |
|---------------------|---------|
| MinIO               | 0.75 GB |
| iceberg-catalog-db  | 0.25 GB |
| Trino               | 3.0 GB  |
| Dagster             | 1.0 GB  |
| Metabase            | 1.0 GB  |
| **Total cap**       | **~6.0 GB** |

On an 8 GB laptop expect ~5-6 GB resident with all services idle. Close browser tabs and desktop apps before running Trino-heavy queries.

## When to use this profile

- Laptop has 8 GB RAM
- You want a fast-start stack for SQL-centric work and dbt/Dagster learning
- You will run the PySpark labs elsewhere (Codespaces/Gitpod/cloud VM)

When you later upgrade hardware, switch to `../full-stack/` — Iceberg tables written via Trino's JDBC catalog are **not** automatically readable from an HMS catalog. Plan to recreate tables (or run a migration) when switching.

## References

- Trino Iceberg JDBC catalog: https://trino.io/docs/current/connector/iceberg.html#jdbc-catalog
- Dagster `dagster dev`: https://docs.dagster.io/guides/running-dagster-locally
- Metabase app DB guidance: https://www.metabase.com/docs/latest/installation-and-operation/configuring-application-database
- Light-profile rationale in plan: `../../../UNIFIED_COURSE_PLAN.md:L267`
