# imports flaks
from flask import (
    Flask, 
    render_template,
    redirect,
    url_for
)

# mongo
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

# blue prints
from app.blueprints import register_blueprints

# custom errors
from app.system.errors import register_errors


# create the app and get the config
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.cfg')

    # mongo
    db = MongoEngine(app)

    # mongo for session
    app.session_interface = MongoEngineSessionInterface(db)

    # simple view
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # register all of the blueprints
    register_blueprints(app)

    # register errors
    register_errors(app)

    # return app to run
    return app