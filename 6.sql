SELECT Name, City.Population,
(SELECT Population FROM Country WHERE City.CountryCode = Country.Code) AS Country_Population
FROM City ORDER BY (CAST (City.Population AS DOUBLE) / (SELECT CAST (Country.Population AS DOUBLE) FROM Country WHERE City.CountryCode = Country.Code)) DESC LIMIT 20;