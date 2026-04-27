# Lab L5c: FastAPI Read-Only Endpoint over Trino Gold Tables

## Goal
Build a minimal FastAPI application that serves Gold-layer lakehouse data through a REST API, using Pydantic models for request/response validation and Trino as the query backend. Verify the auto-generated OpenAPI docs match the declared schema.

## Prerequisites
- Phase 3 full-stack or light-profile compose running (Trino accessible at `localhost:8080`)
- Gold-layer tables exist in Trino (from Phase 3 dbt labs, or create a sample below)
- Python 3.11+ with `pip install fastapi uvicorn trino pydantic`

## Setup

If you do not have Gold tables from Phase 3, create a sample:

```sql
-- Run in Trino CLI: trino --server localhost:8080
CREATE SCHEMA IF NOT EXISTS iceberg.gold;
CREATE TABLE iceberg.gold.daily_revenue (
  day DATE,
  pu_location_id INTEGER,
  trip_count BIGINT,
  total_revenue DOUBLE
) WITH (format = 'PARQUET');

INSERT INTO iceberg.gold.daily_revenue VALUES
  (DATE '2024-01-15', 132, 450, 12350.50),
  (DATE '2024-01-15', 138, 380, 10200.75),
  (DATE '2024-01-16', 132, 410, 11800.00),
  (DATE '2024-01-16', 138, 395, 10650.25),
  (DATE '2024-01-17', 132, 425, 12100.00);
```

## Steps

1. **Read and understand `app.py`** in this directory. It defines:
   - A Pydantic `RevenueRow` response model
   - A `RevenueQuery` model for query parameters (date range, location)
   - A `/revenue` GET endpoint that translates parameters into a parameterized Trino query
   - A `/health` endpoint for readiness checks

2. **Start the server:**
   ```bash
   cd phase_5_advanced/07_data_serving/labs/lab_L5c_fastapi_serving
   uvicorn app:app --reload --port 8000
   ```

3. **Test the health endpoint:**
   ```bash
   curl -s http://localhost:8000/health | python -m json.tool
   ```
   Expected: `{"status": "healthy"}`

4. **Query revenue data:**
   ```bash
   curl -s "http://localhost:8000/revenue?start_date=2024-01-15&end_date=2024-01-17" | python -m json.tool
   ```
   Expected: JSON array of revenue rows matching the date range.

5. **Filter by location:**
   ```bash
   curl -s "http://localhost:8000/revenue?start_date=2024-01-15&end_date=2024-01-17&pu_location_id=132" | python -m json.tool
   ```
   Expected: Only rows for location 132.

6. **Check the auto-generated OpenAPI docs:**
   Open `http://localhost:8000/docs` in a browser. Verify:
   - The `/revenue` endpoint shows query parameters with types
   - The response schema matches `RevenueRow`
   - The `/health` endpoint is documented

7. **Test error handling:**
   ```bash
   curl -s "http://localhost:8000/revenue" | python -m json.tool
   ```
   Expected: 422 Validation Error (missing required `start_date` and `end_date`).

## Verify
- [ ] `GET /health` returns `{"status": "healthy"}`
- [ ] `GET /revenue?start_date=...&end_date=...` returns JSON rows from the Gold table
- [ ] Adding `&pu_location_id=132` filters results correctly
- [ ] `GET /docs` shows Swagger UI with correct parameter types and response schema
- [ ] Missing required parameters return a 422 with field-level errors
- [ ] The Pydantic response model in `/docs` matches the actual JSON shape

## Cleanup
```bash
# Stop uvicorn (Ctrl+C)
# Optionally drop the sample table:
# trino --server localhost:8080 -e "DROP TABLE IF EXISTS iceberg.gold.daily_revenue"
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `Connection refused` to Trino | Ensure Phase 3 compose is running: `docker compose ps` |
| `ModuleNotFoundError: trino` | `pip install trino` |
| Empty results from `/revenue` | Check that Gold tables exist and contain data in the queried date range |
| Slow first query | Trino cold-start; subsequent queries are faster |

## Stretch goals
- Add a response cache using `functools.lru_cache` or a Redis sidecar, and measure latency improvement.
- Add API key authentication using FastAPI's `Security` dependency and verify it appears in the OpenAPI spec.
- Add a `GET /revenue/summary` endpoint that returns aggregate stats (total trips, average revenue) and compare its plan in `EXPLAIN` vs. the detail endpoint.

## References
See [`../../references.md`](../../references.md) (module-level).
