# flask
from flask import abort, session

# acls
from .acls import generate_acl, Allow, Deny

# session
from .session import get_current_user


class permission():
    def __init__(self, permission):
        self.permission = permission

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            user = get_current_user()
            if user is None:
                abort(403)
            permissions = generate_acl(user.groups)

            for permission_list in permissions:
                if permission_list[1] == self.permission and permission_list[0] == Allow:
                    return f(*args, **kwargs)
            abort(403)
        return wrapped_f
