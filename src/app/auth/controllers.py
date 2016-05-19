from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort

from werkzeug import check_password_hash, generate_password_hash

from app.auth.models import User, SignupAttempt
from app.auth.forms import LoginForm, SignupForm, RegistrationForm

from app import db
from datetime import datetime, timedelta

import logging

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            logging.debug("User %s logged in" % user.name)
            return redirect(url_for('index'))
        flash('Incorrect email or password', 'error-message')
        logging.debug('Incorrect email or password')
    return render_template('auth/login.html', form=form)

@auth.route('/logout', methods=['POST'])
def logout():
    session['user_id'] = None
    return redirect(url_for('index'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        # FIXME: check email domain.
        if user:
            # if the user is found send them a password reset email
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
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
        if not attempt:
            # FIXME: display a validation error.
            pass
        create_user(attempt, form)
        return redirect(url_for('auth.login'))
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
