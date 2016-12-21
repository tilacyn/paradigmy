SELECT Country.Name, Country.Population, Country.SurfaceArea FROM City
JOIN Capital ON Capital.CountryCode = Country.Code JOIN Country ON Country.Code = City.CountryCode
WHERE City.Population = (SELECT MAX(City.Population) FROM City WHERE City.CountryCode = Country.Code)
AND City.Id IS NOT Capital.CityId GROUP BY Country.Name
ORDER BY (CAST(Country.Population AS DOUBLE) / CAST (Country.SurfaceArea AS DOUBLE)) DESC, Country.Name;
