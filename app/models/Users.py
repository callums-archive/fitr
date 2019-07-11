# flask
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q

# std
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime

# models
from .Groups import Groups

# system
from app.system.exceptions import DBError
from app.system.session import set_session

import app.system.datetimetools as datetimetools
import app.system.stringtools as stringtools


db = MongoEngine()


class Users(db.Document):
    uid = db.SequenceField()

    first_name =  db.StringField()
    surname = db.StringField()
    date_of_birth = db.DateTimeField()
    gender = db.StringField()

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
    def by_email(cls, email):
        return cls.objects.filter(email=email).first()

    @classmethod
    def create_user(cls, username, password, email, gender, date_of_birth, first_name, surname, groups=['everyone']):
        user = None
        try:
            if cls.by_username(username) is not None:
                raise DBError("Username already registered!")

            if cls.by_email(email) is not None:
                raise DBError("Email already registered!")

            user = cls(
                username=stringtools.sanitize_lower(username),
                email=stringtools.sanitize_lower(email),
                first_name=stringtools.sanitize_title(first_name),
                surname=stringtools.sanitize_title(surname),
                gender=gender,
                date_of_birth=datetimetools.parse_date(date_of_birth))
            for group in groups:
                user.add_group(group)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            if user and user.to_dbref() is not None:
                Users.by_username(username).delete()
            raise(DBError(e))

    @classmethod
    def login(cls, identifier, password):
        user = cls.objects.filter(Q(username=identifier) or Q(email=identifier)).first()
        if not user:
            print("no user")
            raise DBError("Username/Password combination failed.")
        if not user.check_password(password):
            print("passwd")
            raise DBError("Username/Password combination failed.")

        set_session(user)
        return True

    def __str__(self)            :
        return f"{self.username}:{self.groups}"

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
