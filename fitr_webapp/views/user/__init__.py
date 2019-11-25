from .user import UserAPI
from .user import UserAPIWeightDatatable

def register_views(app, base):
    UserAPIWeightDatatable.register(app, route_base=base)
    UserAPI.register(app, route_base=base)
