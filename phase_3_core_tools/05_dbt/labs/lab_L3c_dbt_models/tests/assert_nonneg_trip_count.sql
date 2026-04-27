-- Singular data test: fails if any fct_taxi_hourly row has a negative trip_count.
-- dbt treats any returned row as a failure.
-- Pattern based on the companion lakehouse project's singular test pattern.

select
    pickup_hour,
    trip_count
from {{ ref('fct_taxi_hourly') }}
where trip_count < 0
