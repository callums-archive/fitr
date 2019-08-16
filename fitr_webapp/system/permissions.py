# flask and std
from flask import abort, session
from functools import wraps

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


def permission(permission_name):
    def check_perm(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if has_permission(permission_name):
                print(f"Permission {permission_name} granted")
                return f(*args, **kwargs)
            abort(403)
        return wrap
    return check_perm
