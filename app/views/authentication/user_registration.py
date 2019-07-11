from flask import (
    render_template,
    abort,
    redirect,
    url_for
)

from flask_classy import route

from app.models import Users

from app.system.view_helpers import FormValidation

from app.system.exceptions import DBError


class UserRegistrationView(FormValidation):
    excluded_methods = ['validate_username', 'validate_email']

    def index(self):
        abort(403, "Endpoint not in use.")

    @route('/register')
    def register_get(self):
        return render_template("authentication/register.html")

    @route('/register_validate', methods=['POST'])
    def register_validate_post(self):
        return self.validate_x()

    @route('/register', methods=['POST'])
    def register_post(self):
        errors = self.validate_x(strict=False)
        if errors['valid'] == True:
            # create account
            try:
                Users.create_user(
                    username = self.data.get('username'),
                    password = self.data.get('password'),
                    email = self.data.get('email'),
                    gender = self.data.get('gender'),
                    date_of_birth = self.data.get('date_of_birth'),
                    first_name = self.data.get('first_name'),
                    surname = self.data.get('surname'),
                )
                return "OK"
            except DBError as e:
                abort(412, {"error_msg": str(e)})
        else:
            abort(412, {"error_msg": "There where errors in your submitted data, please retry."})

    def validate_email(self, val):
        if Users.by_email(val) is not None:
            return 0, "Email already registered"
        return 1, ""

    def validate_username(self, val):
        if Users.by_username(val) is not None:
            return 0, "Username already registered"
        return 1, ""
