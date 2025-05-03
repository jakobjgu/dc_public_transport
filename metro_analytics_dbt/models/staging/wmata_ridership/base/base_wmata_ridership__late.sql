WITH source AS (
    SELECT
        *
    FROM
        {{ metro_source('late_night') }}
),
renamed AS (
    SELECT
        ent_station,
        ext_station,
        'Late Night' AS ent_time_period,
        'weekday' AS day_type,
        riders_average_weekday_late_night AS riders,
        trip_length
    FROM
        source
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['ent_station', 'ext_station', 'ent_time_period', 'day_type']) }} AS ridership_key,
    *
FROM
    renamed