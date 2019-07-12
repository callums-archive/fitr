# flask
from flask import abort, session

# acls
from .acls import generate_acl, Allow, Deny

# session
from .session import get_current_user


def has_permission(permission):
    user = get_current_user()
    if user is None:
        return False
    permissions = generate_acl(user.groups)
    for permission_list in permissions:
        if permission_list[1] == permission and permission_list[0] == Allow:
            return True
    return False

class permission():
    def __init__(self, permission):
        self.permission = permission

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            if has_permission(self.permission):
                return f(*args, **kwargs)
            abort(403)
        return wrapped_f
