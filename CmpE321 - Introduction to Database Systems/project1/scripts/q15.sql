/*
In the subselect statement, we find the Gourmet_ID
values of the gourmets for whom there exists a
restaurant such that:
- Favorite_Cuisine and Travel_Destination requirements
of the gourmet are satisfied
- Average_Budget of the gourmet is higher than or
equal to the Average_Price of the restaurant

Then we use this list of Gourmet_IDs and a CASE WHEN
statement to list the "Feasibilty". This column denotes
whether there is a restaurant feasible for the gourmet.
*/
SELECT Gourmet_ID, 
CASE WHEN (Gourmet_ID IN (SELECT Gourmet_ID
	FROM Gourmet
	INNER JOIN Restaurant 
	ON Favorite_Cuisine=Cuisine_Type 
	AND Travel_Destination=Country_Region
	WHERE Average_Budget>=Average_Price)) THEN 'TRUE' ELSE 'FALSE' END Feasibility
FROM Gourmet