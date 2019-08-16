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


# datetime and string tools
import fitr_webapp.system.datetimetools as datetimetools
import fitr_webapp.system.stringtools as stringtools

# models
from fitr_webapp.models import (
    Measurements,
    Weight
)

class User(Base):
    # route_prefix="/<user>/"

    def before_request(self, name, user):
        self.context = Users.serve_context(user)

    @permission('user')
    def index(self):
        return abort(410)

    @permission('user')
    @route("/<user>/get/latest_measurements/")
    def get_measurements(self, user):
        measurements = Measurements.objects(user=self.context).order_by("+create_stamp").limit(5)
        return jsonify({"data": [record.show_measurements for record in measurements]})

    @permission('user')
    @route("/<user>/get/latest_weights/")
    def get_weights(self, user):
        weights = Weight.objects(user=self.context.to_dbref()).order_by("+create_stamp").limit(5)
        return jsonify({"data": [record.show_weights for record in weights], "initial_weight": Weight.objects(user=self.context.to_dbref()).first().weight})
