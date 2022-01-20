from flask import Blueprint, request, render_template, redirect, session
from models.user import get_user_by_email
import bcrypt

session_controller = Blueprint(
    "session_controller", __name__, template_folder="../templates/session")


@session_controller.route('/login')
def loginpage():
    error = request.args.get('error', None)
    return render_template('login.html', error=error)


@session_controller.route('/sessions/create', methods=["POST"])
def login():
    email = request.form.get('email')

    # Check if user is in database
    user = get_user_by_email(email)

    if user == None:
        return render_template('signup.html', message="Email not found, Sign up now!")

    # get password
    password = request.form.get('password')

    # check if password in database - including checking that user matches
    password_valid = user and bcrypt.checkpw(
        password.encode(), user['password'].encode())

    # add condition for password to match as well as email in database
    if password_valid:
        # if they are, update the session
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect('/')
    else:
        # if not, have user signup
        return render_template('login.html', message="Your password does not match. Please try again.")


@session_controller.route('/sessions/destroy', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect('/')
