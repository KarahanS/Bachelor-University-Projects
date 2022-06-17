/* Take Country_Region from Restaurant, take Destination_Name from 
Destination and count DISTINCT type rows in cuisine table.
Check if Country_Region is same as Destination_ID since it is the foreign key
of restaurant table on destination table.
Also check if Cuisine_Type is same as Cuisine_ID since it is the foreign key of
restaurant on cuisine. */
SELECT R.Country_Region, D.Destination_Name, COUNT(DISTINCT C.Type) AS Cuisine_Count
FROM Restaurant R
	INNER JOIN Destination D on R.Country_Region = D.Destination_ID
	INNER JOIN Cuisine C on R.Cuisine_Type = C.Cuisine_ID
GROUP BY Country_Region
ORDER BY Cuisine_Count 
