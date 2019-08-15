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

from fitr_webapp.system.permissions import permission, has_permission

from flask import jsonify


class User(Base):
    # route_prefix="/<user>/"

    def before_request(self, name, user):
        self.context = Users.serve_context(user)

    @permission('user')
    def index(self):
        return abort(410)

    @permission('user')
    @route("/<user>/get/measurements/")
    def get_measurements(self, user):
        return jsonify(self.context.measurements)
