from .recaptcha import RecaptchaAPI


def register_views(app, base):
    RecaptchaAPI.register(app, route_base=base)
