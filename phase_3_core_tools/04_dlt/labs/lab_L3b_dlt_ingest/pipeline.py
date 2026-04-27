"""Lab L3b — dlt pipeline: NYC Yellow Taxi Parquet -> MinIO (filesystem).

Key differences from a production pipeline:
  - pipeline_name is scoped to this lab so state does not collide.
  - Credentials/endpoint come from DESTINATION__FILESYSTEM__* env vars
    (see lab README "Setup"), not from .dlt/config.toml.

Run:
    python pipeline.py --year 2024 --months 1
    python pipeline.py --year 2024 --months 1 2 3
"""

from __future__ import annotations

import argparse
import logging
from typing import Iterator

import dlt
from dlt.sources import incremental
import pyarrow as pa
import pyarrow.parquet as pq

logger = logging.getLogger(__name__)

BASE_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    "yellow_tripdata_{year}-{month:02d}.parquet"
)
BATCH_SIZE = 100_000


@dlt.resource(
    name="yellow_taxi_trips",
    write_disposition="append",
    schema_contract="evolve",
    columns={
        "tpep_pickup_datetime": {"data_type": "timestamp", "nullable": False},
        "tpep_dropoff_datetime": {"data_type": "timestamp", "nullable": False},
        "passenger_count": {"data_type": "bigint", "nullable": True},
        "trip_distance": {"data_type": "double", "nullable": True},
        "total_amount": {"data_type": "double", "nullable": True},
        "PULocationID": {"data_type": "bigint", "nullable": True},
        "DOLocationID": {"data_type": "bigint", "nullable": True},
    },
)
def yellow_taxi_trips(
    year: int = 2024,
    months: tuple[int, ...] = (1,),
    updated_at: incremental[pa.lib.Timestamp] = dlt.sources.incremental(
        "tpep_pickup_datetime"
    ),
) -> Iterator[pa.Table]:
    """Yield Arrow batches; dlt drops rows <= last-seen cursor value."""
    for month in months:
        url = BASE_URL.format(year=year, month=month)
        logger.info("Reading %s", url)
        try:
            table = pq.read_table(url)
        except Exception:
            logger.exception("Failed to read %s — skipping", url)
            continue
        for offset in range(0, table.num_rows, BATCH_SIZE):
            yield table.slice(offset, BATCH_SIZE)


@dlt.source
def taxi_source(year: int = 2024, months: tuple[int, ...] = (1,)):
    return yellow_taxi_trips(year=year, months=months)


def build_pipeline() -> dlt.Pipeline:
    """Return a configured dlt Pipeline without running it.

    Useful when another tool (e.g. dagster-dlt) needs to own the
    ``pipeline.run()`` call itself.
    """
    return dlt.pipeline(
        pipeline_name="nyc_taxi_lab",
        destination="filesystem",
        dataset_name="yellow_taxi",
    )


def main(year: int, months: tuple[int, ...]) -> None:
    pipeline = build_pipeline()
    load_info = pipeline.run(taxi_source(year=year, months=months))
    print(load_info)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--months", type=int, nargs="+", default=[1])
    args = parser.parse_args()
    main(year=args.year, months=tuple(args.months))
