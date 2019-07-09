# flask imports
from flask import (
    Blueprint,
    request,
    abort,
    jsonify,
    redirect, 
    url_for,
)
from flask_login import login_required

# DB imports
from app.models import Users

# system
from app.system.exceptions import DBError
from app.system.session import clear_session


auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)

@auth.route("/login", methods=['GET'])
def login():
    return "Log in"

@auth.route("/login", methods=['POST'])
def submit_login():
    username, password = request.form.get('username'), request.form.get('password')

    try:  
        Users.login(username, password)
        return redirect(url_for("index"))
    except DBError as e:
        abort({"error", str(e)}, 412)
    else:
        abort({"error", "System error, please try again."}, 412)

@auth.route("/logout", methods=['GET'])
@login_required
def logout():
    clear_session()
    return redirect(url_for("index"))