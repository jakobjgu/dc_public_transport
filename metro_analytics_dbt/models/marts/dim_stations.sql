SELECT DISTINCT
    station_name,
    station_id,
    metroline AS line_name,
    lat,
    lon
FROM
    {{ ref('stg_stations__station_list') }}
ORDER BY
    metroline ASC

