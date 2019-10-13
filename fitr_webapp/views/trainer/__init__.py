from .capture import PTCaptureView
from .manage_clients import (
    TrainerManageClients,
    TrainerManageClientsDataTable
)


def register_views(app, base):
    PTCaptureView.register(app, route_base=base)
    TrainerManageClients.register(app, route_base=base)
    TrainerManageClientsDataTable.register(app, route_base=base)
