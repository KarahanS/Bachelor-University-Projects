/* Select Name, Chef and Awarded_Since columns from the Restauran table.
First convert the Awarded_Since to date format and then exract the year information using strftime. Check if Awarded_Since is less than 2000. */
SELECT Name,
       Chef,
       strftime('%Y', date(Awarded_Since)) AS Awarded_Since
FROM Restaurant
WHERE Awarded_Since < 2000
ORDER BY Awarded_Since
