from flask import Blueprint, render_template, request, redirect, session
import bcrypt
from models.user import insert_user, delete_user, get_user_by_email, user_update_name, user_update_email, user_update_password
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
        return render_template('signup.html', message="Email error. Please try again.")

    hashed_password = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()).decode()
    insert_user(email, name, hashed_password)
    user = get_user_by_email(email)
    session['user_id'] = user['id']
    # to display username login as
    session['user_name'] = user['name']
    return redirect('/')


@user_controller.route('/users/account')
def my_account():
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('account.html')


@user_controller.route('/users/account/name', methods=["GET", "POST"])
def update_name():
    if not session.get('user_id'):
        return redirect('/login')

    id = int(session.get('user_id'))
    new_value = request.form.get("name")

    if new_value == None:
        return redirect('/users/account')

    user_update_name(new_value, id)

    return render_template('account.html', message="Name Updated. Login again to view name change.")


@user_controller.route('/users/account/email', methods=["GET", "POST"])
def update_email():
    if not session.get('user_id'):
        return redirect('/login')

    id = int(session.get('user_id'))
    new_value = request.form.get("email")

    if new_value == None:
        return redirect('/users/account')

    user_update_email(new_value, id)

    return render_template('account.html', message="Email Updated")


@user_controller.route('/users/account/password', methods=["GET", "POST"])
def update_password():
    if not session.get('user_id'):
        return redirect('/login')

    id = int(session.get('user_id'))
    password = request.form.get("password")
    field = 'password'

    if password == None:
        return redirect('/users/account')

    new_value = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()).decode()

    user_update_password(new_value, id)

    return render_template('account.html', message="Password Updated")


@user_controller.route('/users/account/delete', methods=["POST"])
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
