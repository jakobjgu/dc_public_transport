WITH all_data AS (

    SELECT
        *
    FROM
        {{ ref('stg_wmata_ridership__all_days') }}
)

SELECT
    ent_station,
    ext_station,
    ent_time_period,
    day_type,
    riders,
    trip_length
FROM all_data
