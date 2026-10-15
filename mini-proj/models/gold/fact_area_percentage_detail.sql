WITH total_area AS (
    SELECT
        SUM(country_area) AS total_world_area
    FROM {{ ref('dim_area') }}
),
flag_area AS (
    SELECT
        flag,
        SUM(country_area) AS total_flag_area
    FROM {{ ref('dim_area') }}
    GROUP BY flag
)
SELECT
    d.country_id,
    e.country,
    d.flag,
    d.country_area,
    fa.total_flag_area,
    ROUND(
        d.country_area
        / fa.total_flag_area * 100,
        2
    ) AS pct_within_flag,
    ROUND(
        d.country_area
        / ta.total_world_area * 100,
        2
    ) AS pct_global_area
FROM {{ ref('dim_area') }} d
LEFT JOIN flag_area fa
    ON d.flag = fa.flag
LEFT JOIN {{ ref('dim_country') }} e
    ON d.country_id = e.country_id
CROSS JOIN total_area ta