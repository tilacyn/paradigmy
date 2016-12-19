SELECT City.Name, City.Population AS City_Population, Country.Population AS Country_Population
FROM City JOIN Country ON Country.Code = City.CountryCode
ORDER BY (CAST (City.Population AS DOUBLE) / CAST(Country.Population AS DOUBLE)) DESC LIMIT 20;
