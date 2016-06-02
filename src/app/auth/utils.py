from flask import request, redirect, url_for, session
from functools import wraps


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


