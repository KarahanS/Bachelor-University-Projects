-- This query drops the tables we have created.
-- The queries are listed with the opposite order
-- of createTables.sql in order to avoid
-- foreign key errors when dropping tables.

DROP TABLE IF EXISTS DBManagers;
DROP TABLE IF EXISTS Reserves;
DROP TABLE IF EXISTS Classroom;
DROP TABLE IF EXISTS Prerequisite;
DROP TABLE IF EXISTS Enrolls;
DROP TABLE IF EXISTS Teaches;
DROP TABLE IF EXISTS Completed_Course;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Instructor;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Department;