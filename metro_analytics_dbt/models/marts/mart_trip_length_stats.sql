SELECT
  ent_time_period as trip_time,
  day_type,
  AVG(trip_length) AS avg_trip_length,
  MAX(trip_length) AS max_trip_length
FROM {{ ref('mart_ridership_enriched') }}
GROUP BY 1, 2