# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime

# system
from fitr_webapp.system.exceptions import DBError
from fitr_webapp.system.session import set_session, is_loggedin, get_current_user


db = MongoEngine()

class Measurements(db.EmbeddedDocument):
    uid = db.SequenceField()

    unit = db.StringField(default="cm")
    neck = db.FloatField()
    bicep = db.FloatField()
    chest = db.FloatField()
    abs1 = db.FloatField()
    abs1_comment = db.StringField()
    abs2 = db.FloatField()
    abs2_comment = db.StringField()
    abs3 = db.FloatField()
    abs3_comment = db.StringField()
    upperthigh = db.FloatField()
    midthigh = db.FloatField()
    calf = db.FloatField()

    create_user = db.ReferenceField("Users")
    create_stamp = db.DateTimeField(default=datetime.utcnow)


class Weight(db.EmbeddedDocument):
    uid = db.SequenceField()

    unit = db.StringField(default="kg")
    weight = db.FloatField()

    create_user = db.ReferenceField("Users")
    create_stamp = db.DateTimeField(default=datetime.utcnow)

class FitnessTests(db.EmbeddedDocument):
    uid = db.SequenceField()

    name = db.StringField()
    data = db.DictField()

    create_user = db.ReferenceField("Users")
    create_stamp = db.DateTimeField(default=datetime.utcnow)


class AuthSessions(db.EmbeddedDocument):
    uid = db.SequenceField()
    session_id = db.StringField()

    login_ip = db.StringField()
    login_stamp = db.DateTimeField(default=datetime.utcnow)
    login_platform = db.StringField()
    login_browser = db.StringField()
    login_version = db.StringField()
    login_language = db.StringField()
    login_user_agent_string = db.StringField()

    logout_ip = db.StringField()
    logout_stamp = db.DateTimeField()
    logout_platform = db.StringField()
    logout_browser = db.StringField()
    logout_version = db.StringField()
    logout_language = db.StringField()
    logout_user_agent_string = db.StringField()
