# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime

# exceptions
from fitr_webapp.system.exceptions import DBError


db = MongoEngine()


class FitnessTests(db.Document):
    uid = db.SequenceField()
    user = db.ReferenceField("Users")

    name = db.StringField()
    data = db.DictField()

    create_user = db.ReferenceField("Users")
    create_stamp = db.DateTimeField(default=datetime.utcnow)

    modified_user = db.ReferenceField("Users")
    modified_stamp = db.DateTimeField()
