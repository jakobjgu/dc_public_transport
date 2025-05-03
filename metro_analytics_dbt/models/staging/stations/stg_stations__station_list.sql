
WITH source AS (
    SELECT
        *
    FROM
        {{ source('external_source_station_lines', 'station_line_map') }}
),
renamed AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['station_name', 'station_id', 'metroline', 'lat', 'lon']) }} AS station_key,
        station_name,
        station_id,
        metroline,
        lat,
        lon
    FROM
        source
)

SELECT
    *
FROM
    renamed