from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    request
)

from flask_classy import route

from app.models import Users

from app.system.exceptions import DBError

from app.system.view_helpers import Base

from app.system.permissions import permission, has_permission

from flask import jsonify


class PTCaptureView(Base):
    route_prefix="/trainer/"

    @route('/')
    @permission('pt_clients')
    def index(self):
        return render_template("trainer/capture.html")

    @route('/clients_search', methods=['POST'])
    def clients_post(self):
        term = self.data.get('term')
        if len(term) > 1:
            users = Users.search(term)
            if users is not None:
                return jsonify([{"username": user.username, "full_name": user.full_name} for user in users])
        return {}

    @route('/<user>', methods=['GET'])
    def clients_get(self, user):
        user = Users.by_username(user)
        if user is None:
            abort(404)
        return render_template("trainer/capture_data.html", client=user)

    @route('/<user>/weight', methods=['POST'])
    def weight_post(self, user):
        user = Users.by_username(user)
        if user is None:
            abort(404)

        if not user.capture_weight(str(self.data.get('weight')).replace(",", ".")):
            abort(412, "Failed to add weight")
        return "OK"

    @route('/<user>/measuremets', methods=['POST'])
    def measurements_post(self, user):
        user = Users.by_username(user)
        if user is None:
            abort(404)

        if not user.capture_mesaurements(
            str(self.data.get('neck')).replace(",", "."),
            str(self.data.get('bicep')).replace(",", "."),
            str(self.data.get('chest')).replace(",", "."),
            str(self.data.get('abs1')).replace(",", "."),
            self.data.get('abs1_comment'),
            str(self.data.get('abs2')).replace(",", "."),
            self.data.get('abs2_comment'),
            str(self.data.get('abs3')).replace(",", "."),
            self.data.get('abs3_comment'),
            str(self.data.get('upperthigh')).replace(",", "."),
            str(self.data.get('midthigh')).replace(",", "."),
            str(self.data.get('calf')).replace(",", "."),
        ):
            abort(412, "Failed to add measurements")
        return "OK"
