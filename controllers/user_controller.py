from flask import Blueprint, render_template, request, redirect
import bcrypt
from models.user import insert_user

user_controller = Blueprint(
    "user_controller", __name__, template_folder="../templates/users")


@user_controller.route('/signup')
def signup():
    return render_template('signup.html')


@user_controller.route('/users', methods=["POST"])
def create_user():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    hashed_password = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()).decode()
    insert_user(email, name, hashed_password)
    return redirect('/login')
