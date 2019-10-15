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

from fitr_webapp.system.view_helpers import Base, Datatable

from fitr_webapp.system.permissions import permission, has_permission

from math import floor

from flask import jsonify

from fitr_webapp.models import (
    Weight, Measurements
)

from fitr_webapp.system import mailer


class TrainerManageClientsDataTable(Datatable):
    @route('/datatable')
    @permission('trainer_clients')
    def index(self):
        return self.datatable()

    def columns(self):
        return ['first_name', 'surname', 'username']

    def model(self):
        return Users.objects.filter(trainers__contains=request.user.to_dbref())

    def search(self, term):
        return Users.search(term).filter(trainers__contains=request.user.to_dbref())


class TrainerManageClients(Base):

    @route('/clients')
    @permission('trainer_clients')
    def index(self):
        # display manage clients interface
        return render_template("trainer/manage_clients/index.html")


class TrainerManageClientAPI(Base):

    def before_request(self, name, **user):
        self.context = Users.serve_context(user.get("user"))

    @route('/clients/<user>')
    @permission('trainer_clients')
    def index(self, user):
        # display manage clients interface
        return render_template("trainer/manage_clients/index.html")
