from flask import request, url_for, redirect, session
import hashlib

from .UserHandler import UserHandler

from db import connection

class AdminHandler(UserHandler):
    def post(self):
        if session['userType'] != 'admin':
            return redirect(url_for('redirect_page'))

        formType = request.form['formType']

        if formType == 'Add Student': # feature 2
            username      = request.form['username']
            password      = request.form['password']
            name          = request.form['name']
            surname       = request.form['surname']
            email         = request.form['email']
            department_id = request.form['department_id']
            student_id    = request.form['student_id']

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            response = connection.run_query(f"""
            INSERT INTO User(username, password, department_id, name, surname, email)
            VALUES ('{username}','{hashed_password}','{department_id}','{name}','{surname}','{email}');
            """)

            response = connection.run_query(f"""
            INSERT INTO Student(username, student_id, gpa, completed_credits)
            VALUES ('{username}',{student_id},0,0);
            """)            

            session['response'] = self.generate_form_response("Student Added. You can control the current users in the system from R5.", request.form)

        elif formType == 'Add Instructor': # feature 2
            username      = request.form['username']
            password      = request.form['password']
            name          = request.form['name']
            surname       = request.form['surname']
            email         = request.form['email']
            department_id = request.form['department_id']
            title    = request.form['title']

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            response = connection.run_query(f"""
            INSERT INTO User(username, password, department_id, name, surname, email)
            VALUES ('{username}','{hashed_password}','{department_id}','{name}','{surname}','{email}');
            """)

            response = connection.run_query(f"""
            INSERT INTO Instructor(username, title)
            VALUES ('{username}','{title}');
            """)            

            session['response'] = self.generate_form_response("Instructor Added. You can control the current users in the system from R6.", request.form)
        elif formType == 'Delete Student': # feature 3
            
            student_id = request.form['student_id']

            response = connection.run_query(f"""
            DELETE u
            FROM user u
            INNER JOIN student s ON u.username = s.username
            WHERE student_id = {student_id}
            """)

            session['response'] = self.generate_form_response(f"An attempt is made to delete the student with id {student_id}. Please check R5 to visit the current students.", request.form)

        elif formType == 'Update Title': # feature 4
            
            username = request.form['username']
            title = request.form['title']

            response = connection.run_query(f"""
            UPDATE instructor i
            SET i.title = \"{title}\"
            WHERE i.username = \"{username}\"
            """)

            session['response'] = self.generate_form_response("Title Updated. Please check R6 to see the titles of the instructors.", request.form)

        elif formType == 'View All Students': # feature 5
            
            response = connection.run_query("""
            SELECT s.username, name, surname, email, department_id, completed_credits, gpa 
            FROM student s
                INNER JOIN user u ON s.username = u.username
            ORDER BY completed_credits ASC
            """)
            session['response'] = self.draw_table_response("All Students",
                                                           [
                                                               'username',
                                                               'name',
                                                               'surname',
                                                               'email',
                                                               'department_id',
                                                               'completed_credits',
                                                               'GPA'
                                                           ],
                                                           response)

        elif formType == 'View All Instructors': # feature 6

            response = connection.run_query("""
            SELECT i.username, name, surname, email, department_id, title
            FROM instructor i
                INNER JOIN user u ON i.username = u.username
            """)
            session['response'] = self.draw_table_response("All Instructors",
                                                           [
                                                               'username',
                                                               'name',
                                                               'surname',
                                                               'email',
                                                               'department_id',
                                                               'title'
                                                           ],
                                                           response)

        elif formType == 'View Student Grades': # feature 7

            student_id = request.form['student_id']
            
            response = connection.run_query(f"""
            SELECT c.course_id, name, grade
            FROM completed_course cc
                INNER JOIN course c ON cc.course_id = c.course_id
            WHERE student_id = {student_id}
            """)
            session['response'] = self.draw_table_response(f"Grades of student with id {student_id}",
                                                           [
                                                               'course_id', 
                                                               'name',
                                                               'grade'
                                                           ],
                                                           response)
        
        elif formType == 'View Courses of Instructor': # feature 8

            instructor_username = request.form['instructor_id']
            
            response = connection.run_query(f"""
            SELECT  t.course_id, name, r.classroom_id, campus, time_slot
            FROM teaches t
                INNER JOIN course c ON t.course_id = c.course_id
                INNER JOIN reserves r ON t.course_id = r.course_id
                INNER JOIN classroom cr ON r.classroom_id = cr.classroom_id
            WHERE t.username = \"{instructor_username}\"
            """)

            session['response'] = self.draw_table_response(f"Courses given by instructor with username {instructor_username}",
                                                           [
                                                               'course_id',
                                                               'course name',
                                                               'classroom_id',
                                                               'campus',
                                                               'time_slot'
                                                           ],
                                                           response)
        
        elif formType == 'View Course Grade Average': # feature 9

            course_id = request.form['course_id']
            
            response = connection.run_query(f"""
            SELECT cc.course_id, name, AVG(grade)
            FROM completed_course cc
                INNER JOIN course c ON cc.course_id = c.course_id
            WHERE cc.course_id = \"{course_id}\"
            GROUP BY cc.course_id
            """)

            session['response'] = self.draw_table_response(f"Average grade from the course with id {course_id}",
                                                           [
                                                               'course_id',
                                                               'name',
                                                               'average grade'
                                                           ],
                                                           response)

        else:
            session['response'] = f"invalid request: {formType}"
        
        return redirect(url_for('response_page'))
