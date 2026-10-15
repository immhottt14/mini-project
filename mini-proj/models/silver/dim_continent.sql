WITH base AS (
    SELECT DISTINCT continent
    FROM {{ ref('countries') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['continent']) }} AS continent_id,
    continent AS continent_code,
    CASE
        WHEN continent = 'AF' THEN 'Africa'
        WHEN continent = 'AN' THEN 'Antarctica'
        WHEN continent = 'AS' THEN 'Asia'
        WHEN continent = 'EU' THEN 'Europe'
        WHEN continent = 'NA' THEN 'North America'
        WHEN continent = 'OC' THEN 'Oceania'
        WHEN continent = 'SA' THEN 'South America'
        ELSE 'Unknown'
    END AS continent_name
FROM base