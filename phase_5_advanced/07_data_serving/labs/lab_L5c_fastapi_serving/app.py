"""Read-only FastAPI endpoint serving Gold-layer data from Trino."""

from datetime import date

from fastapi import FastAPI, Query
from pydantic import BaseModel
from trino.dbapi import connect

app = FastAPI(title="Lakehouse Gold API", version="0.1.0")

TRINO_HOST = "localhost"
TRINO_PORT = 8080
TRINO_CATALOG = "iceberg"
TRINO_SCHEMA = "gold"


class RevenueRow(BaseModel):
    day: date
    pu_location_id: int
    trip_count: int
    total_revenue: float


def _get_connection():
    return connect(host=TRINO_HOST, port=TRINO_PORT, catalog=TRINO_CATALOG, schema=TRINO_SCHEMA)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/revenue", response_model=list[RevenueRow])
def get_revenue(
    start_date: date = Query(..., description="Start date (inclusive)"),
    end_date: date = Query(..., description="End date (inclusive)"),
    pu_location_id: int | None = Query(None, description="Filter by pickup location ID"),
):
    sql = "SELECT day, pu_location_id, trip_count, total_revenue FROM daily_revenue WHERE day >= ? AND day <= ?"
    params = [start_date, end_date]

    if pu_location_id is not None:
        sql += " AND pu_location_id = ?"
        params.append(pu_location_id)

    sql += " ORDER BY day, pu_location_id"

    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        columns = [desc[0] for desc in cur.description]
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        conn.close()

    return rows
