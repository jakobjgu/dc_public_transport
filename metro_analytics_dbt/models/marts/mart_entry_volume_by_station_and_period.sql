SELECT
  ent_station AS station,
  day_type,
  ent_time_period AS trip_time,
  AVG(riders) AS average_entries,
  SUM(riders) AS sum_entries,
  COUNT(*) AS trips_from_this_station,
  AVG(trip_length) AS average_number_of_stops_from_this_station
FROM {{ ref('mart_ridership_enriched') }}
GROUP BY 1, 2, 3
ORDER BY station, day_type, trip_time