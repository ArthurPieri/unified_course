# Lab L4b: PII Masking, Row-Level Access, and Audit Trail in Trino + Iceberg

## Goal
One Iceberg `customers` table; three Trino users (`analyst`, `dpo`, `engineer`) that run the same `SELECT *` and get three different result sets; an `access_audit` table that records every query.

## Prerequisites
- Phase 3 Trino + Iceberg + MinIO stack from `../../../../phase_3_core_tools/compose/light-profile/` running
- `trino` CLI on PATH
- Ability to edit Trino's `etc/` config files and restart the coordinator

## Setup
```bash
cd ../../../../phase_3_core_tools/compose/light-profile
docker compose up -d trino hive-metastore minio
docker compose exec trino trino --server localhost:8080 --catalog iceberg --schema default
```

In Trino, create the table and sample data:
```sql
CREATE SCHEMA IF NOT EXISTS iceberg.sales;

CREATE TABLE iceberg.sales.customers (
  id      BIGINT,
  name    VARCHAR,
  email   VARCHAR,
  ssn     VARCHAR,
  region  VARCHAR
);

INSERT INTO iceberg.sales.customers VALUES
  (1, 'Alice',   'alice@example.com', '111-22-3333', 'analyst'),
  (2, 'Bob',     'bob@example.com',   '222-33-4444', 'analyst'),
  (3, 'Carlos',  'carlos@example.com','333-44-5555', 'dpo'),
  (4, 'Diana',   'diana@example.com', '444-55-6666', 'engineer');

CREATE TABLE iceberg.sales.access_audit (
  ts          TIMESTAMP(6),
  principal   VARCHAR,
  query_text  VARCHAR,
  row_count   BIGINT
);
```

## Steps

1. **Configure file-based access control.** Create `etc/rules.json` on the Trino coordinator:
```json
{
  "tables": [
    {
      "user": "dpo",
      "catalog": "iceberg", "schema": "sales", "table": "customers",
      "privileges": ["SELECT"]
    },
    {
      "user": "engineer",
      "catalog": "iceberg", "schema": "sales", "table": "customers",
      "privileges": ["SELECT"],
      "columns": [
        { "name": "email", "allowed": false },
        { "name": "ssn",   "allowed": false }
      ]
    },
    {
      "user": "analyst",
      "catalog": "iceberg", "schema": "sales", "table": "customers",
      "privileges": ["SELECT"],
      "filter": "region = current_user",
      "columns": [
        { "name": "email", "mask": "to_hex(sha256(to_utf8(email)))" },
        { "name": "ssn",   "mask": "'***-**-' || substr(ssn, 8, 4)" }
      ]
    }
  ]
}
```
Add to `etc/access-control.properties`:
```
access-control.name=file
security.config-file=/etc/trino/rules.json
```
Restart Trino: `docker compose restart trino`.

2. **Run the same query as each user.**
```bash
trino --user dpo      --execute "SELECT * FROM iceberg.sales.customers ORDER BY id"
trino --user analyst  --execute "SELECT * FROM iceberg.sales.customers ORDER BY id"
trino --user engineer --execute "SELECT id, name, region FROM iceberg.sales.customers ORDER BY id"
```
Expected: `dpo` sees 4 rows cleartext; `analyst` sees only rows where `region = 'analyst'` (2 rows) with hashed email and `***-**-3333` style SSN; `engineer` sees all 4 rows but only `id`, `name`, `region`.

3. **Log each query into `access_audit`.** After each SELECT above, run:
```sql
INSERT INTO iceberg.sales.access_audit
VALUES (current_timestamp, current_user,
        'SELECT * FROM iceberg.sales.customers', <row_count>);
```
In practice, wire this through Trino's [event listener SPI](https://trino.io/docs/current/admin/event-listeners-http.html) so it is automatic; for the lab a manual insert is acceptable.

## Verify
- [ ] `SELECT * FROM iceberg.sales.customers` returns a **different** result set for `dpo`, `analyst`, and `engineer`.
- [ ] `analyst` cannot see cleartext email or full SSN in any query.
- [ ] `engineer` receives an error if they try to `SELECT email` from the table.
- [ ] `SELECT * FROM iceberg.sales.access_audit` shows at least three rows, one per principal.

## Cleanup
```sql
DROP TABLE iceberg.sales.customers;
DROP TABLE iceberg.sales.access_audit;
DROP SCHEMA iceberg.sales;
```
```bash
docker compose down
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `Access Denied` for all users | `rules.json` path not mounted into Trino container; check `access-control.properties` |
| Mask applied to wrong user | Rule order — more specific user rules must come before wildcards |
| `analyst` still sees cleartext | Trino not restarted after editing `rules.json` |

## Stretch goals
- Add a row filter on the `dpo` user that excludes test accounts (`name NOT LIKE 'test%'`).
- Wire an HTTP event listener so `access_audit` is populated automatically for every query.
- Add a `dbt` model contract on a downstream model built from `customers` so a schema change fails CI.

## References
See `../../references.md` (module-level).
