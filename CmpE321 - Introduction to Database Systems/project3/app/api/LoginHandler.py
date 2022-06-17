from flask_restful import Resource
from flask import request, url_for, redirect, session
import hashlib

from db import connection

class LoginHandler(Resource):
  def post(self):

    username = request.form['username']
    password = request.form['password']
    userType = request.form['userType']

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    accept = None
    if userType == 'admin':
      accept = self.is_admin(username, hashed_password)
    elif userType == 'instructor':
      accept = self.is_instructor(username, hashed_password)
    else:
      accept = self.is_student(username, hashed_password)

    
    if accept:
      session['username'] = username
      session['userType'] = userType
      return redirect(url_for('redirect_page'))
    else:
      return redirect(url_for('login'))

  # Methods below shall be updated with DB queries

  def is_admin(self, username, password):
    response = connection.run_query("""
    SELECT *
    FROM dbmanagers
    """)
    return (username, password) in response

  def is_instructor(self, username, password):
    response = connection.run_query("""
    SELECT i.username, password
    FROM instructor i
      INNER JOIN user u ON i.username = u.username
    """)
    return (username, password) in response

  def is_student(self, username, password):
    response = connection.run_query("""
    SELECT s.username, password
    FROM student s
      INNER JOIN user u ON s.username = u.username
    """)
    return (username, password) in response