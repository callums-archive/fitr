from flask import session, abort
from fitr_webapp.models.Session import DBSession

from fitr_webapp.models import Users


def set_session(user_obj):
    session['username'] = user_obj.username
    session['email'] = user_obj.email
    session['groups'] = user_obj.groups
    return session.sid

def clear_session():
    user = get_current_user()
    user.logout(session.sid)
    DBSession.destroy_session(session.sid)
    session.clear()

def is_loggedin():
    if session:
        if session['username']:
            return True
    return False

def get_current_user():
    from fitr_webapp.models import Users
    if session:
        if session['username']:
            user = Users.by_username(session['username'])
            if user is not None:
                return user
    abort(403)
