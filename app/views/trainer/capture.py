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
