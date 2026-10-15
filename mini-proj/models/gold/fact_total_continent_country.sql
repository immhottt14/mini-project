SELECT a.continent_code, a.continent_name,
 count(b.country) total_country
FROM {{ ref('dim_continent') }} as a
LEFT JOIN {{ ref('dim_country') }} as b ON a.continent_code = b.continent 
GROUP BY a.continent_code, a.continent_name
ORDER BY a.continent_code ASC