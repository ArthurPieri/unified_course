#!/usr/bin/env python3
"""Generate a synthetic NYC Yellow Taxi CSV sample (50 000 rows).

Uses only the Python standard library — no pip dependencies required.

Usage:
    python generate_sample.py
    python generate_sample.py --rows 100000

Output:
    yellow_sample.csv in the same directory as this script.
"""

from __future__ import annotations

import argparse
import csv
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

COLUMNS = [
    "vendor_id",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "pu_location_id",
    "do_location_id",
    "fare_amount",
    "tip_amount",
    "total_amount",
]

PAYMENT_WEIGHTS = [1] * 67 + [2] * 30 + [3] * 2 + [4] * 1  # credit ~67%, cash ~30%


def generate_row(rng: random.Random, base_date: datetime) -> list:
    vendor_id = rng.choice([1, 2])
    day_offset = rng.randint(0, 30)
    hour = rng.choices(range(24), weights=[
        2, 1, 1, 1, 1, 2, 4, 7, 9, 8, 7, 7,
        8, 8, 8, 8, 9, 9, 9, 8, 7, 6, 5, 3,
    ])[0]
    minute = rng.randint(0, 59)
    second = rng.randint(0, 59)
    pickup = base_date + timedelta(days=day_offset, hours=hour, minutes=minute, seconds=second)

    trip_minutes = max(1, int(rng.gauss(15, 10)))
    dropoff = pickup + timedelta(minutes=trip_minutes, seconds=rng.randint(0, 59))

    passenger_count = rng.choices([1, 2, 3, 4, 5, 6], weights=[65, 15, 8, 5, 4, 3])[0]
    trip_distance = round(max(0.1, rng.gauss(3.5, 3.0)), 2)
    pu_location_id = rng.randint(1, 265)
    do_location_id = rng.randint(1, 265)

    fare_amount = round(max(2.50, 2.50 + trip_distance * rng.uniform(2.0, 4.0)), 2)
    tip_amount = round(fare_amount * rng.choice([0, 0, 0.15, 0.18, 0.20, 0.22, 0.25]), 2)
    total_amount = round(fare_amount + tip_amount + rng.uniform(0.50, 3.50), 2)

    return [
        vendor_id,
        pickup.strftime("%Y-%m-%d %H:%M:%S"),
        dropoff.strftime("%Y-%m-%d %H:%M:%S"),
        passenger_count,
        trip_distance,
        pu_location_id,
        do_location_id,
        fare_amount,
        tip_amount,
        total_amount,
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=50_000, help="Number of rows to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    base_date = datetime(2024, 1, 1)
    out_path = Path(__file__).parent / "yellow_sample.csv"

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        for _ in range(args.rows):
            writer.writerow(generate_row(rng, base_date))

    size_mb = os.path.getsize(out_path) / 1e6
    print(f"wrote {args.rows:,} rows to {out_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
