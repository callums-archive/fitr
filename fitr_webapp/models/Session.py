# flask
from flask_mongoengine import MongoEngine


db = MongoEngine()

class DBSession(db.Document):
    sid = db.StringField(primary_key=True)
    data = db.DictField()
    expiration = db.DateTimeField()
    meta = {
        'allow_inheritance': False,
        'collection': "session",
        'indexes': [{'fields': ['expiration'],
                     'expireAfterSeconds': 60 * 60 * 24 * 7 * 31}]
    }

    @classmethod
    def destroy_session(cls, sid):
        session = cls.objects.filter(sid=sid)
        session.delete()
        return True

    @classmethod
    def by_uid(cls, user):
        return cls.objects.filter(data__username=user).order_by('-expiration')

    @classmethod
    def by_uid_latest(cls, user):
        return cls.objects.filter(data__username=user).order_by('-expiration').first()

