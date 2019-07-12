from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    request
)

from flask_classy import route

from fitr_webapp.models import Users

from fitr_webapp.system.exceptions import DBError

from fitr_webapp.system.view_helpers import Base

from fitr_webapp.system.session import clear_session

from fitr_webapp.system.stringtools import sanitize_lower


class UserAuthenticationView(Base):

    @route('/login')
    def login_get(self):
        return render_template("authentication/login.html")

    @route('/login', methods=['POST'])
    def login_post(self):
        identifier, password = sanitize_lower(self.data.get('identifier')), self.data.get('password')

        try:
            Users.login(identifier, password)
            return {"redirect": url_for("DashboardView:index")}
        except DBError as e:
            abort(412, {"error_msg": str(e)})
        else:
            abort(412, {"error_msg": "System error, please try again."})

    @route("/logout", methods=['GET'])
    def logout(self):
        clear_session()
        return redirect(url_for("index"))
