-- Mart: one row per pickup_hour. Fact grain for BI.
-- Pattern reference: ../dataeng/dbt_project/models/marts/fct_trip_metrics.sql:L1-L31

with hourly as (

    select * from {{ ref('int_taxi_hourly') }}

),

rolled as (

    select
        pickup_hour,
        sum(trip_count)              as trip_count,
        sum(total_revenue)           as total_revenue,
        avg(avg_distance)            as avg_distance
    from hourly
    group by pickup_hour

)

select * from rolled
