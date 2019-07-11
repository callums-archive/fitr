from .authentication import register_views as auth_views


def register_views(app):
    # register Auth view
    auth_views(app, '/auth/')
