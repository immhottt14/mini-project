WITH continent_pop AS(
    SELECT
        continent,
        SUM(population) population
    FROM {{ ref('dim_country') }}
    GROUP BY continent
),
total_pop AS(
    SELECT SUM(population) total_pop
    FROM continent_pop
)
SELECT
    continent,
    population,
    ROUND(
       population * 100.0 / total_pop,
       2
    ) population_pct
FROM continent_pop
CROSS JOIN total_pop