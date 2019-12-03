# flask
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from flask import (
    request,
    session,
    abort,
    url_for
)

# std
from bcrypt import (
    gensalt,
    hashpw,
    checkpw
)
from datetime import datetime
import uuid

# system
from fitr_webapp.system.exceptions import DBError
from fitr_webapp.system.session import set_session, is_loggedin, get_current_user
from fitr_webapp.system.acls import decide_context_acl
import fitr_webapp.system.datetimetools as datetimetools
import fitr_webapp.system.stringtools as stringtools

# Docuements
from fitr_webapp.models.AccountRecovery import *
from fitr_webapp.models.Groups import *
from fitr_webapp.models.Logins import *
from fitr_webapp.models.Weight import Weight
from fitr_webapp.models.Session import DBSession
# from fitr_webapp.models.Measurements import CapturedMeasurements
from fitr_webapp.models.FitnessTests import FitnessTests


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

    trainers = db.ListField(db.ReferenceField("Users"))

    @property
    def full_name(self):
        return f"{self.first_name} {self.surname}"

    @property
    def last_seen(self):
        try:
            session = DBSession.by_uid_latest(self.username)
            return session['data'].get("start_stamp", session.expiration)
        except:
            return "No Data"

    #
    # WEIGHT
    #
    @property
    def initial_weight(self):
        try:
           return Weight.by_uid_initial(self.id)
        except:
            return {"weight": "No Data", "unit": ""}

    @property
    def latest_weight(self):
        try:
            return Weight.by_uid_latest(self.id)
        except:
            return {"weight": "No Data", "unit": ""}

    @property
    def weight_difference(self):
        try:
            return Weight.get_difference(self.id)
        except:
            return {"weight": "No Data", "unit": ""}

    @property
    def weight_difference_previous(self):
        try:
            return Weight.get_difference_previous(self.id)
        except:
            return {"weight": "No Data", "unit": ""}

    #
    # MEASUREMENTS
    #
    @property
    def initial_measurement(self):
        # try:
        #     return CapturedMeasurements.by_uid_initial(self.id)
        # except:
        return "No Data"

    @property
    def latest_measurement(self):
        # try:
        #     return CapturedMeasurements.by_uid_latest(self.id)
        # except:
        return "No Data"

    @property
    def measurement_difference(self):
        # try:
        #     return CapturedMeasurements.get_difference(self.id)
        # except:
        return "No Data"

    #
    # FITNESS TESTS
    #
    @property
    def fitness_tests(self):
        return FitnessTests.by_uid(self.id)

    #
    # QUERY
    #
    @classmethod
    def by_username(cls, username):
        return cls.objects.filter(username=username).first()

    @classmethod
    def by_email(cls, email):
        return cls.objects.filter(email=email).first()

    @classmethod
    def search(cls, term, limit=5):
        q = []

        q.append({'first_name': {'$regex': "%s" % term, '$options' : 'i'}})
        q.append({'surname': {'$regex': "%s" % term, '$options' : 'i'}})
        q.append({'username': {'$regex': "%s" % term, '$options' : 'i'}})

        full_name = term.split(" ")
        if len(full_name) == 2:
            q.append({'first_name': {'$regex': "%s" % full_name[0], '$options': 'i'}, 'surname': {'$regex': "%s" % full_name[1], '$options' : 'i'}})

        q = {"$or": q}
        return cls.objects(__raw__=q).limit(limit).all()

    #
    # CREATE
    #
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
            if Users.by_username(username) is not None:
                Users.by_username(username).delete()
            raise(DBError(e))

    @classmethod
    def by_identifier(cls, identifier):
        identifiers = ['username', 'email']
        for identity in identifiers:
            res = cls.objects(__raw__={identity: identifier}).first()
            if res is not None:
                return res
        return None

    @classmethod
    def login(cls, identifier, password):
        user = cls.by_identifier(identifier)
        if not user:
            raise DBError("Invalid login credentials.")
        if not user or not user.check_password(password):
            raise DBError("Invalid login credentials.")
        sid = set_session(user)

        # log the authentication with Login
        Logins.new_login(user, sid)
        return True

    #
    # CONTEXT
    #
    @classmethod
    def serve_context(cls, username):
        user = cls.by_username(username)
        if user is None:
            abort(404)
        if request.user not in user.trainers:
            return abort(403)
        if decide_context_acl([user, user.trainers], True):
            return user
        return abort(403)

    def logout(self, sid):
        Logins.conclude(sid=sid)

    def __str__(self):
        return f"{self.full_name} (@{self.username})"

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

    def recover_account(self):
        if AccountRecovery.log_recovery(self):
            return True
