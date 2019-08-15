from .authentication import register_views as auth_views
from .dashboard import register_views as dash_views
from .trainer import register_views as trainer_views
from .user import register_views as user_views


def register_views(app):
    # register Auth views
    auth_views(app, '/auth/')

    # register Dash views
    dash_views(app, '/dashboard/')

    # register trainer views
    trainer_views(app, '/trainer/')

    # register user views
    user_views(app, '/users/')
