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
