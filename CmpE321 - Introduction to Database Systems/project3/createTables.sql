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
password VARCHAR(64) NOT NULL,
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
gpa FLOAT,
completed_credits INT,

UNIQUE (student_id),
FOREIGN KEY (username) REFERENCES User(username) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Instructor

CREATE TABLE IF NOT EXISTS  Instructor (
username VARCHAR(100) PRIMARY KEY,
title  VARCHAR(100) NOT NULL,

CHECK
(BINARY title in ('Assistant Professor' , 'Associate Professor', 'Professor' )),
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
grade FLOAT NOT NULL,

PRIMARY KEY(student_id, course_id),
FOREIGN KEY (student_id) REFERENCES Student(student_id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (course_id) REFERENCES Course(course_id) ON UPDATE CASCADE ON DELETE CASCADE
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
password VARCHAR(64) NOT NULL
);


-- DBManagers


DELIMITER $$
CREATE TRIGGER Gpa_update AFTER INSERT ON completed_course
FOR EACH ROW
BEGIN
	UPDATE student s
    SET
		completed_credits = (select sum(credits)
			   FROM completed_course cc
					INNER JOIN course c ON cc.course_id = c.course_id
               where student_id=NEW.student_id),
		gpa = (select sum(grade * credits) / sum(credits)
			   FROM completed_course cc
					INNER JOIN course c ON cc.course_id = c.course_id
               where student_id=NEW.student_id)
    where s.student_id = NEW.student_id;
END$$

DELIMITER $$
CREATE TRIGGER quota_restriction AFTER INSERT ON Reserves
FOR EACH ROW
BEGIN
	DECLARE quota INT;
	DECLARE capacity INT;
	SELECT C.quota into quota from Course C where C.course_id = new.course_id;
    SELECT CR.classroom_capacity into capacity from Classroom CR where CR.classroom_id = new.classroom_id;
    IF quota > capacity THEN
		DELETE FROM Course C WHERE C.course_id = new.course_id; # This will delete all of them (ON CASCADE DELETE)
		# SIGNAL SQLSTATE  '45000' SET MESSAGE_TEXT = 'Quota of the course cannot exceed the classroom capacity.';
    END IF;
END$$

CREATE PROCEDURE filter_course (
F_department_id VARCHAR(100),
F_campus VARCHAR(100),
min_credit INT,
max_credit INT)
SELECT C.course_id
FROM Course C
INNER JOIN Teaches T on T.course_id = C.course_id
INNER JOIN User U on U.username = T.username
INNER JOIN Department D on D.department_id = U.department_id
AND D.department_id = F_department_id
INNER JOIN Reserves R on R.course_id = C.course_id
INNER JOIN Classroom CR on CR.classroom_id = R.classroom_id
AND CR.campus = F_campus
WHERE C.credits >= min_credit AND C.credits <= max_credit
