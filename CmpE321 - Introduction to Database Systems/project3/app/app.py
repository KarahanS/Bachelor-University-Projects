from flask import Flask, render_template, session,url_for, redirect, flash
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__, template_folder='./templates', static_url_path='', static_folder='build')
app.config['SECRET_KEY'] = 'Secret Key'
CORS(app) #comment this on deployment
api = Api(app)

@app.route('/')
def login():
    if not session.get('initialized', False):
        session['initialized'] = True
        session['username'] = None
        session['userType'] = None
    elif session['username'] != None:
        return redirect(url_for('redirect_page'))

    return render_template('login.html')

@app.route('/admin_panel')
def admin_panel():
    if session['username'] == None or session['userType'] != 'admin':
        flash("You are not allowed to access this page.")
        return redirect(url_for('redirect_page'))
    return render_template('admin_panel.html', username=session['username'])

@app.route('/instructor_panel')
def instructor_panel():
    if session['username'] == None or session['userType'] != 'instructor':
        flash("You are not allowed to access this page.")
        return redirect(url_for('redirect_page'))
    return render_template('instructor_panel.html', username=session['username'])

@app.route('/student_panel')
def student_panel():
    if session['username'] == None or session['userType'] != 'student':
        flash("You are not allowed to access this page.")
        return redirect(url_for('redirect_page'))
    return render_template('student_panel.html', username=session['username'])

@app.route("/redirect_page")
def redirect_page():
    if session['username'] == None:
        return redirect(url_for('login'))
    for userType in ['admin', 'instructor', 'student']:
        if session['userType'] == userType:
            return redirect(url_for("%s_panel"%userType))
    return "Error in redirection"

@app.route("/response_page")
def response_page():
    if session.get('response', None) == None:
        flash("There is no response.")
        return redirect(url_for('redirect_page'))
    else:
        response = session['response']
        session['response'] = None
        
        return render_template('response_page.html', response=response)

from api.LoginHandler import LoginHandler
from api.LogoutHandler import LogoutHandler
from api.AdminHandler import AdminHandler
from api.InstructorHandler import InstructorHandler
from api.StudentHandler import StudentHandler

api.add_resource(LoginHandler, '/api/LoginHandler')
api.add_resource(LogoutHandler, '/api/LogoutHandler')
api.add_resource(AdminHandler, '/api/AdminHandler')
api.add_resource(InstructorHandler, '/api/InstructorHandler')
api.add_resource(StudentHandler, '/api/StudentHandler')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)