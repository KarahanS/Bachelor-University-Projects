/*
Apply inner join to join the Gourmet and
Destination tables based on Destination ID.

Then group the rows by the Travel_Destination
column and filter the results using HAVING. Reason why
HAVING is used instead of WHERE is because WHERE
doesn't work with aggregate functions. We filter out the
Travel_Destination values with which there are less than
2 rows using the HAVING.
*/

SELECT Destination_Name,
	   COUNT(Travel_Destination) AS Gourmet_Count
FROM Gourmet
	INNER JOIN Destination ON Travel_Destination=Destination_ID
GROUP BY Travel_Destination
HAVING count(*)>1