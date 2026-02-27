
with countries as (
  SELECT
    -- Top level keys
    country.value:name.common::STRING AS country_name,
    country.value:name.official::STRING AS official_name,
    country.value:area::NUMBER AS area,
    country.value:population::NUMBER AS population,
    country.value:region::STRING AS region,
    country.value:subregion::STRING AS subregion,
    country.value:unMember::BOOLEAN AS un_member,
    country.value:independent::BOOLEAN AS independent,
    country.value:startOfWeek::STRING AS start_of_week,
    
    -- Array keys (getting the first element)
    country.value:capital[0]::STRING AS capital_city,
    country.value:continents[0]::STRING AS continent,
    
    -- Dynamic Currency keys
    currency.key::STRING AS currency_code,
    currency.value:name::STRING AS currency_name,
    currency.value:symbol::STRING AS currency_symbol,
    
    -- Nested IDD keys
    country.value:idd.root::STRING AS idd_root,
    country.value:idd.suffixes[0]::STRING AS idd_suffix
  FROM 
    {{ ref('stg_triplens__countries') }}
    LATERAL FLATTEN(input => PAYLOAD) country,
    LATERAL FLATTEN(input => country.value:currencies) currency;

)


select * from countries