# flask
from flask_mongoengine import MongoEngine
from flask import request

# std
from datetime import datetime

# system
from fitr_webapp.system.ip import get_ip

# exceptions
from fitr_webapp.system.exceptions import DBError


db = MongoEngine()


class Logins(db.Document):
    uid = db.SequenceField()
    user = db.ReferenceField("Users")
    session = db.StringField(required=True)

    in_ip = db.StringField()
    in_stamp = db.DateTimeField(default=datetime.utcnow)
    in_platform = db.StringField()
    in_browser = db.StringField()
    in_version = db.StringField()
    in_language = db.StringField()
    in_user_agent_string = db.StringField()

    out_ip = db.StringField()
    out_stamp = db.DateTimeField()
    out_platform = db.StringField()
    out_browser = db.StringField()
    out_version = db.StringField()
    out_language = db.StringField()
    out_user_agent_string = db.StringField()

    @classmethod
    def by_session(cls, session):
        return cls.objects(session=session).first()

    @classmethod
    def new_login(cls, user, sid):
        new_record = cls()
        new_record.user = user.to_dbref()
        new_record.in_ip = get_ip()
        new_record.in_platform = request.user_agent.platform
        new_record.in_browser = request.user_agent.browser
        new_record.in_version = request.user_agent.version
        new_record.in_language = request.user_agent.language
        new_record.in_user_agent_string = request.user_agent.string
        new_record.session = sid
        new_record.save()
        return True

    @classmethod
    def conclude(cls, sid):
        record = cls.by_session(sid)
        record.out_platform = request.user_agent.platform
        record.out_browser = request.user_agent.browser
        record.out_version = request.user_agent.version
        record.out_language = request.user_agent.language
        record.out_user_agent_string = request.user_agent.string
        record.out_stamp = datetime.utcnow()
        record.out_ip = get_ip()
        record.save()
        return True
