/*Select all fields from Restaurant and Gourmet tables. Instead of using WHERE, use LEFT JOIN
statement to return all records from Restaurant table, and the matching records from Gourmet table.
If a restaurant is more than one gourmet's favourite, it displays the same restaurant more than once. */
SELECT R.*, G.* 
FROM Restaurant R
LEFT JOIN Gourmet G
ON R.Restaurant_ID = G.Favorite_Restaurant 