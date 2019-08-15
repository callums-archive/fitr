from .user import User


def register_views(app, base):
    User.register(app, route_base=base)
