from sqlite3 import connect
from flask import request, url_for, redirect, session
from .UserHandler import UserHandler

from db import connection

# R18 - Done
# R19 - Done
# R20 - Done
# R21 - Done
# R22 - Done

class StudentHandler(UserHandler):
    def post(self):
        if session['userType'] != 'student':
            return redirect(url_for('redirect_page'))

        formType = request.form['formType']
        if formType == 'View All Given Courses': #R18
            response = connection.run_query(f"""
            SELECT C.course_id, C.name, U.surname, D.department_id, C.credits, R.classroom_id, R.time_slot, C.quota, group_concat(P.prerequisite_id) as prerequisites
            FROM Course C
	            INNER JOIN Teaches T on T.course_id = C.course_id
	            INNER JOIN User U on U.username = T.username
                INNER JOIN Department D on U.department_id = D.department_id
	            INNER JOIN reserves R on R.course_id = T.course_id
	        LEFT JOIN prerequisite P on P.successor_id = T.course_id
            GROUP BY C.course_id
            """)
            session['response'] = self.draw_table_response(f"All courses given in this semester",
                                                           [
                                                               'course_id',
                                                               'name',
                                                               'surname',
                                                               'department_id',
                                                               'credits',
                                                               'classroom_id',
                                                               'time_slot',
                                                               'quota',
                                                               'prerequisite list'
                                                           ],
                                                           response)
        elif formType == "Take a Course": #R19
            course_id = request.form["course_id"]
            username = session['username']

            #######
            # 
            # First, I coded up the verbose version with multiple queries.
            # Then I switched to one complicated query version.
            # Advantage of one query format: Condense, short and not ugly like multiple queries
            # Disadvantege of one query format: Not able to return response based on conditions (course was taken before or quota is full etc.)
            #                                   (because we don't know the error although it gives an error at some point)
            #                                   Hard to debug compared to multiple queries
            # ##### 



            
            # student_id = connection.run_query(f"""
            # SELECT S.student_id 
            # FROM Student S
            # WHERE S.username = \"{username}\"
            # """)[0][0]

            # # Conditions must be checked in this order
            # # 1) check if course_id is valid (if there exists a row in Course)
            # # 2) check if course was taken before by the student
            # # 3) check if student meets the prerequisites
            # # 4) check if the quota is full
            # # 5) add the course to the Enrolls table

            # exists = connection.run_query(f"""
            # SELECT COUNT(1)
            # FROM Course
            # WHERE course_id= \"{course_id}\";
            # """)
            # if(exists[0][0] == 0): 
            #     session['response'] = self.generate_form_response("Invalid course ID", request.form)
            # else:
            #     taken = connection.run_query(f"""
            #     SELECT COUNT(1)
            #     FROM Completed_Course CC
            #     WHERE course_id = \"{course_id}\" and student_id =\"{student_id}\";
            #     """)

            #     if(taken[0][0] == 1):
            #         session['response'] = self.generate_form_response("Student has already received a grade from this course.", request.form)
                
            #     else:
            #         prerequisites = connection.run_query(f"""
            #         SELECT(
            #             CASE
	        #                 WHEN 
            #                     (SELECT COUNT(1)  FROM prerequisite P
            #                     INNER JOIN Completed_course CC On CC.course_id = P.prerequisite_id AND CC.student_id =\"{student_id}\" AND P.successor_id = \"{course_id}\")  
			#                     =  (SELECT COUNT(1)  FROM prerequisite P  WHERE P.successor_id = \"{course_id}\") THEN 1
	        #                 ELSE 0
            #             END) as response                    
            #         """)

            #         if(prerequisites[0][0] == 0):
            #             session['response'] = self.generate_form_response("Prerequisites are not taken for this course.", request.form)
                    
            #         else:
            #             quota = connection.run_query(f"""
            #             SELECT (
	        #                 CASE
		    #                     WHEN ( SELECT Count(1) FROM Course C INNER JOIN Enrolls E ON C.course_id =  \"{course_id}\" 
            #                     AND C.quota > (SELECT COUNT(1) FROM Enrolls E WHERE E.course_id = \"{course_id}\") ) THEN 1
		    #                     ELSE 0
	        #                 END) as response 
            #             """)

            #             if(quota[0][0] == 0):
            #                 session['response'] = self.generate_form_response("Quota is full.", request.form)
                        
            #             else:
            #                 response = connection.run_query(f"""
            #                 INSERT INTO Enrolls(student_id, course_id)
            #                 VALUES (\"{student_id}\",  \"{course_id}\");
            #                 """)
            #                 session['response'] = self.generate_form_response("Course Added", request.form)
                    

            response = connection.run_query(f"""
            INSERT INTO Enrolls(student_id, course_id)
            SELECT S.student_id, C.course_id
            FROM Student S 
            INNER JOIN Course C ON C.course_id = \"{course_id}\" # check if it's a valid course
            AND CASE                                              # completed course condition
                WHEN (SELECT COUNT(1)
		            FROM completed_course CC
		            WHERE CC.course_id = \"{course_id}\" and CC.student_id =S.student_id and S.username = \"{username}\") > 0 THEN 0
		        ELSE 1
            END = 1 
            AND CASE                                        # prerequisite condition
                WHEN ( SELECT COUNT(1)
		            FROM Prerequisite P
		            INNER JOIN Completed_course CC On CC.course_id = P.prerequisite_id AND CC.student_id =S.student_id 
                    AND S.username = \"{username}\" AND P.successor_id = \"{course_id}\")  
                    =  (SELECT COUNT(1)  FROM prerequisite P  WHERE P.successor_id =  \"{course_id}\") THEN 1
		        ELSE 0
            END = 1
            AND C.quota > (SELECT COUNT(1) FROM Enrolls E WHERE E.course_id = \"{course_id}\")   # check quota
            AND S.username = \"{username}\"
            """)

            session['response'] = self.generate_form_response("Operation is performed. You can check the courses you are enrolled from R20.", request.form)

        elif formType == "View All Completed or Currently Enrolled Courses":  #R20
            username = session['username']
            response = connection.run_query(f"""
            SELECT C.course_id, C.name, CC.grade
            FROM Course C
                INNER JOIN Student S ON S.username = \"{username}\"
                LEFT JOIN Enrolls E ON E.course_id = C.course_id AND E.student_id = S.student_id 
                LEFT JOIN completed_course CC ON CC.Course_ID = C.course_id AND S.student_id = CC.student_id    
                WHERE E.course_id = C.course_id OR CC.course_id = C.course_id
            """)
            session['response'] = self.draw_table_response(f"All completed or currently enrolled courses by \"{username}\"",
                                                           [
                                                               'course_id',
                                                               'name',
                                                               'grade'
                                                           ],
                                                           response)
            
        elif formType == "View Courses with a Keyword":  #R21
            keyword = request.form['keyword']
            # Case insensitive check
         
            response = connection.run_query(f"""        
            SELECT C.course_id, C.name, U.surname, D.department_id, C.credits, R.classroom_id, R.time_slot, C.quota, group_concat(P.prerequisite_id) as prerequisites
            FROM Course C
                INNER JOIN Teaches T on T.course_id = C.course_id
                INNER JOIN User U on U.username = T.username
                INNER JOIN Department D on U.department_id = D.department_id
                INNER JOIN reserves R on R.course_id = T.course_id
                LEFT JOIN prerequisite P on P.successor_id = T.course_id
            WHERE C.name LIKE '%{keyword}%'
            GROUP BY C.course_id
            """)
            session['response'] = self.draw_table_response(f"Courses whose names include the given keyword \"{keyword}\"",
                                                           [
                                                               'course_id',
                                                               'name',
                                                               'surname',
                                                               'department_id',
                                                               'credits',
                                                               'classroom_id',
                                                               'time_slot',
                                                               'quota',
                                                               'prerequisite list'
                                                           ],
                                                           response)

        elif formType == "View Filtered Courses": #R22
            department_id = request.form["department_id"]
            campus = request.form["campus"]
            credits_1 = request.form["credits #1"]
            credits_2 = request.form["credits #2"]
            min_ = min(credits_1, credits_2)
            max_ = max(credits_1, credits_2)
            response = connection.run_query(f"""
            CALL filter_course(\"{department_id}\" , \"{campus}\",  {min_}, {max_});
            """, multi=True)
            response = [] if response is None else response
            session['response'] = self.draw_table_response(f"Courses filtered by the given parameters",
                                                           [
                                                               'course_id',
                                                           ],
                                                           response)



        return redirect(url_for('response_page'))