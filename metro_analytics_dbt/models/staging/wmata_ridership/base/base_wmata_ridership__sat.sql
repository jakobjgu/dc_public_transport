WITH source AS (
    SELECT
        *
    FROM
        {{ metro_source('saturday') }}
),
renamed AS (
    SELECT
        ent_station,
        ext_station,
        ent_time_period,
        'saturday' AS day_type,
        riders_average_saturday AS riders,
        trip_length
    FROM
        source
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['ent_station', 'ext_station', 'ent_time_period', 'day_type']) }} AS ridership_key,
    *
FROM
    renamed