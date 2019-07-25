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

acls["trainer"] = [
    Permission([Allow, "pt_clients"]),
    acls["everyone"]
]

acls["admin"] = [
    Permission([Allow, "zuck"]),
    acls["everyone"],
    acls["trainer"]
]


# acl expose per user
def generate_acl(levels):
    permissions = []

    def process_permissions_obj(item):
        result = []
        if type(item) == type(list()):
            for perm in item:
                result.extend(process_permissions_obj(perm))
        elif type(item) == type(Permission()):
            result.append(item)
        return result

    for level in levels:
        for acl in acls:
            for permission in acls[acl]:
                if acl == level:
                    permissions.extend(process_permissions_obj(permission))

    return permissions
