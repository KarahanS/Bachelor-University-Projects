
-- create departments
INSERT INTO Department(department_id, department_name)
VALUES ('CMPE', 'Computer Engineering'),
('MATH', 'Mathematics'),
('PHIL', 'Philosophy'),
('IE', 'Industrial Engineering');

-- create users 
INSERT INTO User(username, password, department_id, name, surname, email)
VALUES ('berke.argin', 'newyork123', 'MATH', 'Berke', 'Argin', 'berke.argin@simpleboun.edu.tr'),
('niyazi.ulke', 'mypass',  'CMPE', 'Niyazi', 'Ulke',  'ulke@simpleboun.edu.tr'),
('ryan.andrews', 'pass4321',  'PHIL', 'Ryan', 'Andrews',  'andrews@simpleboun.edu.tr'),
('he.gongmin', 'passwordpass',  'IE', 'He', 'Gongmin',  'he.gongmin@simpleboun.edu.tr'),
('carm.galian', 'madrid9897',  'PHIL', 'Carmelita', 'Galiano',  'carm.galian@simpleboun.edu.tr'),
('kron.helene', 'helenepass',  'CMPE', 'Helene', 'Kron',  'kron.helene@boun.edu.tr'),

('faith.hancock', 'faithfaith11',  'MATH', 'Faith', 'Hancock',  'hancock@simpleboun.edu.tr'),
('rosabel.eerk', 'eerkens1984',  'IE', 'Rosabel', 'Eerkens',  'eerk@simpleboun.edu.tr'),
('arzucan.ozgur', 'mypass4321',  'CMPE', 'Arzucan', 'Ozgur',  'arzucan.ozgur@simpleboun.edu.tr'),
('simon.hunt', '123abc',  'PHIL', 'Simon', 'Hunt',  'hunt.simon@simpleboun.edu.tr'),
('sevgi.demir', 'dmrblk1234',  'MATH', 'Sevgi', 'Demirbilek',  'sevgi.demir1@simpleboun.edu.tr'),
('lyuba.boer', 'easypass12',  'PHIL', 'Lyuba', 'Boerio',  'lyub.boerio15@simpleboun.edu.tr'),
('park.ho', 'linkinpark',  'CMPE', 'Park', 'Ho',  'park.ho@simpleboun.edu.tr'),
('nur.ulku', '1nurulku1',  'CMPE', 'Nur', 'Ulku',  'ulku@simpleboun.edu.tr'),
('charles.sutherland', 'princecharles',  'CMPE', 'Charles', 'Sutherland',  'sutherland@simpleboun.edu.tr');

-- create students
INSERT INTO Student(username, student_id)
VALUES ('berke.argin', 16080),
('niyazi.ulke', 17402),
('ryan.andrews', 18321),
('he.gongmin', 19333),
('carm.galian', 19356),
('kron.helene', 20341);


-- create instructor
INSERT INTO Instructor(username, title)
VALUES ('faith.hancock', 'Associate Professor'),
('rosabel.eerk', 'Assistant Professor'),
('arzucan.ozgur', 'Associate Professor'),
('simon.hunt', 'Professor'),
('sevgi.demir', 'Professor'),
('lyuba.boer', 'Assistant Professor'),
('park.ho', 'Professor'),
('nur.ulku', 'Assistant Professor'),
('charles.sutherland', 'Professor');

-- create courses
INSERT INTO Course(course_id, name, quota, credits)
VALUES ('CMPE150', 'Introduction to Computing', 200, 3),
('CMPE250', 'Data Structures and Algorithms', 15, 4),
('CMPE321', 'Introduction to Database Systems', 120, 4),
('CMPE352', 'Fundamentals of Software Engineering', 4, 4),
('CMPE451', 'Project Development in Software Engineering', 120, 4),
('CMPE493', 'Sp. Tp. in Software Engineering', 20, 3),
('MATH101', 'Calculus I', 100, 4),
('MATH102', 'Calculus II', 5, 4),
('IE306', 'Systems Simulation', 100, 3),
('IE310', 'Operations Research', 5, 4),
('PHIL101', 'Introduction to Philosophy', 5, 3),
('PHIL106', 'Philosophical Texts', 105, 3);

-- create completed courses
INSERT INTO Completed_Course(student_id, course_id, grade)
VALUES (16080, 'IE310', 3.5),
(16080, 'CMPE150', 3),
(16080, 'CMPE250', 4),
(16080, 'CMPE493', 3),
(17402, 'CMPE150', 4),
(17402, 'CMPE250', 3.5),
(17402, 'PHIL101', 4),
(19333, 'MATH101', 3.5),
(19333, 'MATH102', 2.5),
(19356, 'MATH101', 3),
(19356, 'PHIL101', 3.5),
(20341, 'CMPE150', 3.5);

-- create teaches
INSERT INTO Teaches(username, course_id)
VALUES ('arzucan.ozgur', 'CMPE150'),
('park.ho', 'CMPE250'),
('arzucan.ozgur', 'CMPE321'),
('nur.ulku', 'CMPE352'),
('charles.sutherland', 'CMPE451'),
('park.ho', 'CMPE493'),
('faith.hancock', 'MATH101'),
('sevgi.demir', 'MATH102'),
('rosabel.eerk', 'IE306'),
('rosabel.eerk', 'IE310'),
('simon.hunt', 'PHIL101'),
('lyuba.boer', 'PHIL106');

-- create enrolls 
INSERT INTO Enrolls(student_id, course_id)
VALUES (16080, 'CMPE321'),
(16080, 'IE306'),
(17402, 'CMPE321'),
(18321, 'PHIL101'),
(19333, 'IE306'),
(19333, 'IE310'),
(19356, 'PHIL106'),
(19356, 'MATH102'),
(20341, 'CMPE250');


-- create prerequisites
INSERT INTO Prerequisite(successor_id, prerequisite_id)
VALUES ('CMPE250', 'CMPE150'),
('CMPE321', 'CMPE250'),
('CMPE451', 'CMPE321'),
('CMPE451', 'CMPE352'),
('MATH102', 'MATH101'),
('PHIL106', 'PHIL101');

-- create classrooms
INSERT INTO Classroom(classroom_id, campus, classroom_capacity)
VALUES('HD201', 'Hisar Campus', 300),
('BMA2', 'North Campus', 200),
('BMA3', 'North Campus', 150),
('TB310', 'South Campus', 100),
('M1171', 'South Campus', 100);

-- create Reservations
INSERT INTO Reserves(course_id, classroom_id, time_slot)
VALUES ('CMPE150', 'HD201', 1),
('CMPE250', 'BMA2', 2),
('CMPE321', 'BMA2', 3),
('CMPE352', 'BMA3', 3),
('CMPE451', 'BMA3', 10),
('CMPE493', 'BMA2', 4),
('MATH101', 'TB310', 1),
('MATH102', 'TB310', 2),
('IE306', 'M1171', 3),
('IE310', 'M1171', 7),
('PHIL101', 'M1171', 10),
('PHIL106', 'HD201', 8);

-- create database managers
INSERT INTO DBManagers(username, password)
VALUES ('manager1', 'managerpass1'),
('manager2', 'managerpass2'),
('manager35', 'managerpass35');

