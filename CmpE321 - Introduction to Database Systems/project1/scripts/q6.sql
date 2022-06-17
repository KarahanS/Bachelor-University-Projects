/*
Apply inner join to Restaurant and Destination tables based on the ID
of the destination. Then group the resulting table based on the 
Country_Region in order to find the number of restaurants in each
Country_Region and save this column as Restaurant_Count. Then order
the table by the Restaurant_Count column in descending order.
*/
SELECT Country_Region,
       Destination_Name,
       COUNT(Country_Region) AS Restaurant_Count
FROM Restaurant
    INNER JOIN Destination ON Destination_ID=Country_Region
GROUP BY Country_Region
ORDER BY Restaurant_Count DESC