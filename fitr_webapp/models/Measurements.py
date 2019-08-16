# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime

# exceptions
from fitr_webapp.system.exceptions import DBError

# system
import fitr_webapp.system.datetimetools as datetimetools

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

    @property
    def show_measurements(self):
        return {
            "unit": self.unit,
            "create_user": self.create_user.__str__(),
            "create_stamp": datetimetools.cast_string(self.create_stamp, "dt"),
            "neck": self.neck,
            "bicep": self.bicep,
            "chest": self.chest,
            "abs1": self.abs1,
            "abs1_comment": self.abs1_comment,
            "abs2": self.abs2,
            "abs2_comment": self.abs2_comment,
            "abs3": self.abs3,
            "abs3_comment": self.abs3_comment,
            "upperthigh": self.upperthigh,
            "midthigh": self.midthigh,
            "calf": self.calf,
        }
