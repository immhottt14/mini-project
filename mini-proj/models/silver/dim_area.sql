SELECT
    cty_pkey as country_id,
    -- cty_cd3 as country_cd, 
    -- country,
    -- capital,
    area_km2 as country_area,
     CASE
        WHEN area_km2 < 1000000 THEN 'SMALL'
        WHEN area_km2 BETWEEN 1000001 AND 5000000 THEN 'MEDIUM'
        WHEN area_km2 BETWEEN 5000001 AND 10000000 THEN 'LARGE'
        ELSE 'XLARGE'
    END AS flag
FROM {{ ref('countries') }}