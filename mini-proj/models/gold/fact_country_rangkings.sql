SELECT
    country,
    continent,
    population,
    area_km2,
    RANK() OVER(
      ORDER BY population DESC
    ) AS population_rank,
    RANK() OVER(
      ORDER BY area_km2 DESC
    ) AS area_rank
FROM {{ ref('dim_country') }}