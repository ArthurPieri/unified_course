-- Staging: one-to-one with raw_taxi.yellow_taxi_trips, rename + cast only.
-- Based on the companion lakehouse project's staging pattern.
-- (trimmed to a view for the lab; a production version would be incremental).

with source as (

    select * from {{ source('raw_taxi', 'yellow_taxi_trips') }}

),

renamed as (

    select
        cast(vendorid            as integer)         as vendor_id,
        cast(tpep_pickup_datetime  as timestamp)     as pickup_datetime,
        cast(tpep_dropoff_datetime as timestamp)     as dropoff_datetime,
        cast(passenger_count     as integer)         as passenger_count,
        cast(trip_distance       as double)          as trip_distance,
        cast(fare_amount         as decimal(10, 2))  as fare_amount,
        cast(total_amount        as decimal(10, 2))  as total_amount
    from source
    where tpep_pickup_datetime is not null

)

select * from renamed
