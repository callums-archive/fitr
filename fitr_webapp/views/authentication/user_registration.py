from flask import (
    render_template,
    abort,
    redirect,
    url_for,
)

from flask_classy import route

from fitr_webapp.models import Users, Captcha

from fitr_webapp.system.view_helpers import FormValidation

from fitr_webapp.system.exceptions import DBError

from fitr_webapp.system import stringtools, datetimetools

from flask import current_app as app

from fitr_webapp.system.ip import get_ip


class UserRegistrationView(FormValidation):
    excluded_methods = ['validate_username', 'validate_email']

    # register interface
    @route('/register')
    def index(self):
        return render_template("authentication/register.html", captcha_site_key=app.config['CAPTCHA_SITE'])

    # register validation (AJAX)
    @route('/register_validate', methods=['POST'])
    def register_validate_post(self):
        return self.validate_x()

    # register submit user data
    @route('/register', methods=['POST'])
    def register_post(self):
        print(self.data)
        if not Captcha.by_ip(get_ip(), "register")[0].recall:
            abort(412, {"error_msg": "Failed to authenticate request. Please try again."})

        errors = self.validate_x(strict=False)

        if errors['valid'] == True:
            # create account
            try:
                Users.create_user(
                    username=self.data.get('username'),
                    password=self.data.get('password'),
                    email=self.data.get('email'),
                    gender=self.data.get('gender'),
                    date_of_birth=self.data.get('date_of_birth'),
                    first_name=self.data.get('first_name'),
                    surname=self.data.get('surname'),
                )
                return "OK"
            except DBError as e:
                abort(412, {"error_msg": str(e)})
        else:
            abort(
                412, {"error_msg": errors['issues'][0]})

    # validators
    # validate email
    def validate_email(self, val):
        if stringtools.re_email.match(val) is None:
            return 0, "Email is invalid."
        if Users.by_email(val) is not None:
            return 0, "Email already registered."
        return 1, ""

    # validate username
    def validate_username(self, val):
        if stringtools.re_username.match(val) is None:
            return 0, "Field can only consist of alphabetical charectors and numbers. Min length 3 charectors"
        if Users.by_username(val) is not None:
            return 0, "Username already registered."
        return 1, ""

    # validate gender
    def validate_gender(self, val):
        if val not in ['male', 'female']:
            return 0, "Gender is invalid."
        return 1, ""

    # validate date of birth
    def validate_date_of_birth(self, val):
        try:
            bd = datetimetools.parse_date(val)
            print(datetimetools.age_lower(bd, 13))
            print(datetimetools.age_lower(bd, 13))
            print(datetimetools.age_lower(bd, 13))
            if datetimetools.age_lower(bd, 13):
                return 0, "Age is too young."
            return 1, ""
        except Exception as e:
            return 0, "Date is incorrect."

    # validate_password
    def validate_password(self, val):
        if stringtools.re_password.match(val) is None:
            return 0, "Password needs to be minimum 8 characters, at least one letter and one number"
        return 1, ""