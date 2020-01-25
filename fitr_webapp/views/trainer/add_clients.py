from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    request
)

from flask_classy import route

from fitr_webapp.models import Users, FitnessTests

from fitr_webapp.system.exceptions import DBError

from fitr_webapp.system.view_helpers import Base

from fitr_webapp.system.permissions import permission, has_permission

from flask import jsonify

from fitr_webapp.models import (
    Weight, Measurements
)

from fitr_webapp.system import mailer


class TrainerAddClientsAPI(Base):
    @route('/')
    @permission('trainer_clients')
    def index(self):
        return render_template("trainer/add_clients/add_clients.html")

    @route('/', methods=['POST'])
    @permission('trainer_clients')
    def add_client(self):
        user = Users.by_username(self.data.get("username"))
        user.trainers.append(self.request.user)
        user.save()
        return "OK"

    @route('/clients_search', methods=['POST'])
    @permission('trainer_clients')
    def client_search_post(self):
        term = self.data.get('term')
        if len(term) > 1:
            users = Users.search(term)
            if users is not None:
                return jsonify([{"username": user.username, "full_name": user.full_name, "trainers": len(user.trainers)} for user in users if len(user.trainers) == 0])
        return jsonify({})