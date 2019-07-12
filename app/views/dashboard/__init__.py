from .dashboard import DashboardView


def register_views(app, base):
    DashboardView.register(app, route_base=base)
