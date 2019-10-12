from flask import jsonify, make_response, redirect, url_for


def register_errors(app):

    # 412 precondition failed
    @app.errorhandler(412)
    def precondition_failed(error):
        if type(error.description) is not type(dict()):
            return make_response(error.description, 412)
        return make_response(jsonify(error.description), 412)

    @app.errorhandler(403)
    def forbidden_x(error):
        return redirect(url_for("UserAuthentication:login_get"))
        # if type(error.description) is not type(dict()):
        #     return make_response(error.description, 412)
        # return make_response(jsonify(error.description), 412)
