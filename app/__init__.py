# imports flaks
from flask import (
    Flask,
    render_template,
    redirect,
    url_for
)

# mongo
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension

# custom errors
from app.system.errors import register_errors

# views
from app.views import register_views


# create the app and get the config
def create_app():
    app = Flask(__name__)


    # config
    app.config.from_json('config.json')

    # mongo
    db = MongoEngine(app)

    from flask_debugtoolbar import DebugToolbarExtension

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
