from flask import session, current_app, request, abort
from fitr_webapp.models.Session import DBSession


def set_session(user_obj):
    session['username'] = user_obj.username
    session['email'] = user_obj.email
    session['groups'] = user_obj.groups

def clear_session():
    session_id = request.cookies.get('session')
    print(session_id)
    DBSession.destroy_session(session_id)
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
