with
weekdays as (
    SELECT
        ent_station,
        day_type,
        ent_time_period,
        sum(riders) as sum_riders
    FROM {{ ref('mart_ridership_enriched') }}
    WHERE day_type = 'weekday'
        AND ent_time_period <> 'late_night'
    GROUP BY 1,2,3
),
weekends as (
    SELECT
        ent_station,
        ent_time_period,
        sum(riders) as sum_riders
    FROM {{ ref('mart_ridership_enriched') }}
    WHERE day_type IN ('saturday', 'sunday')
        AND ent_time_period <> 'late_night'
    GROUP BY 1,2
),

weekday_weekend_ratio as (
    SELECT
        wd.ent_station as entrance_station,
        wd.ent_time_period as time_of_day,
        wd.sum_riders as weekday_entrances,
        we.sum_riders as weekend_entrances,
        wd.sum_riders / we.sum_riders as weekday_to_weekend_ratio
    FROM weekdays as wd
    LEFT JOIN weekends as we
        ON wd.ent_station = we.ent_station
        AND wd.ent_time_period = we.ent_time_period
    ORDER BY weekday_to_weekend_ratio DESC
)

SELECT * FROM weekday_weekend_ratio