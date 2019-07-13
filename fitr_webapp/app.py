# imports flaks
from flask import (
    Flask,
    render_template,
    redirect,
    url_for
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

# std for os env
from os import environ

# create the app and get the config
app = Flask(__name__)

# config
if environ.get("ENV", "") == "production":
    app.config.from_json('production.json')
else:
    app.config.from_json('development.json')

# mongo
db = MongoEngine(app)

# mongo for session
app.session_interface = MongoEngineSessionInterface(db)


# register jinja2 funtions
app.jinja_env.globals.update(is_loggedin=is_loggedin)
app.jinja_env.globals.update(user=get_current_user)
app.jinja_env.globals.update(has_permission=has_permission)

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

if __name__ == "__main__":
    app.run()
