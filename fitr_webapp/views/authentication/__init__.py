from .user_authentication import UserAuthentication
from .user_registration import UserRegistrationView


def register_views(app, base):
    UserAuthentication.register(app, route_base=base)
    UserRegistrationView.register(app, route_base=base)
