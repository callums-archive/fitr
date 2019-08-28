from flask import (
    abort
)

from . import Base

from datetime import datetime

from flask import current_app as app

class FormValidation(Base):

    def __init__(self):
        super(FormValidation, self).__init__()

    def validate_x(self, field=None, strict=True, prefix=""):
        # check to see if the filed element has been added
        if field is not None:
            self.data[field['name']] = field['value']

        # set strict
        self.strict = strict

        def process_x(vfield):
            # standardize input
            vfield = dict(vfield)

            self.key = next(iter(vfield))
            self.val = vfield[self.key]

            try:
                return getattr(self, f"{prefix}validate_{self.key}")(self.val)
            except Exception as e:
                if self.strict:
                    print(f"***\nVALIDATION ISSUE:\n{e}\n***")
                    return 0, f"There was an issue attepting to validate the field {self.key}."
                return 1, ""

        if len(self.data) == 1:
            # validate the one field
            opfield = process_x(self.data)
            if opfield[0] == 0:
                return 0, opfield[1]
            return {'field': self.key, 'valid': True}

        elif len(self.data) > 1:
            # validate multiple fields
            op = []
            for vfield in self.data:
                opfield = process_x({vfield:self.data[vfield]})
                if opfield[0] == 0:
                    op.append(opfield[1])
            if len(op) > 0:
                return {'valid': False, 'issues': op}
            return {'valid': True}

    def process_inline(self, prefix=""):
        if prefix != "":
            prepend = prefix + "_"
            validation = self.validate_x(prefix=prepend)
        else:
            prepend = ""
            validation = self.validate_x()

        if validation['valid']:
            try:
                update_op = self.update_x(prepend)
                if update_op and self.context:
                    if hasattr(self.context, "modified_user"):
                        self.context.update(modified_user = self.request.user, modified_stamp = datetime.utcnow())
                return update_op
            except Exception as e:
                print(f"***\nUPDATE ISSUE:\n{e}\n***")
                raise abort(412, f"There was an issue updating {self.key}")
        raise abort(412, validation['message'])

    def update_x(self, prefix):
        field = getattr(self, f"{prefix}update_{self.key}")(self.val)
        if field[0] == 1:
            return field[1]
        raise abort(412, field[1])
