from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort

from werkzeug import check_password_hash, generate_password_hash

from app.auth.models import User, SignupAttempt
from app.auth.forms import LoginForm, SignupForm, RegistrationForm

from app import db
from flask import current_app
from datetime import datetime, timedelta
from ldap3 import Server, Connection

import logging

auth = Blueprint('auth', __name__, url_prefix='/auth')


def rotate_session():
    # NOTE: this prods the underlying class
    # so this may be tied into the underlying Werkzeug class
    si = current_app.session_interface
    cache = si.cache
    cache.delete(session.sid)
    session.sid = si._generate_sid()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            password = form.password.data
            if user.ldap_auth:
                ldap = current_app.ldap
                dn = ldap.find_user_by_email(user.email)
                if dn and ldap.check_password(dn, password):
                    return successful_login(user, password)

            elif check_password_hash(user.password, password):
                return successful_login(user, password)

        flash('Incorrect email or password', 'error-message')
        logging.debug('Incorrect email or password')
    return render_template('auth/login.html', form=form)

def successful_login(user, password):
    session['user_id'] = user.id
    session['password'] = password
    flash('Welcome %s' % user.name)
    rotate_session()
    logging.debug("User %s logged in" % user.name)
    return redirect(url_for('index'))


@auth.route('/logout', methods=['POST'])
def logout():
    rotate_session()
    session['user_id'] = None
    # FIXME: rotate session
    return redirect(url_for('index'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        # lets see if the user is on ldap
        ldap_user = current_app.ldap.user_info_by_email(email, ['displayName'])
        # ['displayName']
        if ldap_user:
            name = ldap_user['attributes']['displayName'][0]
            u = User(name, email, '*****', ldap_auth=True)
            db.session.add(u)
            db.session.commit()
            flash('User account setup, login with your LDAP password', 'message')
            return redirect(url_for('auth.login'))
        elif user:
            # if the user is found send them a password reset email
            pass
        else:
            # FIXME: check for existing attempts.
            attempt = SignupAttempt.AttemptFor(email)
            db.session.add(attempt)
            db.session.commit()
            # send them a signup email.
        flash('Email sent', 'message')
    return render_template('auth/signup.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register_no_token():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        attempt = find_signup_attempt(form.token.data)
        if attempt:
            create_user(attempt, form)
            return redirect(url_for('auth.login'))
        else:
            form.token.errors.append('Unable to find registration token, perhaps it has expired.')
    return render_template('auth/register.html', form=form)


def find_signup_attempt(token):
    attempt = SignupAttempt.query.filter_by(registration_code=token).first()
    if not attempt:
        return None

    day = timedelta(days=1)
    if attempt.date_created + day < datetime.today():
        # expired.
        logging.debug("Removing expired token %s" % attempt)
        db.session.delete(attempt)
        db.session.commit()
        return None

    return attempt

def create_user(attempt, form):
    u = User(form.name.data, attempt.email, generate_password_hash(form.password.data))
    db.session.add(u)
    db.session.delete(attempt)
    db.session.commit()

@auth.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    # check for a signup attempt.
    # bounce them if it's not found.
    attempt = find_signup_attempt(token)
    if not attempt:
        abort(404)

    form = RegistrationForm(request.form)
    del form.token
    if form.validate_on_submit():
        # create new user
        # clobber the signup attempt token.
        create_user(attempt, form)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, email=attempt.email)
