from flask import Flask, redirect
import os

from controllers.coins_controller import coins_controller
from controllers.user_controller import user_controller
from controllers.session_controller import session_controller

app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET")
app.config['SECRET_KEY'] = SECRET_KEY
# DB_URL = os.environ.get("DATABASE_URL", "dbname=project-2-cryptrack")


@app.route('/')
def index():
    return redirect('/coins')


app.register_blueprint(user_controller)
app.register_blueprint(session_controller)
app.register_blueprint(coins_controller)

if __name__ == "__main__":
    app.run(debug=True)
