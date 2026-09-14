SELECT a.continent, count(b.country) total_country
FROM {{ ref('dim_continent') }} as a
LEFT JOIN {{ ref('dim_country') }} as b ON a.continent = b.continent 
GROUP BY a.continent
ORDER BY 1 ASC