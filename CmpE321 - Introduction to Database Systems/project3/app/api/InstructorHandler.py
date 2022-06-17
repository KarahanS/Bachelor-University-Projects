from flask import request, url_for, redirect, session
from .UserHandler import UserHandler

from db import connection

# R11 - Done
# R12 - 
# R13 - Done (?)
# R14 - Done
# R15 - Done
# R16 - Done (?)
# R17 - Done (?)


class InstructorHandler(UserHandler):
    def post(self):
        if session['userType'] != 'instructor':
            return redirect(url_for('redirect_page'))

        formType = request.form['formType']
        
        if formType == 'View All Classrooms': #R11            
            time_slot = request.form['time_slot']

            response = connection.run_query(f"""
            SELECT C.*
            FROM Classroom C
            WHERE C.classroom_id NOT IN (SELECT r.classroom_id 
	            FROM reserves r
    	        WHERE r.time_slot = {time_slot})
            """)

            session['response'] = self.draw_table_response(f"Available classrooms at time slot {time_slot}",
                                                           [
                                                               'classroom_id',
                                                               'campus',
                                                               'classroom_capacity'
                                                           ],
                                                           response)

        elif formType == 'Add Course': # R12
            # don't forget to add quota <= capacity check

            course_id = request.form['course_id']
            name = request.form['name']
            credits = request.form['credits']
            classroom_id = request.form['classroom_id']
            time_slot = request.form['time_slot']
            quota = request.form['quota']
            username = session['username']

            connection.run_query(f"""
            INSERT INTO Course(course_id, name, quota, credits)  # no need to make any checks
            SELECT \"{course_id}\", \"{name}\", {quota}, {credits}
            FROM DUAL
            WHERE (SELECT COUNT(1) FROM Reserves R WHERE R.classroom_id= \"{classroom_id}\"  AND R.time_slot = {time_slot}) = 0
            AND (SELECT COUNT(1) FROM Classroom CR WHERE CR.classroom_id = \"{classroom_id}\" ) > 0;
            """)

            connection.run_query(f"""
            INSERT INTO Teaches(username, course_id)  # no need to make any checks
            SELECT \"{username}\", \"{course_id}\"
            FROM DUAL
            WHERE (SELECT COUNT(1) FROM Reserves R WHERE R.classroom_id= \"{classroom_id}\"  AND R.time_slot = {time_slot}) = 0
            AND (SELECT COUNT(1) FROM Classroom CR WHERE CR.classroom_id = \"{classroom_id}\" ) > 0;
            """)

            connection.run_query(f"""
            INSERT INTO Reserves(course_id, classroom_id, time_slot)
            SELECT \"{course_id}\", CR.classroom_id, {time_slot}
            FROM classroom CR where CR.classroom_id = \"{classroom_id}\" 
            AND (SELECT COUNT(1) FROM Reserves R WHERE R.classroom_id= \"{classroom_id}\"  AND R.time_slot = {time_slot})= 0
            AND (SELECT COUNT(1) FROM Classroom CR WHERE CR.classroom_id = \"{classroom_id}\" ) > 0;
            """)


            session['response'] = self.generate_form_response("An attempt is made to add the course with given information. Please refer to R14 to view your courses.", request.form)
        elif formType == 'Add Prerequisite':  #R13
            # instructor should be the lecturer of successor (not necessarily lecturer of prerequisite)
            successor_id = request.form['successor_id']
            prerequisite_id = request.form['prerequisite_id']
            username = session['username']

            connection.run_query(f"""
            INSERT INTO Prerequisite(successor_id, prerequisite_id)
            SELECT \"{successor_id}\", \"{prerequisite_id}\" FROM Course C
	            INNER JOIN Course CC ON CC.Course_id = \"{prerequisite_id}\"
                INNER JOIN Teaches T On T.username = \"{username}\" and T.course_id = C.course_id
                WHERE C.course_id = \"{successor_id}\"
                AND \"{successor_id}\" > \"{prerequisite_id}\"
            """)

            session['response'] = self.generate_form_response(f"""An attempt is made to add Prerequisite relation between the courses 
            \"{successor_id}\" and \"{prerequisite_id}\". Please check R14 to see prerequisites of your courses.""", request.form)
        elif formType == 'View Your Courses':  #R14
            username = session['username']
  

            response = connection.run_query(f"""
            SELECT C.course_id, C.name, R.classroom_id, R.time_slot, C.quota, group_concat(P.prerequisite_id) as prerequisites
            FROM Course C
                INNER JOIN Teaches T on T.username = \"{username}\" AND C.course_id = T.course_id
                INNER JOIN reserves R on R.course_id = T.course_id
                LEFT JOIN prerequisite P on P.successor_id = T.course_id
            GROUP BY C.course_id
            ORDER BY C.course_id 
            """)

            session['response'] = self.draw_table_response(f"Courses given by {username}",
                                                           [
                                                               'course_id',
                                                               'name',
                                                               'classroom_id',
                                                               'time_slot',
                                                               'quota',
                                                               'prerequisite_list'
                                                           ],
                                                           response)
        elif formType == 'View Your Students by Course':  #R15
            # Possible scenario:
            # User attempts to view students from a course of which he is not the instructor.
            # By checking the TEACHES relation, we guarantee that in such an attempt response will be empty.

            instructor = session['username']
            course_id = request.form['course_id']
            response = connection.run_query(f"""
            SELECT U.username, S.student_id, U.email, U.name, U.surname
            FROM User U
                INNER JOIN Student S ON S.username = U.username
                INNER JOIN Teaches T On T.course_id = \"{course_id}\" AND T.username = \"{instructor}\"
                INNER JOIN Enrolls E ON E.student_id = S.student_id AND E.course_id = \"{course_id}\"
            """)
           

            session['response'] = self.draw_table_response(f"Students taking the course {course_id} given by {instructor}",
                                                           [
                                                               'username',
                                                               'student_id',
                                                               'email',
                                                               'name',
                                                               'surname'
                                                           ],
                                                           response)

        elif formType == 'Update Course Name':  # R16
            course_id = request.form['course_id']
            new_course_name = request.form['new_course_name']
            username = session['username']

            response = connection.run_query(f"""
            UPDATE Course C
            INNER JOIN Teaches T
            SET name = \"{new_course_name}\"
            WHERE T.username = \"{username}\" AND
            C.course_id = \"{course_id}\"  AND T.course_id = C.course_id
            """)

            session['response'] = self.generate_form_response(f"""An attempt is made to change the name of the course with id 
            {course_id}. You can check your courses with R14 or all courses in the system with R18.""", request.form)
        elif formType == 'Grade a Student':  #R17
            # some questions in mind:
            # does grading mean that we ended this course?
            # - should we delete this course from added courses of student?
            # - should we delete this course from given courses of instructor?
            # For now, I did the first but not the second.

            course_id = request.form["course_id"]
            student_id = request.form["student_id"]
            grade = request.form["grade"]
            username = session["username"]
            
            response = connection.run_query(f"""
            INSERT INTO Completed_Course(student_id, course_id, grade)
            SELECT \"{student_id}\", \"{course_id}\", {grade} FROM Course C
                INNER JOIN Teaches T 
                INNER JOIN Enrolls E
                WHERE T.username = \"{username}\" AND
                C.course_id =\"{course_id}\"  AND T.course_id = C.course_id
                AND E.course_id = C.course_id AND E.student_id = \"{student_id}\" 
            """)

            delete = connection.run_query(f"""
            DELETE E FROM Enrolls E
                INNER JOIN Teaches T
                WHERE T.username = \"{username}\" AND
                E.student_id =\"{student_id}\"  AND T.course_id =\"{course_id}\" 
                AND E.course_id = T.course_id;            
            """)

            session['response'] = self.generate_form_response(f"""An attempt is made to give student with id \"{student_id}\", grade {grade} from \"{course_id}\". 
            Student must check R20 to see his grade.""", request.form)
        else:  # impossible to reach here
            session['response'] = f"invalid request: {formType}"

        return redirect(url_for('response_page'))