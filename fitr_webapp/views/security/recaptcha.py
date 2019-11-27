from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    jsonify
)

from flask_classy import route

from fitr_webapp.models.Recptcha import Captcha

from fitr_webapp.system.exceptions import DBError

from fitr_webapp.system.view_helpers import Base

from fitr_webapp.system.permissions import permission, has_permission
from fitr_webapp.system.session import clear_session
from fitr_webapp.system.ip import get_ip

import requests
from flask import current_app as app

actions = [
    "register", # user registration
    "login", # user login
    "forgot" # forgot password interface
]

class RecaptchaAPI(Base):
    @route('/', methods=["POST"])
    def index(self):
        token = self.data.get("___g-recaptcha-token___")
        secret = app.config.get("CAPTCHA_SECRET")
        action = self.request.referrer.split("/").pop()

        resp = requests.post("https://www.google.com/recaptcha/api/siteverify", {
            "secret": secret,
            "response": token
        })

        res_j = resp.json()
        if res_j['success'] and res_j['action'] in actions and res_j['action'] == action:
            Captcha.create_record(res_j['action'], ip=get_ip(), user=self.request.user)
        return jsonify(res_j)
