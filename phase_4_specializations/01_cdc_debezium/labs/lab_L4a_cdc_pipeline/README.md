# Lab L4a: Postgres → Debezium → Kafka → Iceberg (MERGE)

## Goal
Capture inserts, updates, and deletes from a Postgres table through a Debezium source connector, land them in a Kafka topic, and apply them to an Iceberg table with `MERGE INTO` from Trino — then query Iceberg time-travel to see the history.

## Prerequisites
- Docker + Compose v2, 6 GB free RAM
- Phase 3 module 01 (MinIO + Iceberg + Hive Metastore) running locally OR adapt the compose below
- `curl` and `psql` on the host

## Setup

Compose snippet (pin versions from the vendors page before running):

```yaml
services:
  postgres:
    image: postgres:16-alpine
    command: ["postgres", "-c", "wal_level=logical", "-c", "max_wal_senders=4", "-c", "max_replication_slots=4"]
    environment:
      POSTGRES_USER: debezium
      POSTGRES_PASSWORD: ${PG_PASSWORD:?set PG_PASSWORD}
      POSTGRES_DB: inventory
    ports: ["5432:5432"]
  kafka:
    image: apache/kafka:3.8.0
    environment:
      KAFKA_PROCESS_ROLES: "broker,controller"
      KAFKA_NODE_ID: "1"
      KAFKA_CONTROLLER_QUORUM_VOTERS: "1@kafka:9093"
      KAFKA_LISTENERS: "PLAINTEXT://:9092,CONTROLLER://:9093"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://kafka:9092"
      KAFKA_CONTROLLER_LISTENER_NAMES: "CONTROLLER"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT"
    ports: ["9092:9092"]
  connect:
    image: debezium/connect:2.7
    depends_on: [kafka, postgres]
    environment:
      BOOTSTRAP_SERVERS: "kafka:9092"
      GROUP_ID: "connect-cluster"
      CONFIG_STORAGE_TOPIC: "connect-configs"
      OFFSET_STORAGE_TOPIC: "connect-offsets"
      STATUS_STORAGE_TOPIC: "connect-status"
    ports: ["8083:8083"]
  trino:
    image: trinodb/trino:latest
    ports: ["8080:8080"]
    volumes:
      - ./trino/catalog:/etc/trino/catalog
```

You also need an `iceberg.properties` catalog file pointing at your Hive Metastore + MinIO — reuse the one from Phase 3 module 01.

## Steps

1. Start the stack and prepare the source table.
   ```bash
   docker compose up -d
   psql -h localhost -U debezium -d inventory <<SQL
   CREATE TABLE customers (id INT PRIMARY KEY, name TEXT, email TEXT, pii_ssn TEXT);
   ALTER TABLE customers REPLICA IDENTITY FULL;
   CREATE PUBLICATION dbz_pub FOR TABLE customers;
   INSERT INTO customers VALUES (1,'alice','a@x','111'),(2,'bob','b@x','222');
   SQL
   ```
   `REPLICA IDENTITY FULL` makes the `before` image of updates and deletes complete — required for correct MERGE behavior. Ref: [PG connector — replica identity](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-replica-identity).

2. Register the Debezium source connector via the Kafka Connect REST API.
   ```bash
   curl -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d '{
     "name": "customers-src",
     "config": {
       "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
       "database.hostname": "postgres", "database.port": "5432",
       "database.user": "debezium", "database.password": "'"$PG_PASSWORD"'",
       "database.dbname": "inventory", "topic.prefix": "dbz",
       "plugin.name": "pgoutput", "publication.name": "dbz_pub",
       "table.include.list": "public.customers",
       "transforms": "unwrap",
       "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
       "transforms.unwrap.drop.tombstones": "false"
     }}'
   ```
   Expected: `HTTP 201` and `curl http://localhost:8083/connectors/customers-src/status` shows `state: RUNNING`.

3. Verify events land on Kafka.
   ```bash
   docker exec -it $(docker compose ps -q kafka) \
     /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
     --topic dbz.public.customers --from-beginning --max-messages 2
   ```
   You should see JSON with `id`, `name`, `email`, `pii_ssn` — two `r` snapshot rows.

4. Create the Iceberg target and a staging table in Trino, then `MERGE`.
   ```sql
   CREATE SCHEMA IF NOT EXISTS iceberg.cdc;
   CREATE TABLE iceberg.cdc.customers (id INT, name VARCHAR, email VARCHAR) WITH (format='PARQUET');
   -- load the last batch of events into iceberg.cdc.customers_stage (id, name, email, op)
   MERGE INTO iceberg.cdc.customers t USING iceberg.cdc.customers_stage s ON t.id = s.id
     WHEN MATCHED AND s.op = 'd' THEN DELETE
     WHEN MATCHED THEN UPDATE SET name = s.name, email = s.email
     WHEN NOT MATCHED AND s.op <> 'd' THEN INSERT (id, name, email) VALUES (s.id, s.name, s.email);
   ```
   Ref: [Iceberg MERGE INTO](https://iceberg.apache.org/docs/latest/spark-writes/#merge-into).

5. Exercise the pipeline.
   ```sql
   -- in psql:
   UPDATE customers SET email='alice@new' WHERE id=1;
   DELETE FROM customers WHERE id=2;
   INSERT INTO customers VALUES (3,'carol','c@x','333');
   ```
   Re-run the staging load + MERGE.

## Verify
- [ ] `customers-src` connector reports `state: RUNNING`
- [ ] Kafka topic `dbz.public.customers` contains events for every insert/update/delete
- [ ] `SELECT * FROM iceberg.cdc.customers ORDER BY id` matches the current Postgres state (no row 2, alice has new email, carol present)
- [ ] `SELECT snapshot_id, committed_at FROM iceberg.cdc."customers$snapshots"` shows one snapshot per MERGE
- [ ] `SELECT * FROM iceberg.cdc.customers FOR VERSION AS OF <older snapshot_id>` returns the prior state

## Cleanup
```bash
curl -X DELETE http://localhost:8083/connectors/customers-src
psql -h localhost -U debezium -d inventory -c "SELECT pg_drop_replication_slot('debezium');"
docker compose down -v
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| Connector `FAILED` with `wal_level` error | `ALTER SYSTEM SET wal_level=logical;` then restart Postgres (compose `command:` already does this) |
| No events after `INSERT` | Check `table.include.list` matches `schema.table`; confirm publication exists |
| Updates arrive with `before=null` | Set `REPLICA IDENTITY FULL` on the source table |
| Postgres disk growing | Drop the orphaned replication slot after removing the connector |

## Stretch goals
- Add an SMT that drops the `pii_ssn` column before the record hits Kafka using `ReplaceField$Value` with `exclude: pii_ssn`. Ref: [Kafka Connect transforms](https://kafka.apache.org/documentation/#connect_transforms).
- Swap the manual staging-table load for a Kafka Connect Iceberg sink connector and compare operational cost.

## References
See `../../references.md` (module-level).
