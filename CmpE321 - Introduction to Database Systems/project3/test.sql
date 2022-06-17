
-- create departments
INSERT INTO Department(department_id, department_name)
VALUES ('CMPE', 'Computer Engineering'),
('IE', 'Industrial Engineering'),
('MATH', 'Mathematics'),
('PHIL', 'Philosophy'),
('POLS', 'Political Science and International Relations');

-- create users 
INSERT INTO User(username, password, department_id, name, surname, email)
VALUES ('berke.argin', '4a08316c2183e37daae78d0948e7590c9f880f74dc0e0dead221d13604d1ab9e', 'MATH', 'Berke', 'Argin', 'berke.argin@simpleboun.edu.tr'),
('niyazi.ulke', 'ea71c25a7a602246b4c39824b855678894a96f43bb9b71319c39700a1e045222', 'CMPE', 'Niyazi', 'Ulke', 'ulke@simpleboun.edu.tr'),
('ryan.andrews', '766e341c1b4feb65feff7688501fb7ea99377d096cad8c851add335715fa6d6c', 'PHIL', 'Ryan', 'Andrews', 'andrews@simpleboun.edu.tr'),
('he.gongmin', '9379c98db8165036cf2315f548165a19c740d531f9b2e49bafbd82cb46cbfa96', 'IE', 'He', 'Gongmin', 'he.gongmin@simpleboun.edu.tr'),
('carm.galian', 'b765c074377d62ae1399e92ad4ae147e46af048b2908cc247376452382e8c866', 'PHIL', 'Carmelita', 'Galiano', 'carm.galian@simpleboun.edu.tr'),
('kron.helene', 'ffb0051bd5371a72c62c1867f22cfe05cece84e78fe502144c3022aa773201c5', 'CMPE', 'Helene', 'Kron', 'kron.helene@boun.edu.tr'),
('aylin.karakaya', 'c973c0493b6fe94de9d056ba75ddfe41dd0d5940b026904ed19ea069a6f15ae3', 'IE', 'Aylin', 'Karakaya', 'aylin.karakaya@simpleboun.edu.tr'),
('demir.sari', 'a11b7f3acb5aea7e3a63e3bba98f3ef11da5774a7729e70a88f6eb470b3708b8', 'CMPE', 'Demir', 'Sari', 'demir@simpleboun.edu.tr'),
('yeager.eren', 'eccb82647181c36d6b93cb7268c7238eee08fccee280ec8c4d050a46f56e8cc5', 'CMPE', 'Eren', 'Yeager', 'yeager.eren@simpleboun.edu.tr'),
('mikasa.ack', 'fea1cf890bd688dc848a230980e03f79f7f6827f5d1e190cb795a5f12c9f3fa5', 'PHIL', 'Mikasa', 'Ackerman', 'mikasa.ack@simpleboun.edu.tr'),
('mike.knuew', '74f11276b5ca0087b0c419de0e1d802c81d184b9d1349a50c5e1de6507089d18', 'POLS', 'Mike', 'Knuew', 'mike@simpleboun.edu.tr'),

('faith.hancock', '942315084255274fb68283eb839caf63a78c43aea367bc1ac8268ec55ae87356', 'MATH', 'Faith', 'Hancock', 'hancock@simpleboun.edu.tr'),
('rosabel.eerk', 'c4447597a6b28ed8695d78919297d94bc685ff6fa4d370a094dce946ccdcda9b', 'IE', 'Rosabel', 'Eerkens', 'eerk@simpleboun.edu.tr'),
('arzucan.ozgur', 'e527009e7b9ccce6c13a64d7ed797f535f87c7ee25fceab5d028b638e08bd40f', 'CMPE', 'Arzucan', 'Ozgur', 'arzucan.ozgur@simpleboun.edu.tr'),
('simon.hunt', 'dd130a849d7b29e5541b05d2f7f86a4acd4f1ec598c1c9438783f56bc4f0ff80', 'PHIL', 'Simon', 'Hunt', 'hunt.simon@simpleboun.edu.tr'),
('sevgi.demir', 'cf62fbaa96a930d323f586b2aaea35d6104c3ddd2836fff933013c363dc27653', 'MATH', 'Sevgi', 'Demirbilek', 'sevgi.demir1@simpleboun.edu.tr'),
('lyuba.boer', '5beca10c6923aba1605ae1994e23b6e7c61ae423503e796fb45da9247d918d61', 'PHIL', 'Lyuba', 'Boerio', 'lyub.boerio15@simpleboun.edu.tr'),
('park.ho', 'f46daca7eb795765f476243ee233a9c3fa03bd49e71121bb5aebad24a0b5d015', 'CMPE', 'Park', 'Ho', 'park.ho@simpleboun.edu.tr'),
('naz.ozcan', 'ef38da678682f2a09ab968c10ab8098666f48144fef643b78eda3fb05313f514', 'CMPE', 'Naz', 'Ozcan', 'ozcan@simpleboun.edu.tr'),
('charles.sutherland', 'eedebcc23d68ac468b1d5ad2395a83b6cde774f06dbebc7a2d20407715a62b9b', 'CMPE', 'Charles', 'Sutherland', 'sutherland@simpleboun.edu.tr'),
('philip.sonn', 'cbc498b6e8f2c61aae4564d5501df6a170895267ec68dd4e35b234873c6df610', 'POLS', 'Philip', 'Sonn', 'sonn.philip@simpleboun.edu.tr');

-- create students
INSERT INTO Student(username, student_id, gpa, completed_credits)
VALUES ('berke.argin', 16080, 0,0),
('niyazi.ulke', 17402, 0,0),
('ryan.andrews', 18321, 0,0),
('he.gongmin', 19333, 0,0),
('carm.galian', 19356, 0,0),
('kron.helene', 20341, 0,0),
('aylin.karakaya', 20345, 0, 0),
('demir.sari', 21246, 0, 0),
('yeager.eren', 22344, 0, 0),
('mikasa.ack', 23344, 0, 0),
('mike.knuew', 23567, 0, 0);


-- create instructor
INSERT INTO Instructor(username, title)
VALUES ('faith.hancock', 'Associate Professor'),
('rosabel.eerk', 'Assistant Professor'),
('arzucan.ozgur', 'Associate Professor'),
('simon.hunt', 'Professor'),
('sevgi.demir', 'Professor'),
('lyuba.boer', 'Assistant Professor'),
('park.ho', 'Professor'),
('naz.ozcan', 'Assistant Professor'),
('charles.sutherland', 'Professor'),
('philip.sonn', 'Associate Professor');

-- create courses
INSERT INTO Course(course_id, name, quota, credits)
VALUES ('CMPE150', 'Introduction to Computing', 100, 3),
('CMPE250', 'Data Structures and Algorithms', 5, 4),
('CMPE321', 'Introduction to Database Systems', 12, 4),
('CMPE352', 'Fundamentals of Software Engineering', 120, 2),
('CMPE451', 'Project Development in Software Engineering', 120, 2),
('ENG493', 'Sp. Tp. in Software Engineering', 5, 3),
('MATH101', 'Calculus I', 5, 4),
('MATH102', 'Calculus II', 5, 4),
('IE306', 'Systems Simulation', 100, 3),
('IE310', 'Operations Research', 80, 4),
('PHIL101', 'Introduction to Philosophy', 3, 3),
('PHIL106', 'Philosophical Texts', 100, 3),
('POLS101', 'Introduction to Politics', 3, 3);

-- create completed courses
INSERT INTO Completed_Course(student_id, course_id, grade)
VALUES (16080, 'IE310', 3),
(16080, 'CMPE150', 3),
(16080, 'CMPE250', 4),
(16080, 'ENG493', 4),
(17402, 'CMPE150', 4),
(17402, 'CMPE250', 3.5),
(17402, 'PHIL101', 4),
(19333, 'MATH101', 3.5),
(19333, 'MATH102', 2.5),
(19356, 'MATH101', 3),
(19356, 'PHIL101', 4),
(19356, 'POLS101', 2),
(20341, 'CMPE150', 3.5),
(20341, 'ENG493', 3),
(21246, 'CMPE150', 3.5),
(21246, 'CMPE250', 3.5),
(22344, 'CMPE150', 2.5),
(22344, 'CMPE250', 4),
(22344, 'CMPE321', 3),
(22344, 'CMPE352', 1),
(22344, 'MATH101', 3.5),
(22344, 'POLS101', 1.5),
(23344, 'ENG493', 3),
(23344, 'IE306', 3),
(23567, 'POLS101', 2.5);

-- create teaches
INSERT INTO Teaches(username, course_id)
VALUES ('arzucan.ozgur', 'CMPE150'),
('park.ho', 'CMPE250'),
('arzucan.ozgur', 'CMPE321'),
('naz.ozcan', 'CMPE352'),
('charles.sutherland', 'CMPE451'),
('park.ho', 'ENG493'),
('faith.hancock', 'MATH101'),
('sevgi.demir', 'MATH102'),
('rosabel.eerk', 'IE306'),
('rosabel.eerk', 'IE310'),
('simon.hunt', 'PHIL101'),
('lyuba.boer', 'PHIL106'),
('philip.sonn', 'POLS101');

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
(20341, 'CMPE250'),
(21246, 'CMPE321'),
(21246, 'IE306'),
(21246, 'PHIL101'),
(22344, 'CMPE451'),
(22344, 'MATH102'),
(23344, 'CMPE150'),
(23344, 'PHIL101'),
(23344, 'POLS101');


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
VALUES('HD201', 'Hisar Campus', 100),
('BMA2', 'North Campus', 200),
('BMA3', 'North Campus', 150),
('TB310', 'South Campus', 5),
('M1171', 'South Campus', 100),
('HD202', 'Hisar Campus', 140);

-- create Reservations
INSERT INTO Reserves(course_id, classroom_id, time_slot)
VALUES ('CMPE150', 'HD201', 1),
('CMPE250', 'BMA2', 2),
('CMPE321', 'BMA2', 3),
('CMPE352', 'BMA3', 3),
('CMPE451', 'BMA3', 10),
('ENG493', 'BMA2', 4),
('MATH101', 'TB310', 1),
('MATH102', 'TB310', 2),
('IE306', 'M1171', 3),
('IE310', 'M1171', 7),
('PHIL101', 'M1171', 10),
('PHIL106', 'HD201', 8),
('POLS101', 'HD202', 6);

-- create database managers
INSERT INTO DBManagers(username, password)
VALUES ('manager1', 'd06dde9f54c0ad830d055b50a3c2a20a6d427bc6ccb9ae64887558c2f5d0b332'),
('manager2', '38cf16bdc844f4487f776fb507c0b7370ae174b413ea8d68a5d29769c85894f8'),
('manager35', '4de010eb677261986ee747d16e58725b19d02335e02a5e472af9620b9223b6e7'),
('manager4', 'b97873a40f73abedd8d685a7cd5e5f85e4a9cfb83eac26886640a0813850122b');