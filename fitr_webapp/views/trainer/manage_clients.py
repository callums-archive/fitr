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

from fitr_webapp.system import (
    datetimetools, 
    stringtools
)

from math import floor

from flask import jsonify

from fitr_webapp.models import (
    Weight, Measurements, Users
)

from fitr_webapp.system import mailer

#
# All Clients Datatable
#
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
        for x in Weight.objects.all():
            x.create_user = request.user
            x.save()
        return render_template("trainer/manage_clients/client_list.html")


class TrainerManageClientAPI(Datatable):

    def before_request(self, name, **user):
        # possibley a context user issue, can see user data after delinking
        self.context = Users.serve_context(user.get("user"))

    @route('/clients/<user>')
    @permission('trainer_clients')
    def index(self, user):
        """
        Trainer datatable of all clients
        """
        return render_template("trainer/manage_clients/user_options.html", client=self.context)


    @route('/clients/<user>/details')
    @permission('trainer_clients')
    def user_details(self, user):
        """
        User Details JSON
        """
        try:
            initial_measurement = f"{self.context.initial_measurement.to_dict['facts']['total']} {self.context.initial_measurement.to_dict['facts']['unit']}"
        except:
            initial_measurement = "No Data"

        try:
            latest_measurement = f"{self.context.latest_measurement.to_dict['facts']['total']} {self.context.latest_measurement.to_dict['facts']['unit']}"
        except:
            latest_measurement = "No Data"

        try:
            measurement_difference = f"{self.context.measurement_difference['diff']} {self.context.measurement_difference['unit']}"
        except:
            measurement_difference = "No Data"

        try:
            last_seen = datetimetools.cast_string(self.context.last_seen, "dt")
        except:
            last_seen = "No Data"

        try:
            initial_weight = f"{self.context.initial_weight.weight} {self.context.initial_weight.unit}"
            latest_weight = f"{self.context.latest_weight.weight} {self.context.latest_weight.unit}"
        except:
            initial_weight = "No Data"
            latest_weight = "No Data"

        return jsonify({
            "fullname": self.context.full_name,
            "username": self.context.username,
            "gender": stringtools.sanitize_title(self.context.gender),
            "age": datetimetools.age(self.context.date_of_birth),
            "birth_date": datetimetools.cast_string(self.context.date_of_birth, "d"),
            "last_seen": last_seen,
            "initial_weight": initial_weight,
            "latest_weight": latest_weight,
            "weight_difference": f"{self.context.weight_difference.get('weight')} {self.context.weight_difference.get('unit')}",
            "initial_measurement": initial_measurement,
            "latest_measurement": latest_measurement,
            "measurement_difference": measurement_difference,
            "fitness_tests_total": len(self.context.fitness_tests)
        })

    @route('/clients/<user>/', methods=['DELETE'])
    @permission('trainer_clients')
    def user_delink(self, user):
        """
        Detach user from trainer
        """
        index = self.context.trainers.index(self.request.user)
        self.context.trainers.pop(index)
        self.context.save()
        return "OK"
       

    @route('/clients/<user>/weight')
    @permission('trainer_clients')
    def user_weight(self, user):
        """
        User weight management interface
        """
        return render_template("trainer/manage_clients/client_weight.html", client=self.context)
