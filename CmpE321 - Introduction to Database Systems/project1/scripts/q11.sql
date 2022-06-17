/*
In the subselect statement, we find the distinct values
in the Favorite_Restaurant column of the Gourmet table.

Then we apply inner join to Restaurant and Destination
based on Destination_ID. This is done in order to find 
Destination_Name fields for each Restaurant.

We filter the rows of the table that results from the
inner join based on whether their Restaurant_ID is present
in the list of distinct Favorite_Restaurant values we
retrieved with the subselect statement.
*/
SELECT Name,
	   Chef,
	   Destination_Name
FROM Restaurant
	INNER JOIN Destination ON Country_Region=Destination_ID
WHERE Restaurant_ID IN (SELECT DISTINCT Favorite_Restaurant
						FROM Gourmet)