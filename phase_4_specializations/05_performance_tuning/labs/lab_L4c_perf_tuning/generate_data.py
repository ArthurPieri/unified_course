# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pyarrow>=16",
#   "numpy>=1.26",
# ]
# ///
"""
generate_data.py — deliberately-bad lakehouse dataset.

Writes ~10_000_000 rows of synthetic event data to MinIO at
s3://lakehouse/perf_lab/raw_events/ as ~10_000 tiny Parquet files,
one file per shard, with no partition layout at all.

The badness is on purpose: the companion lab fixes it.

Run:
    uv run python generate_data.py
    uv run python generate_data.py --rows 10000000 --files 10000
    uv run python generate_data.py --skew        # concentrate 90% of rows on 1% of user_ids

Refs:
    https://arrow.apache.org/docs/python/parquet.html
    https://arrow.apache.org/docs/python/dataset.html
    https://min.io/docs/minio/linux/integrations/aws-cli-with-minio.html
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import date, timedelta

import numpy as np
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq


def build_batch(n: int, seed: int, skew: bool) -> pa.Table:
    rng = np.random.default_rng(seed)

    # event_id: monotonically increasing within the batch, offset by seed
    event_id = np.arange(n, dtype=np.int64) + (seed * n)

    # event_date: uniform across 365 days of 2024
    day_offsets = rng.integers(low=0, high=365, size=n, dtype=np.int32)
    base = np.datetime64("2024-01-01", "D")
    event_date = base + day_offsets.astype("timedelta64[D]")

    # user_id: either uniform or heavily skewed
    if skew:
        # 90% of rows come from 1% of user_ids (1..10_000 out of 1..1_000_000)
        hot = rng.integers(low=1, high=10_001, size=int(n * 0.9), dtype=np.int64)
        cold = rng.integers(low=10_001, high=1_000_001, size=n - hot.size, dtype=np.int64)
        user_id = np.concatenate([hot, cold])
        rng.shuffle(user_id)
    else:
        user_id = rng.integers(low=1, high=1_000_001, size=n, dtype=np.int64)

    # amount: log-normal-ish, clipped
    amount = np.round(rng.lognormal(mean=3.0, sigma=0.8, size=n), 2)

    return pa.table(
        {
            "event_id": pa.array(event_id),
            "event_date": pa.array(event_date, type=pa.date32()),
            "user_id": pa.array(user_id),
            "amount": pa.array(amount, type=pa.float64()),
        }
    )


def make_s3_filesystem(
    endpoint: str, access_key: str, secret_key: str, region: str
) -> pafs.S3FileSystem:
    # pyarrow.fs.S3FileSystem supports non-AWS S3 endpoints via `endpoint_override`.
    # Ref: https://arrow.apache.org/docs/python/filesystems.html#s3
    return pafs.S3FileSystem(
        endpoint_override=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        scheme="http",
        region=region,
        allow_bucket_creation=False,
        allow_bucket_deletion=False,
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rows", type=int, default=10_000_000)
    p.add_argument("--files", type=int, default=10_000)
    p.add_argument("--bucket", default=os.environ.get("LAKEHOUSE_BUCKET", "lakehouse"))
    p.add_argument("--prefix", default="perf_lab/raw_events")
    p.add_argument(
        "--endpoint",
        default=os.environ.get("MINIO_ENDPOINT", "localhost:9000"),
        help="MinIO host:port (no scheme)",
    )
    p.add_argument("--access-key", default=os.environ.get("MINIO_ACCESS_KEY", "minioadmin"))
    p.add_argument("--secret-key", default=os.environ.get("MINIO_SECRET_KEY", "minioadmin"))
    p.add_argument("--region", default=os.environ.get("MINIO_REGION", "us-east-1"))
    p.add_argument("--skew", action="store_true", help="concentrate user_id distribution")
    args = p.parse_args()

    if args.rows % args.files != 0:
        print(
            f"warning: rows ({args.rows}) is not divisible by files ({args.files}); "
            "last file will be smaller",
            file=sys.stderr,
        )

    rows_per_file = args.rows // args.files
    target_dir = f"{args.bucket}/{args.prefix}"
    print(
        f"generating {args.rows:,} rows into {args.files:,} files "
        f"(~{rows_per_file:,} rows each) at s3://{target_dir}/"
    )

    fs = make_s3_filesystem(
        endpoint=args.endpoint,
        access_key=args.access_key,
        secret_key=args.secret_key,
        region=args.region,
    )

    t0 = time.time()
    written = 0
    total_bytes = 0

    # One file per shard, written with pyarrow.parquet.write_table for simplicity.
    # This is intentionally not using write_dataset's partitioning — the lab's point
    # is that a flat dump of many tiny files is pathological.
    for i in range(args.files):
        n = rows_per_file if i < args.files - 1 else (args.rows - rows_per_file * i)
        tbl = build_batch(n=n, seed=i, skew=args.skew)
        path = f"{target_dir}/part-{i:05d}.parquet"
        with fs.open_output_stream(path) as sink:
            pq.write_table(tbl, sink, compression="snappy")
        written += n
        # Stat after write to learn the file size for the summary.
        info = fs.get_file_info(path)
        total_bytes += info.size or 0

        if (i + 1) % max(1, args.files // 20) == 0:
            elapsed = time.time() - t0
            rate = written / elapsed if elapsed else 0.0
            print(
                f"  {i + 1:>6}/{args.files} files  "
                f"{written:>12,} rows  "
                f"{rate:>10,.0f} rows/s"
            )

    elapsed = time.time() - t0
    avg_bytes = total_bytes / args.files if args.files else 0
    print(
        f"done: {written:,} rows, {args.files:,} files, "
        f"{total_bytes / 1e6:.1f} MB total, "
        f"{avg_bytes / 1024:.1f} KB avg/file, "
        f"{elapsed:.1f}s"
    )
    print(f"location: s3://{target_dir}/")
    print(
        "next: follow labs/lab_L4c_perf_tuning/README.md to register the Iceberg "
        "table, time the slow query, then run `rewrite_data_files` / `optimize`."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
