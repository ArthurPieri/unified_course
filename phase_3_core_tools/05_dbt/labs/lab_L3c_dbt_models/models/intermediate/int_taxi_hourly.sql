-- Intermediate: bucket trips to the hour and pre-aggregate per vendor.
-- Materialized as table (see dbt_project.yml models.intermediate block).
-- Pattern reference: ../dataeng/dbt_project/models/intermediate/int_trips_enriched.sql:L1-L52

with trips as (

    select * from {{ ref('stg_taxi_trips') }}

),

hourly as (

    select
        date_trunc('hour', pickup_datetime)  as pickup_hour,
        vendor_id,
        count(*)                             as trip_count,
        sum(total_amount)                    as total_revenue,
        avg(trip_distance)                   as avg_distance
    from trips
    group by 1, 2

)

select * from hourly
