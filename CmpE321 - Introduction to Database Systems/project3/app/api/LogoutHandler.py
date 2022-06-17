from flask_restful import Resource
from flask import request, url_for, redirect, session


class LogoutHandler(Resource):
  def post(self):
    session['username'] = None
    session['userType'] = None
    return redirect(url_for('login'))