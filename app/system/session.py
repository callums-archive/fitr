from flask import session, current_app, request, abort
from flask_pymongo import MongoClient


app = current_app

def set_session(user_obj):
    session['username'] = user_obj.username
    session['email'] = user_obj.email
    session['groups'] = user_obj.groups

def clear_session():
    sid = request.cookies.get(app.session_cookie_name)
    get_store().delete_one({'_id': sid})
    session.clear()

def get_store():
    store = MongoClient(app.config.get("MONGODB_HOST"), app.config.get("MONGODB_PORT"))
    return store[app.config.get("MONGODB_DB")]['session']

def get_current_user():
    from app.models import Users
    if session:
        if session['username']:
            return Users.by_username(session['username'])
        abort(403)

