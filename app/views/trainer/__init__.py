from .capture import PTCaptureView


def register_views(app, base):
    PTCaptureView.register(app, route_base="/capture/")
