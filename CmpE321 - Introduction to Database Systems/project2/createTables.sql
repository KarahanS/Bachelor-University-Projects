-- This script contains the queries for
-- creation of the tables we designed
-- in the Part 1, 2 and 3 of our assignment.

-- Department

CREATE TABLE IF NOT EXISTS Department (
department_id VARCHAR(100) PRIMARY KEY,
department_name VARCHAR(100) NOT NULL,

UNIQUE (department_name)
);

-- User

CREATE TABLE IF NOT EXISTS  User (
username VARCHAR(100) PRIMARY KEY,
password VARCHAR(100) NOT NULL,
department_id VARCHAR(100) NOT NULL,
name VARCHAR(100) NOT NULL,
surname VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL,

FOREIGN KEY (department_id) REFERENCES Department(department_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Student

CREATE TABLE IF NOT EXISTS Student (
username VARCHAR(100) PRIMARY KEY,
student_id INT NOT NULL,

UNIQUE (student_id),
FOREIGN KEY (username) REFERENCES User(username) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Instructor

CREATE TABLE IF NOT EXISTS  Instructor (
username VARCHAR(100) PRIMARY KEY,
title  VARCHAR(100) NOT NULL,

FOREIGN KEY (username) REFERENCES User(username) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Course

CREATE TABLE IF NOT EXISTS  Course (
course_id VARCHAR(100) PRIMARY KEY,
name VARCHAR(100) NOT NULL,
quota INT NOT NULL,
credits INT NOT NULL
);

-- Completed Course

CREATE TABLE IF NOT EXISTS Completed_Course (
student_id INT,
course_id VARCHAR(100),
grade VARCHAR(100) NOT NULL,

PRIMARY KEY(student_id, course_id),
FOREIGN KEY (student_id) REFERENCES Student(student_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Teaches

CREATE TABLE IF NOT EXISTS  Teaches (
username VARCHAR(100) NOT NULL,
course_id VARCHAR(100) PRIMARY KEY,

FOREIGN KEY (username) REFERENCES Instructor(username) ON UPDATE CASCADE ON DELETE CASCADE, -- If the instructor is removed from the database, then remove the teaches relation as well.
FOREIGN KEY (course_id) REFERENCES Course(course_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Enrolls

CREATE TABLE IF NOT EXISTS Enrolls (
student_id INT,
course_id VARCHAR(100),

PRIMARY KEY(student_id, course_id),
FOREIGN KEY (student_id) REFERENCES Student(student_id) ON UPDATE CASCADE ON DELETE CASCADE, 
FOREIGN KEY (course_id) REFERENCES Course(course_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Prerequisite

CREATE TABLE IF NOT EXISTS Prerequisite (
successor_id VARCHAR(100),
prerequisite_id VARCHAR(100),

PRIMARY KEY(successor_id, prerequisite_id),
FOREIGN KEY (successor_id) REFERENCES Course(course_id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (prerequisite_id) REFERENCES Course(course_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Classroom

CREATE TABLE IF NOT EXISTS Classroom (
classroom_id VARCHAR(100) PRIMARY KEY,
campus VARCHAR(100) NOT NULL,
classroom_capacity INT NOT NULL
);

-- Reserves

CREATE TABLE IF NOT EXISTS Reserves (
course_id VARCHAR(100) NOT NULL,
classroom_id VARCHAR(100),
time_slot INT,

UNIQUE(course_id),
CHECK(0<time_slot AND time_slot<=10), -- only values from 1 to 10 are allowed to be time_slot
PRIMARY KEY(classroom_id, time_slot),
FOREIGN KEY (course_id) REFERENCES Course(course_id) ON UPDATE CASCADE ON DELETE CASCADE, -- If the course is removed from the database, then remove the reserves relation as well.
FOREIGN KEY (classroom_id) REFERENCES Classroom(classroom_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- DBManagers

CREATE TABLE IF NOT EXISTS DBManagers (
username VARCHAR(100) PRIMARY KEY,
password VARCHAR(100) NOT NULL
);