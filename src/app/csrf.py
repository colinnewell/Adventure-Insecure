import hmac
import hashlib
import time
import random
from flask import current_app, session
from flask_wtf._compat import to_bytes
from werkzeug.security import safe_str_cmp


def generate_csrf(secret_key=None, time_limit=None, token_key=None):
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

    if time_limit:
        expires = int(time.time() + time_limit)
        csrf_build = '%s:%s' % (expires, random.getrandbits(32))
    else:
        expires = ''
        csrf_build = '%s:%s' % (expires, random.getrandbits(32))

    hmac_csrf = hmac.new(
        to_bytes(secret_key),
        to_bytes(session.sid + csrf_build),
        digestmod=hashlib.sha1
    ).hexdigest()
    return '%s##%s' % (csrf_build, hmac_csrf)


def validate_csrf(data, secret_key=None, time_limit=None):
    """Check if the given data is a valid csrf token.

    :param data: The csrf token value to be checked.
    :param secret_key: A secret key for mixing in the token,
                       default is Flask.secret_key.
    :param time_limit: Check if the csrf token is expired.
                       default is True.
    """
    if not data or '##' not in data:
        return False

    try:
        csrf_build, hmac_csrf = data.split('##', 1)
        expires, _ = csrf_build.split(':', 1)
    except ValueError:
        return False  # unpack error

    if time_limit is None:
        time_limit = current_app.config.get('WTF_CSRF_TIME_LIMIT', 3600)

    if time_limit:
        try:
            expires = int(expires)
        except ValueError:
            return False

        now = int(time.time())
        if now > expires:
            return False

    if not secret_key:
        secret_key = current_app.config.get(
            'WTF_CSRF_SECRET_KEY', current_app.secret_key
        )

    hmac_compare = hmac.new(
        to_bytes(secret_key),
        to_bytes(session.sid + csrf_build),
        digestmod=hashlib.sha1
    ).hexdigest()

    return safe_str_cmp(hmac_compare, hmac_csrf)
