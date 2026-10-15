WITH total_population AS (
    SELECT
        SUM(population) AS world_population
    FROM {{ ref('dim_population') }}
),
category_population AS (
    SELECT
        flag,
        SUM(population) AS category_population
    FROM {{ ref('dim_population') }}
    GROUP BY flag
)
SELECT
    p.country_id,
    cty.country,
    p.flag AS categorize,
    p.population,
    cp.category_population,
    ROUND(
        p.population
        / cp.category_population * 100,
        2
    ) AS pct_within_category,
    ROUND(
        p.population
        / tp.world_population * 100,
        2
    ) AS pct_global_population,
    RANK() OVER (
        ORDER BY p.population DESC
    ) AS population_rank_desc,
    RANK() OVER (
        ORDER BY p.population ASC
    ) AS population_rank_asc
FROM {{ ref('dim_population') }} p
LEFT JOIN category_population cp
    ON p.flag = cp.flag
LEFT JOIN {{ ref('dim_country') }} cty
    ON p.country_id = cty.country_id
CROSS JOIN total_population tp