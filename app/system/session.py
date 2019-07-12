from flask import session, current_app, request, abort
from flask_pymongo import MongoClient
from flask_mongoengine import connection


app = current_app

def set_session(user_obj):
    session['username'] = user_obj.username
    session['email'] = user_obj.email
    session['groups'] = user_obj.groups

def clear_session():
    sid = request.cookies.get(app.session_cookie_name)
    store = get_store()
    store.delete_one({'_id': sid})
    session.clear()

def get_store():
    db = connection.get_connection_settings(app.config)
    store = MongoClient(db.get("host"), db.get("port"))
    return store[db.get("name")]['session']

def is_loggedin():
    if session:
        if session['username']:
            return True
    return False

def get_current_user():
    from app.models import Users
    if session:
        if session['username']:
            return Users.by_username(session['username'])
        abort(403)
