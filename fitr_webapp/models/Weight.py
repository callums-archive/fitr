# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime

# exceptions
from fitr_webapp.system.exceptions import DBError

# system
import fitr_webapp.system.datetimetools as datetimetools


db = MongoEngine()


class Weight(db.Document):
    uid = db.SequenceField()
    user = db.ReferenceField("Users")

    unit = db.StringField(default="kg")
    weight = db.FloatField()

    create_user = db.ReferenceField("Users")
    create_stamp = db.DateTimeField(default=datetime.utcnow)

    modified_user = db.ReferenceField("Users")
    modified_stamp = db.DateTimeField()

    @property
    def show_weights(self):
        return {
            "unit": self.unit,
            "create_user": self.create_user.__str__(),
            "create_stamp": datetimetools.cast_string(self.create_stamp, "dt"),
            "weight": self.weight,
        }
