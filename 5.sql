SELECT GovernmentForm, SUM(SurfaceArea) AS SumS FROM Country group by GovernmentForm order by SumS DESC LIMIT 1;
