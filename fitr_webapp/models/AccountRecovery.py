# flask
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from flask import (
    url_for,
    request
)

# std
from datetime import datetime
import uuid

# system
from fitr_webapp.system.exceptions import DBError
from fitr_webapp.system.mailer import send_short_message
from fitr_webapp.system.ip import get_ip


db = MongoEngine()


class AccountRecovery(db.Document):
    uid = db.SequenceField()
    user = db.ReferenceField("Users")
    expired = db.BooleanField(default=False)
    reference = db.StringField()
    create_stamp = db.DateTimeField(default=datetime.utcnow)
    modified_stamp = db.DateTimeField()

    request_ip = db.StringField()
    request_stamp = db.DateTimeField(default=datetime.utcnow)
    request_platform = db.StringField()
    request_browser = db.StringField()
    request_version = db.StringField()
    request_language = db.StringField()
    request_user_agent_string = db.StringField()

    response_ip = db.StringField()
    response_stamp = db.DateTimeField()
    response_platform = db.StringField()
    response_browser = db.StringField()
    response_version = db.StringField()
    response_language = db.StringField()
    response_user_agent_string = db.StringField()

    @classmethod
    def search_username(cls, user):
        return cls.objects(user=user).all()

    @classmethod
    def by_key(cls, key):
        return cls.objects(reference=key).first()

    @classmethod
    def log_recovery(cls, user):
        user_search = cls.search_username(user.to_dbref())
        if user_search is not None:
            for req in user_search:
                if req.expired is False:
                    raise DBError("A reset request has already been made for this user.")

        rec = cls(user=user.to_dbref())

        rec.reference = str(uuid.uuid4())
        rec.user = user.to_dbref()

        rec.request_ip = get_ip()
        rec.request_platform = request.user_agent.platform
        rec.request_browser = request.user_agent.browser
        rec.request_version = request.user_agent.version
        rec.request_language = request.user_agent.language
        rec.request_user_agent_string = request.user_agent.string
        rec.save()

        # send recovery email
        send_short_message(user.email, "Account Recovery",
        f"Click on the link to reset you password :{url_for('UserAuthenticationView:forgot_reset_get', key=rec.reference, _external=True)}")
        return True

    @classmethod
    def process_response(cls, key):
        res = cls.by_key(key)
        if res is not None:
            if res.expired == True:
                raise DBError("Link has expired")
            return True
        return False

    @classmethod
    def finalize_response(cls, key, new_password):
        res = cls.by_key(key)
        if res is not None and res.expired is False:
            res.user.set_password(new_password)
            res.user.save()

            res.modified_stamp = datetime.utcnow()
            res.expired = True

            res.response_ip = get_ip()
            res.response_platform = request.user_agent.platform
            res.response_browser = request.user_agent.browser
            res.response_version = request.user_agent.version
            res.response_language = request.user_agent.language
            res.response_user_agent_string = request.user_agent.string

            res.save()

            # email user on success
            send_short_message(res.user.email, "Account Recovery", "New password has been set.")
            # log the user in
            from fitr_webapp.models import Users
            Users.login(res.user.username, new_password)
            return True
        raise DBError("Could not validate reset link. Could be expired. Check for password reset success email, otherwise try resetting the password again.")
