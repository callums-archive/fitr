from flask import (
    render_template,
    abort,
    redirect,
    url_for
)

from flask_classy import (
    FlaskView,
    route,
)

from app.models import Users


class UserAuthenticationView(FlaskView):

    @route('/login')
    def login_get(self):
        return render_template("authentication/login.html")

    @route('/login', methods=['POST'])
    def login_post(self):
        identifier, password = request.form.get('identifier'), request.form.get('password')

        try:
            Users.login(identifier, password)
            return redirect(url_for("index"))
        except DBError as e:
            abort(412, {"error_msg": str(e)})
        else:
            abort(412, {"error_msg": "System error, please try again."})

    @route("/logout", methods=['GET'])
    def logout():
        clear_session()
        return redirect(url_for("index"))
