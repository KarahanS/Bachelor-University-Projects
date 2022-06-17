/*
Apply inner join to join the Restaurant and
Cuisine tables based on Cuisine ID.

Then group the rows by the Cuisine_Type column and
find the count of Restaurant_ID values and distinct 
Country_Region values for each Cuisine_Type value.

Order the result by Type in ascending order
*/
SELECT Cuisine_Type,
	   Type,
	   COUNT(Restaurant_ID) AS Restaurant_Count,
	   COUNT(distinct Country_Region) AS Distinct_Country_Region_Count
FROM Restaurant
	INNER JOIN Cuisine ON Cuisine_Type=Cuisine_ID
GROUP BY Cuisine_Type
ORDER BY Type