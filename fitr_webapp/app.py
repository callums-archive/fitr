# imports flaks
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request
)

# mongo
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

# custom errors
from fitr_webapp.system.errors import register_errors

# views
from fitr_webapp.views import register_views

# permissions
from fitr_webapp.system.permissions import permission, has_permission

# session stuff
from fitr_webapp.system.session import is_loggedin, get_current_user

# sentry
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# datetime and string tools
import fitr_webapp.system.datetimetools as datetimetools
import fitr_webapp.system.stringtools as stringtools

# std for os env
from os import environ

# create the app and get the config
app = Flask(__name__)

# config
if environ.get("FLASK_ENV", "") == "development":
    app.config.from_json('development.json')
else:
    app.config.from_json('production.json')

app.config.from_json('frontend.json')

# mongo
db = MongoEngine(app)

# mongo for session
app.session_interface = MongoEngineSessionInterface(db)

# register jinja2 funtions
app.jinja_env.globals.update(is_loggedin=is_loggedin)
app.jinja_env.globals.update(user=get_current_user)
app.jinja_env.globals.update(has_permission=has_permission)
app.jinja_env.globals.update(datetimetools=datetimetools)
app.jinja_env.globals.update(datetimetools=datetimetools)
app.jinja_env.globals.update(colours=app.config['COLOURS'])

# register views
register_views(app)

# register custom errors
register_errors(app)

# init sentry
if app.config.get("SENTRY", "") != "":
    sentry_sdk.init(
        dsn=app.config['SENTRY'],
        integrations=[FlaskIntegration()]
    )

# root view
@app.route('/')
def index():
    if is_loggedin():
        return redirect(url_for('DashboardView:index'))
    return redirect(url_for('UserAuthenticationView:login_get'))


@app.before_request
def before_req():
    if is_loggedin():
        request.user = get_current_user()
    else:
        request.user = None
