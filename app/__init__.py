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
from app.system.errors import register_errors
from app.views import register_views


# create the app and get the config
def create_app():
    app = Flask(__name__)

    # config
    app.config.from_pyfile('config.cfg')

    # mongo
    db = MongoEngine(app)

    # mongo for session
    app.session_interface = MongoEngineSessionInterface(db)

    # simple view
    @app.route('/')
    def index():
        return redirect(url_for('UserAuthenticationView:login_get'))

    # register views
    register_views(app)

    # register custom errors
    register_errors(app)

    # return app to run
    return app
