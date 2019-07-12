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


class DashboardView(Base):


    @route('/')
    @permission('dashboard')
    def index(self):
        return render_template("dashboard/dashboard.html")
