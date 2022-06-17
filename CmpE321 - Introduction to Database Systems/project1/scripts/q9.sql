/*
Create a table by applying inner join to Gourmet,
Restaurant and Destination.

Inner join of restaurant is based on:
- Matching country region
This inner join is done in order to find match gourmets and chefs of restaurants

Inner join of Destination is based on:
- Matching destination ID
This inner join is done in order to find the Destination_Name fields corresponding to each Travel_Destination field

Then we select the rows where the Gourmet_ID is 2 and
the Average_Budget is more than or equal to the Average_Price
or Favorite_Cuisine should match Cuisine_Type of the restaurant.
*/

SELECT Name,
	   Chef,
	   Destination_Name
FROM Gourmet
	INNER JOIN Restaurant ON Travel_Destination=Country_Region
	INNER JOIN Destination ON Travel_Destination=Destination_ID
WHERE Gourmet_ID=2
	  AND (Average_Budget>=Average_Price
		   OR Favorite_Cuisine=Cuisine_Type)