SELECT City.Name FROM
(City JOIN (Capital JOIN Country ON Capital.CountryCode = Country.Code
WHERE Country.Name = 'Malaysia') ON City.Id = Capital.CityId);
