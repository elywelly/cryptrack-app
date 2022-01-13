from flask import Blueprint, request, render_template

session_controller = Blueprint(
    "session_controller", __name__, template_folder="../templates/session")


@session_controller.route('/login')
def loginpage():
    error = request.args.get('error', None)
    return render_template('login.html', error=error)
