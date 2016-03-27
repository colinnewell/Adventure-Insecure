from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort

from werkzeug import check_password_hash, generate_password_hash

from app.auth.models import User, SignupAttempt
from app.auth.forms import LoginForm, SignupForm, RegistrationForm

from app import db

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('index'))
        flash('Incorrect email or password', 'error-message')
    return render_template('auth/login.html', form=form)

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

@auth.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    # check for a signup attempt.
    # bounce them if it's not found.
    attempt = SignupAttempt.query.filter_by(registration_code=token).first()
    if not attempt:
        abort(404)
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        # create new user
        # clobber the signup attempt token.
        u = User(form.name.data, attempt.email, generate_password_hash(form.password.data))
        db.session.add(u)
        db.session.commit()
        # bounce them to login page
        # or perhaps just log them in?
        return redirect(url_for('auth.login'))
    # check expiry
    return render_template('auth/register.html', form=form, email=attempt.email)
