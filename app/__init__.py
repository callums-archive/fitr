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


# create the app and get the config
def create_app():
    app = Flask(__name__)

    # config
    app.config.from_json('config.json')

    # app.config['MONGODB_SETTINGS'] = {
    #   "db": "fitr",
    #   "host": "35.247.114.174",
    #   "port": 27017,
    #   "username": "fitr",
    #   "password": "4szlBDVZFOhhfACsIlZk10M5vmhTEbwCrv6f0zFV5NY="
    # }

    # mongo
    db = MongoEngine(app)

    # mongo for session
    app.session_interface = MongoEngineSessionInterface(db)

    # print(connection.get_connection_settings(app.config))

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
