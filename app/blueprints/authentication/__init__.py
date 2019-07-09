# flask imports
from flask import (
    Blueprint,
    request,
    abort,
    jsonify,
    redirect, 
    url_for,
    render_template
)
from app.system.permissions import permission

# DB imports
from app.models import Users

# system
from app.system.exceptions import DBError
from app.system.session import clear_session

# std
from datetime import datetime


auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)

@auth.route("/login", methods=['GET'])
def login():
    return render_template("authentication/login.html", year= datetime.utcnow().year)

@auth.route("/login", methods=['POST'])
def submit_login():
    username, password = request.form.get('username'), request.form.get('password')

    try:  
        Users.login(username, password)
        return redirect(url_for("index"))
    except DBError as e:
        abort(412, {"error_msg": str(e)})
    else:
        abort(412, {"error_msg": "System error, please try again."})

@auth.route("/logout", methods=['GET'])
def logout():
    clear_session()
    return redirect(url_for("index"))