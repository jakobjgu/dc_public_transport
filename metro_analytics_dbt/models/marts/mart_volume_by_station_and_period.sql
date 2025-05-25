with entries as (
  SELECT
    station,
    day_type,
    trip_time,
    average_entries AS avg_station_usage,
    'entries' AS usage_type
  FROM
    {{ ref('mart_entry_volume_by_station_and_period') }}
),

exits as (
  SELECT
    station,
    day_type,
    trip_time,
    average_exits AS avg_station_usage,
    'exits' AS usage_type
    FROM
      {{ ref('mart_exit_volume_by_station_and_period') }}
),

combined_entries_and_exits AS (
  SELECT * FROM entries
  UNION ALL
  SELECT * FROM exits
  ORDER BY station, day_type, trip_time, usage_type
)

SELECT * FROM combined_entries_and_exits