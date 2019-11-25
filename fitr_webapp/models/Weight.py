# flask
from flask_mongoengine import MongoEngine
from flask import request

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

    @classmethod
    def by_uid(cls, uid):
        return cls.objects.filter(user=uid).order_by('-create_stamp').all()

    @classmethod
    def by_uid_latest(cls, uid):
        return cls.objects.filter(user=uid).order_by('-create_stamp').first()

    @classmethod
    def by_uid_initial(cls, uid):
        return cls.objects.filter(user=uid).order_by('create_stamp').first()

    @classmethod
    def get_difference(cls, uid):
        weights = cls.objects.filter(user=uid).order_by('create_stamp')
        return {"weight": round(weights[len(weights)-1].weight - weights[0].weight, 2),
                "unit": weights[0].unit}

    @classmethod
    def get_difference_previous(cls, uid):
        weights = cls.objects.filter(user=uid).order_by('create_stamp')
        return {"weight": round(weights[len(weights)-1].weight - weights[len(weights)-2].weight, 2),
                "unit": weights[0].unit}

    @property
    def show_weights(self):
        return {
            "unit": self.unit,
            "create_user": self.create_user.__str__(),
            "create_stamp": datetimetools.cast_string(self.create_stamp, "dt"),
            "weight": self.weight,
        }

    @property
    def show_weight(self):
        return f"{self.weight} {self.unit}"

    @classmethod
    def add(cls, user, weight, date=False):
        row = cls()

        try:
            row.create_stamp = datetimetools.parse_date(date)
        except:
            pass

        row.user = user
        row.weight = float(weight)
        row.create_user = request.user.to_dbref()
        row.save()
        return True
