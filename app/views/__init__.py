from .authentication import register_views as auth_views
from .dashboard import register_views as dash_views
from .trainer import register_views as trainer_views


def register_views(app):
    # register Auth views
    auth_views(app, '/auth/')

    # register Dash views
    dash_views(app, '/dashboard/')

    # register Dash views
    trainer_views(app, '/trainer/')
