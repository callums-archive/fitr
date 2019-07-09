# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime

# exceptions
from app.system.exceptions import DBError


db = MongoEngine()


class Groups(db.Document):
    name = db.StringField()

    create_user = db.ReferenceField("Users")
    create_stamp = db.DateTimeField(default=datetime.utcnow)

    modified_user = db.ReferenceField("Users")
    modified_stamp = db.DateTimeField()

    @classmethod
    def create_group(cls, name):
        if cls.by_name(name):
            raise DBError("Group already exists!")
        group = cls(name=name)
        group.save()
        return group.to_json()

    @classmethod
    def by_name(cls, name):
        return cls.objects.filter(name=name).first()
