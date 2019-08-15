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

class User(Base):
    # route_prefix="/<user>/"

    def before_request(self, name, user):
        self.context = Users.serve_context(user)

    @permission('user')
    def index(self):
        return abort(410)

    @permission('user')
    @route("/<user>/get/measurements/")
    def get_measurements(self, user):
        from fitr_webapp.models import Users, Measurements, Weight, FitnessTests, Logins

        # iter = 1
        # for x in Users.objects.all():
        #     x.uid = iter
        #     iter+=1
        #     x.save()
        #
        # print(f"user {iter}")
        #
        # iter = 1
        # for x in Measurements.objects.all():
        #     x.uid = iter
        #     iter+=1
        #     x.save()
        #
        # print(f"measure {iter}")
        #
        # iter = 1
        # for x in Weight.objects.all():
        #     x.uid = iter
        #     iter+=1
        #     x.save()
        #
        # print(f"we {iter}")

        # iter = 1
        # for x in FitnessTests.objects.all():
        #     x.uid = iter
        #     iter+=1
        #     x.save()
        #
        # print(f"ft {iter}")

        return ""
        # return jsonify(self.context.measurements.order_by('-create_stamp'))
