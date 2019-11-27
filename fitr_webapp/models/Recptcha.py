# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime
from time import mktime

# exceptions
from fitr_webapp.system.exceptions import DBError

# system
import fitr_webapp.system.datetimetools as datetimetools


db = MongoEngine()


class Captcha(db.Document):
    uid = db.SequenceField()

    user = db.ReferenceField("Users")
    ip = db.StringField()

    action = db.StringField()

    create_stamp = db.DateTimeField(default=datetime.utcnow)

    @classmethod
    def create_record(cls, action, ip=None, user=None):
        rec = cls()
        rec.ip = ip
        rec.user = user
        rec.action = action
        rec.save()
        return True

    @classmethod
    def by_ip(cls, ip, action=None):
        if action is None:
            return cls.objects.filter(ip=ip).order_by("-create_stamp")
        else:
            return cls.objects.filter(ip=ip, action=action).order_by("-create_stamp")

    @property
    def recall(self):
        now = mktime(datetime.utcnow().timetuple())
        record = mktime(self.create_stamp.timetuple())
        res = now - record

        self.delete()

        if res > 5:
            return False
        return True