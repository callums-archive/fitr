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
from fitr_webapp.system.session import clear_session

# from fitr_webapp.models import Measurements, CapturedMeasurements, MeasurementTemplates, Users


class DashboardView(Base):

    @route('/')
    @permission("user")
    def index(self):
        trainer = Users.by_username("wendy")
        # r = MeasurementTemplates()
        # r.name = "Gents"
        # r.fields = {
        #     "0": {"value": "Neck", "required": True},
        #     "1": {"value": "Bicep", "required": True},
        #     "2": {"value": "Chest", "required": True},
        #     "3": {"value": "Abs1", "required": True},
        #     "4": {"value": "Abs2", "required": True},
        #     "5": {"value": "Abs3", "required": True},
        #     "6": {"value": "Mid Thigh", "required": True},
        #     "7": {"value": "Calf", "required": True}
        #     }
        # r.create_user = trainer
        # r.save()

        # tem = MeasurementTemplates.objects.all()[0]
        # temw = MeasurementTemplates.objects.all()[1]

        # for m in Measurements.objects.all():
        #     print(m.show_measurements)
        #     if len(m.show_measurements['value']) == 9:
        #         e = CapturedMeasurements()
        #         e.user = m.user
        #         e.template = tem
        #         e.actuals = m.show_measurements['value']
        #         e.create_user = trainer
        #         e.create_stamp = m.show_measurements['create_stamp']
        #         e.save()
        #     else:
        #         e = CapturedMeasurements()
        #         e.user = m.user
        #         e.template = temw
        #         e.actuals = m.show_measurements['value']
        #         e.create_user = trainer
        #         e.create_stamp = m.show_measurements['create_stamp']
        #         e.save()

        # print(CapturedMeasurements.objects.all()[0].to_dict)
        return render_template("dashboard/dashboard.html")
