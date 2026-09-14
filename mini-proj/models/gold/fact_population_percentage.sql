WITH total AS (
    SELECT SUM(POPULATION) AS total_population FROM 
    {{ ref('dim_population') }}
)
SELECT
    flag categorize,
    SUM(population) AS total,
    ROUND(SUM(population) / total.total_population * 100, 2) AS percent_population
FROM {{ ref('dim_population') }}, total
GROUP BY flag, total.total_population
ORDER BY percent_population DESC