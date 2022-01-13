from flask import Blueprint, render_template

user_controller = Blueprint(
    "user_controller", __name__, template_folder="../templates/users")


@user_controller.route('/signup')
def signup():
    return render_template('signup.html')
