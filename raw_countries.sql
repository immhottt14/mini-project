SELECT 
    UID,
    NAME,
    CAPITAL,
    POPULATION,
    AREA
FROM 
    {{ source('raw', 'raw_countries')}}