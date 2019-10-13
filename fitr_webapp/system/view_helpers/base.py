from flask import (
    request,
    has_request_context
)

from flask_classy import FlaskView


class Base(FlaskView):
    def __init__(self):
        super(Base, self).__init__()
        self.request = request

    @property
    def data(self):
        if has_request_context():
            if self.request.is_json:
                data = request.get_json(force=True)
            else:
                data = request.form
        return data
