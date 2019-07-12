from .user_authentication import UserAuthenticationView
from .user_registration import UserRegistrationView


def register_views(app, base):
    UserAuthenticationView.register(app, route_base=base)
    UserRegistrationView.register(app, route_base=base)
