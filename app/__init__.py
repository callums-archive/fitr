# imports flaks
from flask import (
    Flask,
    render_template,
    redirect,
    url_for
)

# mongo
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface, connection

# custom errors
from app.system.errors import register_errors

# views
from app.views import register_views

# permission
from app.system.permissions import permission, has_permission

# session stuff
from app.system.session import is_loggedin, get_current_user

# create the app and get the config
def create_app():
    app = Flask(__name__)

    # config
    app.config.from_json('config.json')

    # mongo
    db = MongoEngine(app)

    # mongo for session
    app.session_interface = MongoEngineSessionInterface(db)

    # root view
    @app.route('/')
    def index():
        if is_loggedin():
            print("here here here")
            return redirect(url_for('DashboardView:index'))
        return redirect(url_for('UserAuthenticationView:login_get'))

    # register jinja2 funtions
    app.jinja_env.globals.update(is_loggedin=is_loggedin)
    app.jinja_env.globals.update(user=get_current_user)
    app.jinja_env.globals.update(has_permission=has_permission)

    # register views
    register_views(app)

    # register custom errors
    register_errors(app)

    # return app to run
    return app
