SELECT
    cty_pkey as country_id,
    cty_cd3 as country_cd, 
    country,
    capital,
    continent,
    area_km2,
    population
FROM {{ ref('countries') }}