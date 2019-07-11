# imports flaks
from flask import (
    Flask,
    render_template,
    redirect,
    url_for
)

# mongo
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface, connection
from mongoengine import connect

# custom errors
from app.system.errors import register_errors

# views
from app.views import register_views

from .models import Users


class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-MongoEngine settings
    MONGODB_SETTINGS = {
        'db': 'fitr',
        'host': 'mongodb://35.247.114.174:27017/fitr',
        "password": "4szlBDVZFOhhfACsIlZk10M5vmhTEbwCrv6f0zFV5NY="
    }

# create the app and get the config
def create_app():
    app = Flask(__name__)

    # config
    # app.config.from_json('config.json')


    app.config.from_object(__name__+'.ConfigClass')

    # app.config['MONGODB_SETTINGS'] = {
    #   "db": "fitr",
    #   "host": "mongodb://35.247.114.174:27017/fitr",
    #   "port": 27017,
    #   "username": "fitr",
    #   "password": "4szlBDVZFOhhfACsIlZk10M5vmhTEbwCrv6f0zFV5NY="
    # }




    # mongo
    # connect('fitr', alias='default')
    db = MongoEngine(app, app.config)

    try:
        Users.objects.first().username
    except Exception as e:
        print(e)
    print(connection.get_connection_settings(app.config))


    # mongo for session
    app.session_interface = MongoEngineSessionInterface(db)


    # simple view
    @app.route('/')
    def index():
        # return connection.get_connection_settings(app.config)['host']
        return redirect(url_for('UserAuthenticationView:login_get'))

    # register views
    register_views(app)

    # register custom errors
    register_errors(app)

    # return app to run
    return app
