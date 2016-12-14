SELECT Name, (SELECT Rate FROM LiteracyRate WHERE CountryCode = Code ORDER BY Year DESC LIMIT 1) AS LiteracyRate
FROM Country ORDER BY (SELECT Rate FROM LiteracyRate WHERE CountryCode = Code ORDER BY Year DESC LIMIT 1) DESC LIMIT 1;
