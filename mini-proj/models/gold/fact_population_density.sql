SELECT
    country_id,
    country,
    continent,
    population,
    area_km2,
    ROUND(
        population / NULLIF(area_km2,0),
        2
    ) population_density
FROM {{ ref('dim_country') }}