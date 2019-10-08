from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    request,
    jsonify
)

from flask_classy import route

from fitr_webapp.models import Users, AccountRecovery

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

    @route("/forgot", methods=['GET'])
    def forgot_get(self):
        return render_template("authentication/forgot.html")

    @route("/forgot", methods=['POST'])
    def forgot_post(self):
        user = Users.by_identifier(self.data.get('identifier'))
        if user is None:
            abort(412, jsonify({"error_msg": "Error submitting request."}))

        try:
            if user.recover_account():
                return "OK"
            else:
                abort(412, {"error_msg": "Error submitting request."})
        except DBError as e:
            abort(412, {"error_msg": str(e)})

    @route("/forgot/<key>/", methods=['GET'])
    def forgot_reset_get(self, key):
        try:
            if AccountRecovery.process_response(key):
                return render_template("authentication/forget_reset.html")
        except DBError as e:
            return str(e)

    @route("/forgot/<key>/", methods=['POST'])
    def forgot_reset_post(self, key):
        if self.data.get("password") != self.data.get("confirm"):
            abort(400, {"error_msg": "Password missmatch."})

        try:
            if AccountRecovery.finalize_response(key, self.data.get("confirm")):
                return "OK"
            else:
                abort(412, {"error_msg": "Error submitting request."})
        except DBError as e:
            abort(412, {"error_msg": str(e)})

    @route("/logout", methods=['GET'])
    def logout(self):
        clear_session()
        return redirect(url_for("index"))
