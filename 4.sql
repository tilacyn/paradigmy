SELECT Name, (SELECT COUNT (*) FROM City WHERE CountryCode =
Code AND City.Population >= 1000000) AS Millioniki FROM Country ORDER BY Millioniki DESC, Name;
