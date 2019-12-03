# # flask
# from flask_mongoengine import MongoEngine

# # std
# from datetime import datetime

# # exceptions
# from fitr_webapp.system.exceptions import DBError

# # system
# import fitr_webapp.system.datetimetools as datetimetools

# db = MongoEngine()


# class MeasurementTemplates(db.Document):
#     uid = db.SequenceField()

#     name = db.StringField()
#     fields = db.DictField()
#     unit = db.StringField()

#     create_user = db.ReferenceField("Users")
#     create_stamp = db.DateTimeField(default=datetime.utcnow)

#     modified_user = db.ReferenceField("Users")
#     modified_stamp = db.DateTimeField()


# class CapturedMeasurements(db.Document):
#     uid = db.SequenceField()
#     user = db.ReferenceField("Users")

#     template = db.ReferenceField("MeasurementTemplates")
#     actuals = db.DictField()
#     comment = db.StringField()

#     create_user = db.ReferenceField("Users")
#     create_stamp = db.DateTimeField(default=datetime.utcnow)

#     modified_user = db.ReferenceField("Users")
#     modified_stamp = db.DateTimeField()

#     @classmethod
#     def by_uid(cls, uid):
#         return cls.objects.filter(user=uid).order_by('-create_stamp').all()

#     @classmethod
#     def by_uid_latest(cls, uid):
#         return cls.objects.filter(user=uid).order_by('-create_stamp').first()

#     @classmethod
#     def by_uid_initial(cls, uid):
#         return cls.objects.filter(user=uid).order_by('create_stamp').first()

#     @classmethod
#     def get_difference(cls, uid):
#         return {"diff": cls.by_uid_initial(uid).to_dict['facts']['total'] - cls.by_uid_latest(uid).to_dict['facts']['total'],
#                 "unit": cls.by_uid_latest(uid).to_dict['facts']['unit']}

#     @property
#     def to_dict(self):
#         fields = []
#         total = 0.0
#         for field in self.template.fields:
#             dict_field = {}
#             dict_field = self.template.fields[field]
#             dict_field.update(self.actuals[field])
#             total+=self.actuals[field]["value"]
#             fields.append(dict_field)
#         return {
#             "fields": fields,
#             "facts": {
#                 "unit": self.template.unit,
#                 "total": total,
#                 "create_stamp": self.create_stamp,
#                 "create_user": {"full_name": self.create_user.full_name, "username": self.create_user.username}
#             }
#         }

# class Measurements(db.Document):
#     uid = db.SequenceField()
#     user = db.ReferenceField("Users")

#     unit = db.StringField(default="cm")
#     neck = db.FloatField()
#     bicep = db.FloatField()
#     chest = db.FloatField()

#     abs1 = db.FloatField()
#     abs1_comment = db.StringField()

#     abs2 = db.FloatField()
#     abs2_comment = db.StringField()

#     abs3 = db.FloatField()
#     abs3_comment = db.StringField()

#     upperthigh = db.FloatField()
#     midthigh = db.FloatField()
#     calf = db.FloatField()

#     create_user = db.ReferenceField("Users")
#     create_stamp = db.DateTimeField(default=datetime.utcnow)

#     modified_user = db.ReferenceField("Users")
#     modified_stamp = db.DateTimeField()



#     @property
#     def show_measurements(self):
#         ac1 = {}
#         ac2 = {}
#         ac3 = {}

#         ac1["value"] = self.abs1
#         ac2["value"] = self.abs2
#         ac3["value"] = self.abs3

#         if len(self.abs1_comment) > 0:
#             ac1['comment'] = self.abs1_comment

#         if len(self.abs2_comment) > 0:
#             ac2['comment'] = self.abs2_comment

#         if len(self.abs3_comment) > 0:
#             ac3['comment'] = self.abs3_comment

#         if self.upperthigh is not None:
#             return {
#                 # "unit": self.unit,
#                 "create_stamp": datetimetools.cast_string(self.create_stamp, "dt"),
#                 "value": {
#                 "0": {"value": self.neck},
#                 "1": {"value": self.bicep},
#                 "2": {"value": self.chest},
#                 "3": ac1,
#                 "4": ac2,
#                 "5": ac3,
#                 "6": {"value": self.upperthigh},
#                 "7": {"value": self.midthigh},
#                 "8": {"value": self.calf},
#                 }
#             }
#         else:
#             return {
#                 # "unit": self.unit,
#                 "create_stamp": datetimetools.cast_string(self.create_stamp, "dt"),
#                 "value": {
#                 "0": {"value": self.neck},
#                 "1": {"value": self.bicep},
#                 "2": {"value": self.chest},
#                 "3": {"value": self.abs1, "comment": self.abs1_comment},
#                 "4": {"value": self.abs2, "comment": self.abs2_comment},
#                 "5": {"value": self.abs3, "comment": self.abs3_comment},
#                 "6": {"value": self.midthigh},
#                 "7": {"value": self.calf},
#                 }
#             }

#                 def show_measurements(self):
#         if self.upperthigh is not None:
#             return {
#                 # "unit": self.unit,
#                 "create_stamp": datetimetools.cast_string(self.create_stamp, "dt"),
#                 "value": {
#                 "neck": {"value": self.neck},
#                 "bicep": {"value": self.bicep},
#                 "chest": {"value": self.chest},
#                 "abs1": {"value": self.abs1, "comment": self.abs1_comment},
#                 "abs2": {"value": self.abs2, "comment": self.abs2_comment},
#                 "abs3": {"value": self.abs3, "comment": self.abs3_comment},
#                 "upperthigh": {"value": self.upperthigh},
#                 "midthigh": {"value": self.midthigh},
#                 "calf": {"value": self.calf},
#                 }
#             }
#         else:
#             return {
#                 # "unit": self.unit,
#                 "create_stamp": datetimetools.cast_string(self.create_stamp, "dt"),
#                 "value": {
#                 "neck": {"value": self.neck},
#                 "bicep": {"value": self.bicep},
#                 "chest": {"value": self.chest},
#                 "abs1": {"value": self.abs1, "comment": self.abs1_comment},
#                 "abs2": {"value": self.abs2, "comment": self.abs2_comment},
#                 "abs3": {"value": self.abs3, "comment": self.abs3_comment},
#                 "midthigh": {"value": self.midthigh},
#                 "calf": {"value": self.calf},
#                 }
#             }

        
#     @property
#     def total(self):
#         return f"dfg"

#     @classmethod
#     def add_measurement(cls, user, neck, bicep, chest, abs1, abs1_comment, abs2, abs2_comment, abs3, abs3_comment, upperthigh, midthigh, calf):
#         row = cls(
#             user = user,
#             neck=float(neck),
#             bicep=float(bicep),
#             chest=float(chest),
#             abs1=float(abs1),
#             abs1_comment=str(abs1_comment),
#             abs2=float(abs2),
#             abs2_comment=str(abs2_comment),
#             abs3=float(abs3),
#             abs3_comment=str(abs3_comment),
#             upperthigh=float(upperthigh),
#             midthigh=float(midthigh),
#             calf=float(calf),
#         )

#         row.save()
#         return True

#     @classmethod
#     def by_username(cls, uid):
#         return cls.objects.filter(user=uid).order_by('create_stamp')


# flask
from flask_mongoengine import MongoEngine

# std
from datetime import datetime

# exceptions
from fitr_webapp.system.exceptions import DBError

# system
import fitr_webapp.system.datetimetools as datetimetools

db = MongoEngine()


class Measurements(db.Document):
    uid = db.SequenceField()
    user = db.ReferenceField("Users")

    unit = db.StringField(default="cm")
    neck = db.FloatField()
    bicep = db.FloatField()
    chest = db.FloatField()

    abs1 = db.FloatField()
    abs1_comment = db.StringField()

    abs2 = db.FloatField()
    abs2_comment = db.StringField()

    abs3 = db.FloatField()
    abs3_comment = db.StringField()

    upperthigh = db.FloatField()
    midthigh = db.FloatField()
    calf = db.FloatField()

    create_user = db.ReferenceField("Users")
    create_stamp = db.DateTimeField(default=datetime.utcnow)

    modified_user = db.ReferenceField("Users")
    modified_stamp = db.DateTimeField()

    @property
    def show_measurements(self):
        return {
            "unit": self.unit,
            "create_user": self.create_user.__str__(),
            "create_stamp": datetimetools.cast_string(self.create_stamp, "dt"),
            "neck": self.neck,
            "bicep": self.bicep,
            "chest": self.chest,
            "abs1": self.abs1,
            "abs1_comment": self.abs1_comment,
            "abs2": self.abs2,
            "abs2_comment": self.abs2_comment,
            "abs3": self.abs3,
            "abs3_comment": self.abs3_comment,
            "upperthigh": self.upperthigh,
            "midthigh": self.midthigh,
            "calf": self.calf,
        }

    @classmethod
    def add_measurement(cls, user, neck, bicep, chest, abs1, abs1_comment, abs2, abs2_comment, abs3, abs3_comment, upperthigh, midthigh, calf):
        row = cls(
            user = user,
            neck=float(neck),
            bicep=float(bicep),
            chest=float(chest),
            abs1=float(abs1),
            abs1_comment=str(abs1_comment),
            abs2=float(abs2),
            abs2_comment=str(abs2_comment),
            abs3=float(abs3),
            abs3_comment=str(abs3_comment),
            upperthigh=float(upperthigh),
            midthigh=float(midthigh),
            calf=float(calf),
        )

        row.save()
        return True