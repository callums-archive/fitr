# flask imports
from flask import (
    Blueprint,
    request,
    abort,
    jsonify,
    redirect, 
    url_for,
)
from app.system.permissions import permission

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
@permission("none")
def login():
    return "Log in"

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