from flask import request, redirect, url_for, session, abort
from functools import wraps
from app import db
from app.auth.models import User


EXEMPT_METHODS = set(['OPTIONS'])

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif 'user_id' not in session or not session['user_id']:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_view

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif 'user_id' not in session or not session['user_id']:
            return redirect(url_for('auth.login'))
        user_id = session['user_id']
        u = User.query.filter_by(id=session['user_id']).one()
        if u and u.admin:
            return func(*args, **kwargs)
        abort(404)

    return decorated_view


