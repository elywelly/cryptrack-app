from flask import Blueprint, render_template, request, redirect, session
import bcrypt
from models.user import insert_user, delete_user, get_user_by_email
from models.transactions import delete_wallet, delete_history

user_controller = Blueprint(
    "user_controller", __name__, template_folder="../templates/users")


@user_controller.route('/about')
def about():
    return render_template('about.html')


@user_controller.route('/signup')
def signup():
    return render_template('signup.html')


@user_controller.route('/users', methods=["GET", "POST"])
def create_user():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if email == None or name == None or password == None:
        return redirect('/')

    db_email = get_user_by_email(email)

    if db_email != None:
        return render_template('signup.html', message="Email is already in use. Please enter a new email.")

    hashed_password = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()).decode()
    insert_user(email, name, hashed_password)
    return redirect('/login')


@user_controller.route('/users/account')
def my_account():
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('account.html')


@user_controller.route('/users/account/delete', methods=["GET", "POST"])
def delete_account():
    if not session.get('user_id'):
        return redirect('/login')

    delete = request.form.get("delete")

    if delete == None:
        return redirect('/coins')

    if delete == 'Delete Account':
        user_id = int(session.get('user_id'))
        delete_wallet(user_id)
        delete_history(user_id)
        delete_user(user_id)
        session.clear()
        return redirect('/signup')
