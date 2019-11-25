from flask import (
    jsonify,
    make_response,
    redirect,
    url_for,
    request,
    render_template
)


def register_errors(app):

    # 412 precondition failed
    @app.errorhandler(412)
    def precondition_failed(error):
        if type(error.description) is not type(dict()):
            return make_response(error.description, 412)
        return make_response(jsonify(error.description), 412)

    @app.errorhandler(403)
    def forbidden(error):
        if not request.user:
            return redirect(url_for("UserAuthentication:login_get"))
        else:
            return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
