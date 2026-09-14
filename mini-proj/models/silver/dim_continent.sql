WITH base AS (
    SELECT DISTINCT continent
    FROM {{ ref('countries') }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['continent']) }} AS id,
    continent
FROM base