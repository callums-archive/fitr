# class defs
class Allow():
    pass

class Deny():
    pass

class Permission(list):
    pass


# acls
acls = {}

acls["everyone"] = [
    Permission([Allow, "dashboard"]),
    Permission([Allow, "profile"]),
]

acls["admin"] = [
    acls["everyone"]
]


# acl expose per user
def generate_acl(level):
    permissions = []
    def process_permissions_obj(item):
        result = []
        if type(item) == type(list()):
            for perm in item:
                result.extend(process_permissions_obj(perm))
        elif type(item) == type(Permission()):
            result.append(item)
        return result

    for acl in acls:
        for permission in acls[acl]:
            if acl == level:
                permissions.extend(process_permissions_obj(permission))
    return permissions
