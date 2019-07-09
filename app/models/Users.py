# flask
from flask_mongoengine import MongoEngine
from flask import session

# std
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime

# models
from .Groups import Groups

# system
from app.system.exceptions import DBError
from app.system.session import set_session


db = MongoEngine()


class Users(db.Document):
    username = db.StringField()
    email = db.StringField()
    password = db.StringField()
    groups = db.ListField(db.StringField())

    create_user = db.ReferenceField("Users")
    create_stamp = db.DateTimeField(default=datetime.utcnow)

    modified_user = db.ReferenceField("Users")
    modified_stamp = db.DateTimeField()

    @classmethod
    def by_username(cls, username):
        return cls.objects.filter(username=username).first()

    @classmethod
    def create_user(cls, username, password, email, groups=['logged_in']):
        user = None
        try:
            if cls.by_username(username) is not None:
                raise DBError("Username exists!")

            user = cls(username=username, email=email)
            for group in groups:
                user.add_group(group)
            user.set_password(password)
            user.save()
            return user.to_json()
        except Exception as e:
            if user and user.to_dbref() is not None:
                Users.by_username(username).delete()
            raise(Exception(e))
            

    def add_group(self, group):
        if not Groups.by_name(group):
            raise DBError("Group is invalid")
        self.groups.append(group)
        self.save()
        return True

    def remove_group(self, group):
        if not Groups.by_name(group):
            raise DBError("Group is invalid")
        self.groups.remove(group)
        self.save()
        return True

    def set_password(self, password):
        hash = hashpw(str(password).encode("utf-8"), gensalt())
        self.password = hash.decode("utf-8")
        self.save()
        return True

    def check_password(self, password):
        if checkpw(password.encode("utf-8"), self.password.encode("utf-8")):
            return True
        return False

    @classmethod
    def login(cls, username, password):
        user = cls.by_username(username)
        if not user:
            raise DBError("Username/Password combination failed.")
        if not user.check_password(password):
            raise DBError("Username/Password combination failed.")

        set_session(user)
        return True

