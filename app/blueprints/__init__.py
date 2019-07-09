# import blueprints
from .authentication import auth

# register all blueprints
def register_blueprints(app):
    app.register_blueprint(auth, url_prefix="/auth")