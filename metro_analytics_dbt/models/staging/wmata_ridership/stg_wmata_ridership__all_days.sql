WITH all_ridership AS (
    SELECT
        *
    FROM
        {{ ref('base_wmata_ridership__weekday') }}
    
    UNION ALL

    SELECT
        *
    FROM
        {{ ref('base_wmata_ridership__sat') }}
    
    UNION ALL

    SELECT
        *
    FROM
        {{ ref('base_wmata_ridership__sun') }}
    
    UNION ALL

    SELECT
        *
    FROM
        {{ ref('base_wmata_ridership__late') }}
)

SELECT
    *
FROM
    all_ridership