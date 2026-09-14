SELECT
    cty_pkey as country_id,
    -- cty_cd3 as country_cd, 
    -- country,
    -- capital,
    population,
    CASE
        WHEN population < 50000000 THEN 'LOW'
        WHEN population BETWEEN 50000000 AND 250000000 THEN 'MID'
        WHEN population BETWEEN 250000000 AND 500000000 THEN 'HIGH'
        ELSE 'MEGA'
    END AS flag
FROM {{ ref('countries') }}