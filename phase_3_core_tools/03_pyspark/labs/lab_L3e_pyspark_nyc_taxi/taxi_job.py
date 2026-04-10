"""Lab L3e — PySpark NYC Taxi hourly counts → Iceberg.

Reads one NYC Yellow Taxi monthly Parquet file from MinIO via s3a://,
computes per-hour trip counts, and writes the result to the Iceberg table
`lakehouse.nyc.trips_hourly`. Verify from Trino after the run.

Refs:
  - Iceberg Spark writes: https://iceberg.apache.org/docs/1.5.2/spark-writes/
  - PySpark DataFrame API: https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/dataframe.html
  - Submitting Applications: https://spark.apache.org/docs/3.5.3/submitting-applications.html

Catalog + S3A confs are passed on the spark-submit command line — see the
lab README. This script assumes the `lakehouse` catalog is already wired.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

INPUT_PATH = "s3a://lakehouse/raw/yellow_tripdata_2024-01.parquet"
TARGET_TABLE = "lakehouse.nyc.trips_hourly"


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("lab_L3e_pyspark_nyc_taxi")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # Read the monthly Parquet file directly from MinIO.
    trips = spark.read.parquet(INPUT_PATH)
    rows_in = trips.count()
    print(f"Rows read    : {rows_in}")

    # NYC TLC column: tpep_pickup_datetime (timestamp).
    # Truncate to the hour and count trips per bucket.
    hourly = (
        trips
        .withColumn("pickup_hour", F.date_trunc("hour", F.col("tpep_pickup_datetime")))
        .groupBy("pickup_hour")
        .agg(F.count(F.lit(1)).alias("trip_count"))
        .orderBy("pickup_hour")
    )

    # DataFrameWriterV2 — createOrReplace writes a fresh Iceberg table each run.
    # Swap for .append() to accumulate across months.
    (
        hourly.writeTo(TARGET_TABLE)
        .using("iceberg")
        .createOrReplace()
    )

    rows_out = spark.table(TARGET_TABLE).count()
    print(f"Rows written : {rows_out}")
    print(f"Wrote {TARGET_TABLE}")

    spark.stop()


if __name__ == "__main__":
    main()
