-- Lab L2b — Generate synthetic data and write it to MinIO as Parquet.
-- Run inside the duckdb CLI AFTER configuring httpfs + s3 settings (see README).

-- 1. Install + load httpfs (idempotent; INSTALL persists, LOAD is per-session).
INSTALL httpfs;
LOAD httpfs;

-- 2. Configure S3 for local MinIO. Path-style is required for MinIO.
SET s3_endpoint='localhost:9000';
SET s3_use_ssl=false;
SET s3_url_style='path';
SET s3_access_key_id='minioadmin';
SET s3_secret_access_key='minioadmin';

-- 3. Build 10,000 synthetic rows via range() CTE and COPY to MinIO as Parquet.
COPY (
    WITH src AS (
        SELECT
            i                                       AS id,
            ('user_' || (i % 500))                  AS user_id,
            (i % 7)                                 AS region_id,
            (random() * 1000)::DOUBLE               AS amount,
            TIMESTAMP '2025-01-01 00:00:00'
              + INTERVAL (i) MINUTE                 AS event_ts
        FROM range(10000) t(i)
    )
    SELECT * FROM src
) TO 's3://lakehouse/events/data.parquet' (FORMAT PARQUET);

-- 4. Read it back directly from s3:// to verify.
SELECT count(*) AS row_count,
       avg(amount) AS avg_amount,
       min(event_ts) AS first_ts,
       max(event_ts) AS last_ts
FROM 's3://lakehouse/events/data.parquet';

-- 5. Stretch: write a partitioned dataset by region_id (one file per region).
COPY (
    WITH src AS (
        SELECT
            i                          AS id,
            (i % 7)                    AS region_id,
            (random() * 1000)::DOUBLE  AS amount
        FROM range(10000) t(i)
    )
    SELECT * FROM src
) TO 's3://lakehouse/events_partitioned'
  (FORMAT PARQUET, PARTITION_BY (region_id), OVERWRITE_OR_IGNORE);

-- 6. Query the partitioned layout with a glob. DuckDB discovers region_id from the path.
SELECT region_id, count(*) AS n, avg(amount) AS avg_amount
FROM 's3://lakehouse/events_partitioned/*/*.parquet'
GROUP BY region_id
ORDER BY region_id;
