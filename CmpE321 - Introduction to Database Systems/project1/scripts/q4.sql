/*Join the Restaurant table with Destination and Cuisine
tables using the inner join method. Also find the restaurant
with the maximum average price. Then choose the rows that
have this maximum average price in their average price
column.

*/
SELECT Destination_Name,
	   Type
FROM Restaurant
	INNER JOIN Destination ON Destination_ID=Country_Region
	INNER JOIN Cuisine ON Cuisine_Type=Cuisine_ID
WHERE Average_Price = (SELECT max(Average_Price)	
					   FROM Restaurant)