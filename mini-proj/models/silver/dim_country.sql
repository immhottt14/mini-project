SELECT
    cty_pkey as country_id,
    cty_cd3 as country_cd, 
    country,
    capital,
    continent
FROM {{ ref('countries') }}