SELECT City.Name FROM City JOIN Capital ON Capital.CityId = City.Id
JOIN Country ON Capital.CountryCode = Country.Code WHERE Country.Name == 'Malaysia';
