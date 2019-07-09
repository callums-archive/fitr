# flask
from flask import abort

# acls
from .acls import generate_acl, Allow, Deny


class permission():
    def __init__(self, acl):
        self.acl = acl


    def __call__(self, f):
        # abort(403)

        print(type(f))

        def wrapped_f(*args, **kwargs):
            abort(403)
            if not g.role in self.acl[request.method]:
                pass
            return f(*args, **kwargs)
        return wrapped_f