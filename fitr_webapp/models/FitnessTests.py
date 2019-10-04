# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime

# exceptions
from fitr_webapp.system.exceptions import DBError
from fitr_webapp.system.datetimetools import cast_string


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


    @classmethod
    def by_user(cls, user, test):
        op = dict()
        for x in cls.objects.filter(user=user).all():
            if x.name == test:
                print("HERE HERE ++++++++++++++++++++++++++++++++++++++++++++++++++")
                op[cast_string(x.create_stamp, "d")] = x.data
        return op

    @classmethod
    def capture(cls, user, test, value):
        nu = cls()

        nu.name = test
        nu.data = value
        nu.user = user.to_dbref()
        if nu.save():
            return True
        return False
