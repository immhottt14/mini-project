 SELECT
    {{
        dbt_utils.generate_surrogate_key([
            'iso_alpha2',
            'iso_alpha3',
            'iso_numeric'
        ])
    }} as cty_pkey,
    iso_alpha2 AS cty_cd2,
    iso_alpha3 AS cty_cd3, 
    iso_numeric AS cty_iso,
    COALESCE(NULLIF(TRIM(fips),''), '#N/A') AS fips_cd,
    country,
    COALESCE(NULLIF(TRIM(capital),''), '#N/A') as capital,
    CAST(REPLACE(area_km2, ',', '') AS INTEGER) AS area_km2,
    CAST(REPLACE(population, ',', '') AS INTEGER) AS population,
    continent
FROM 
    {{ source('raw', 'world_countries')}}