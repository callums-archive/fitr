# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime

# exceptions
from fitr_webapp.system.exceptions import DBError


db = MongoEngine()


class Measurements(db.Document):
    uid = db.SequenceField()
    user = db.ReferenceField("Users")

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

    modified_user = db.ReferenceField("Users")
    modified_stamp = db.DateTimeField()
