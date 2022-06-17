/* Select all rows that satisfy the condition that their 
Average_Price is in the result of the subquery that returns
the minimum average price using MIN */
SELECT *
FROM Restaurant
WHERE Average_Price = (SELECT MIN(Average_Price)
                       FROM Restaurant)
