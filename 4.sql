SELECT Country.Name, COALESCE(SUM(City.Population >= 1000000), 0) AS Millionniki 
FROM Country LEFT JOIN City ON City.CountryCode = Country.Code
GROUP BY Country.Name ORDER BY Millionniki DESC;
