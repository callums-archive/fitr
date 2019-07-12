from flask import session, current_app, request, abort
from flask_pymongo import MongoClient
from flask_mongoengine import connection, MongoEngineSession, MongoEngine

# from fitr_webapp import




app = current_app()
db=MongoEngine(app)

def set_session(user_obj):
    session['username'] = user_obj.username
    session['email'] = user_obj.email
    session['groups'] = user_obj.groups

def clear_session():
    get_store()
    # sid = request.cookies.get(app.session_cookie_name)
    # sessions = MongoEngineSession(sid=sid)
    # # sessions.delete()
    # store = get_store()
    # store.delete_one({'_id': sid})
    # session.clear()

def get_store():
    print(db.connection())
    # db = connection.get_connection_settings(app.config)
    # store = MongoClient(db.get("host"), db.get("port"))
    # return store[db.get("name")]['session']

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
