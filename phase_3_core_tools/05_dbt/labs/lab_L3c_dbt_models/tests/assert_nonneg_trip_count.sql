-- Singular data test: fails if any fct_taxi_hourly row has a negative trip_count.
-- dbt treats any returned row as a failure.
-- Pattern reference: ../dataeng/dbt_project/tests/assert_positive_revenue.sql:L1-L9

select
    pickup_hour,
    trip_count
from {{ ref('fct_taxi_hourly') }}
where trip_count < 0
