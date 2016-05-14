import hmac
import hashlib
import time
import random
import os
from flask import current_app, session
from flask_wtf._compat import to_bytes, string_types

def generate_csrf(secret_key=None, time_limit=None):
    """Generate csrf token code.

    :param secret_key: A secret key for mixing in the token,
                       default is Flask.secret_key.
    :param time_limit: Token valid in the time limit,
                       default is 3600s.
    """
    if not secret_key:
        secret_key = current_app.config.get(
            'WTF_CSRF_SECRET_KEY', current_app.secret_key
        )

    if not secret_key:
        raise Exception('Must provide secret_key to use csrf.')

    if time_limit is None:
        time_limit = current_app.config.get('WTF_CSRF_TIME_LIMIT', 3600)

    if 'csrf_token' not in session:
        session['csrf_token'] = hashlib.sha1(os.urandom(64)).hexdigest()

    if time_limit:
        expires = int(time.time() + time_limit)
        csrf_build = '%s%s' % (session['csrf_token'], expires)
    else:
        expires = ''
        csrf_build = session['csrf_token']

    hmac_csrf = hmac.new(
        to_bytes(secret_key),
        to_bytes(csrf_build),
        digestmod=hashlib.sha1
    ).hexdigest()
    return '%s##%s' % (expires, hmac_csrf)

