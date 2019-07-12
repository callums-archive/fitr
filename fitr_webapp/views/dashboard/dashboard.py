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


class DashboardView(Base):


    @route('/')
    @permission('dashboard')
    def index(self):
        return render_template("dashboard/dashboard.html")
