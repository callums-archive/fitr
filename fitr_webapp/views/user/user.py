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


class UserAPIWeightDatatable(Datatable):

    def before_request(self, name, **user):
        self.context = Users.serve_context(user.get("user"))

    @route('/<user>/weight/datatable')
    @permission('trainer_clients')
    def index(self, user):
        return self.datatable()

    def columns(self):
        return ["weight", "create_stamp", "unit"]

    def adj_create_stamp(self, val, row):
        return datetimetools.cast_string(val, "dt")
    
    def adj_weight(self, val, row):
        return f"{val} {row['unit']}"

    def model(self):
        return Weight.objects.filter(user=self.context)

    def search(self, term):
        return Weight.objects.filter(user=self.context)

class UserAPI(Base):
    # route_prefix="/<user>/"

    def before_request(self, name, **user):
        self.context = Users.serve_context(user.get("user"))

    #
    # Weight
    #

    @permission("user")
    @route("/<user>/weight", methods=["POST"])
    def post_weight(self, user):
        if Weight.add(self.context, self.data['weight'], self.data['backdate']):
            return {"diff_init": self.context.weight_difference, "diff_prev": self.context.weight_difference_previous}
        abort(412, {"error_msg": "Failed to add weight. Please try again!"})

    # @permission('user')
    # @route('/<user>/weight/datatable')
    # def weight_datatable

    @permission('user')
    def index(self):
        return abort(410)

    @permission('user')
    @route("/<user>/get/latest_measurements/")
    def get_measurements(self, user):
        measurements = Measurements.objects(user=self.context).order_by("+create_stamp")
        return jsonify({"data": [record.show_measurements for record in measurements]})

    @permission('user')
    @route("/<user>/get/latest_weights/")
    def get_weights(self, user):
        weights = Weight.objects(user=self.context.to_dbref()).order_by("+create_stamp")
        return jsonify({"data": [record.show_weights for record in weights], "initial_weight": Weight.objects(user=self.context.to_dbref()).order_by("+create_stamp").first().weight})

    @permission('user')
    @route("/<user>/get/measurements/<measure>/")
    def get_measure(self, user, measure):
        measurements = Measurements.objects(user=self.context).order_by("+create_stamp")
        return jsonify({"data": [{
            "value": record.show_measurements.get(measure),
            "unit": record.unit,
            "create_user": record.create_user,
            "create_stamp": datetimetools.cast_string(record.create_stamp, "d"),
            "comment": record.show_measurements.get(f"{measure}_comment"),
            "initial":Measurements.objects(user=self.context.to_dbref()).order_by("+create_stamp").first().show_measurements.get(measure)} for record in measurements]})

    # @permission('zuck')
    # @route("/<user>/get")
    # def get_all(self, user):
    #     res = []
    #     all = Users.objects.all();
    #     for x in all:
    #         wht = Weight.objects(user=x).order_by('-create_stamp').first()
    #         try:
    #             res.append({x.full_name: wht.weight})
    #         except:
    #             pass
    #     return jsonify(res)
