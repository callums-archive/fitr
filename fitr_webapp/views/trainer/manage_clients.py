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

from math import floor

from flask import jsonify

from fitr_webapp.models import (
    Weight, Measurements
)

from fitr_webapp.system import mailer


class TrainerManageClients(Base):

    @route('/clients')
    @permission('trainer_clients')
    def index(self):
        # display manage clients interface
        return render_template("trainer/manage_clients/index.html")

    @route('/get_clients/<page>', methods=['GET'])
    @permission('trainer_clients')
    def get_clients(self, page=0):
        # we assume that the request.user is the trainer
        # we need to do a lookup on the database (Users) where request.user is in list of trainers

        skip = int(page) * 10
        res = Users.objects.filter(
            trainers__contains=request.user.to_dbref()
        )

        # get to total number of documents
        total = floor(len(res)/10)

        # set pagination
        res = res.skip(skip).limit(10)

        final_result = []
        for user in res:
            final_result.append(
                {"name": user.full_name, "username": user.username}
            )
        return jsonify({"data": final_result, "offsets": total})

    @route('/search_clients', methods=['POST'])
    @permission('trainer_clients')
    def search_clients(self):
        term = self.data.get('term')
        res = Users.search(term).filter(
            trainers__contains=request.user.to_dbref()
        )
        final_result = []
        for user in res:
            final_result.append(
                {"name": user.full_name, "username": user.username}
            )
        return jsonify(final_result)
