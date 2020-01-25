from .user import UserAPI
from .user import UserAPIWeightDatatable
from .user_datatables import *

def register_views(app, base):
    UserAPIWeightDatatable.register(app, route_base=base)
    UserAPI.register(app, route_base=base)
    UserAPIWeightDatatablePeek.register(app, route_base=base)
    UserAPIMeasureDatatablePeek.register(app, route_base=base)
