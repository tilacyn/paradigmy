SELECT Name FROM City WHERE Id = 
(SELECT CityId FROM Capital WHERE CountryCode = 
(SELECT Code FROM Country WHERE Name = 'Malaysia'));
