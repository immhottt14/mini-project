WITH total_population AS (
    SELECT
        SUM(population) AS total_population
    FROM {{ ref('dim_population') }}
)
SELECT
    flag AS categorize,
    COUNT(*) AS total_country,
    SUM(population) AS total_population,
    ROUND(
        SUM(population) / total_population.total_population * 100,
        2
    ) AS percent_population
FROM {{ ref('dim_population') }}
CROSS JOIN total_population
GROUP BY
    flag,
    total_population.total_population
ORDER BY percent_population DESC