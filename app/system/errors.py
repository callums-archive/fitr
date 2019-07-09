from flask import jsonify, make_response


def register_errors(app):

    # 412 precondition failed
    @app.errorhandler(412)
    def precondition_failed(error):
        if type(error.description) is not type(dict()):
            return error
        return make_response(jsonify(error.description), 412)