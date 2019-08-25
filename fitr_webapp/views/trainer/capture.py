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

from fitr_webapp.models import (
    Weight, Measurements
)


class PTCaptureView(Base):
    # route_prefix="/trainer/"

    @route('/')
    @permission('pt_clients')
    def index(self):
        return render_template("trainer/capture.html")

    @route('/clients_search', methods=['POST'])
    @permission('pt_clients')
    def clients_post(self):
        term = self.data.get('term')
        if len(term) > 1:
            users = Users.search(term)
            if users is not None:
                return jsonify([{"username": user.username, "full_name": user.full_name} for user in users])
        return {}

    @route('/<user>/weights', methods=['GET'])
    @permission('pt_clients')
    def clients_get_weight(self, user):
        user = Users.by_username(user)
        if user is None:
            abort(404)
        return render_template("trainer/weights.html", client=user)

    @route('/<user>/measurements', methods=['GET'])
    @permission('pt_clients')
    def clients_get_measurements(self, user):
        user = Users.by_username(user)
        if user is None:
            abort(404)
        return render_template("trainer/measurements.html", client=user)

    @route('/<user>/weight', methods=['POST'])
    @permission('pt_clients')
    def weight_post(self, user):
        user = Users.by_username(user)
        if user is None:
            abort(404)

        if not Weight.add_weight(user, self.data.get("weight"), self.data.get("date", False)):
            abort(412, "Failed to add weight")

        weights = Weight.objects(user=user).order_by("-create_stamp").limit(2)
        diff = weights[0].weight - weights[1].weight
        sign = ""
        if diff > 0:
            sign="+"
        return f"{sign}{diff}KG's"

    @route('/<user>/fitness_test/<test>', methods=['POST'])
    @permission('pt_clients')
    def fitness_test_post(self, user, test):
        user = Users.by_username(user)
        if user is None:
            abort(404)

        if test not in ['pushup', 'situp', 'stepper']:
            abort(404)

        if test == "pushup":
            if user.capture_fitness_test(
                    test,
                    {
                        "unit": "pushups",
                        "value": int(self.data.get("value"))
                    }
                ):
                    return "OK"

        elif test == "situp":
            if user.capture_fitness_test(
                    test,
                    {
                        "unit": "situps",
                        "value": int(self.data.get("value"))
                    }
                ):
                    return "OK"
        elif test == "stepper":
            if user.capture_fitness_test(
                    test,
                    {
                        "unit": "bpm",
                        "value": int(self.data.get("value"))
                    }
                ):
                    return "OK"

    @route('/<user>/measuremets', methods=['POST'])
    @permission('pt_clients')
    def measurements_post(self, user):
        user = Users.by_username(user)
        if user is None:
            abort(404)

        if not Measurements.add_measurement(
            user,
            self.data.get('neck'),
            self.data.get('bicep'),
            self.data.get('chest'),
            self.data.get('abs1'),
            self.data.get('abs1_comment'),
            self.data.get('abs2'),
            self.data.get('abs2_comment'),
            self.data.get('abs3'),
            self.data.get('abs3_comment'),
            self.data.get('upperthigh', ""),
            self.data.get('midthigh'),
            self.data.get('calf'),
        ):
            abort(412, "Failed to add measurements")
        return "OK"
