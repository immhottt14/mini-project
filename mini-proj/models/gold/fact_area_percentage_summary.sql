WITH total AS (
    SELECT
        SUM(country_area) AS total_area
    FROM {{ ref('dim_area') }}
)
SELECT
    flag,
    COUNT(*) AS total_country,
    SUM(country_area) AS total_area,
    ROUND(
        SUM(country_area)
        / total.total_area * 100,
        2
    ) AS percent_area
FROM {{ ref('dim_area') }}, total
GROUP BY
    flag,
    total.total_area
ORDER BY percent_area DESC