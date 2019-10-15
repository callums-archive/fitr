from .capture import PTCaptureView
from .manage_clients import *


def register_views(app, base):
    PTCaptureView.register(app, route_base=base)
    # interface for datatable
    TrainerManageClients.register(app, route_base=base)
    # datatable for trainer clients
    TrainerManageClientsDataTable.register(app, route_base=base)
    # client management api
    TrainerManageClientAPI.register(app, route_base=base)
