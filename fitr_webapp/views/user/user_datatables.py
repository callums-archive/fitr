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

from fitr_webapp.system.view_helpers import Base, Datatable

from fitr_webapp.system.permissions import permission, has_permission

from flask import jsonify


# datetime and string tools
import fitr_webapp.system.datetimetools as datetimetools
import fitr_webapp.system.stringtools as stringtools

# models
from fitr_webapp.models import (
    Measurements,
    Weight,
    Users
)


class UserAPIWeightDatatablePeek(Datatable):

    def before_request(self, name, **user):
        self.context = Users.serve_context(user.get("user"))

    @route('/<user>/weight_peek/datatable')
    @permission('user')
    def index(self, user):
        return self.datatable()

    def columns(self):
        return ["create_stamp", "weight", "unit"]

    def adj_create_stamp(self, val, row):
        return datetimetools.cast_string(val, "dt")
    
    def adj_weight(self, val, row):
        return f"{val} {row['unit']}"

    def adj_create_user(self, val, row):
        return str(val)

    def model(self):
        return Weight.objects.filter(user=self.context)


class UserAPIMeasureDatatablePeek(Datatable):

    def before_request(self, name, **user):
        self.context = Users.serve_context(user.get("user"))

    @route('/<user>/measure_peek/datatable')
    @permission('user')
    def index(self, user):
        return self.datatable()

    def columns(self):
        return ["create_stamp", "neck", "bicep", "chest", "abs1", "abs2", "abs3", "upperthigh", "midthigh", "calf"]

    def adj_create_stamp(self, val, row):
        return datetimetools.cast_string(val, "d")
    
    # def adj_weight(self, val, row):
    #     return f"{val} {row['unit']}"

    # def adj_create_user(self, val, row):
    #     return str(val)

    def model(self):
        return Measurements.objects.filter(user=self.context)