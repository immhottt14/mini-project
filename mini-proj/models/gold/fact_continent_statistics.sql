SELECT
    continent,
    COUNT(*) total_country,
    SUM(population) total_population,
    SUM(area_km2) total_area,
    AVG(population) avg_population,
    AVG(area_km2) avg_area
FROM {{ ref('dim_country') }}
GROUP BY continent