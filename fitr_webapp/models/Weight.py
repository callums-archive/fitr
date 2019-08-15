# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime

# exceptions
from fitr_webapp.system.exceptions import DBError


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
