from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for

from werkzeug import check_password_hash, generate_password_hash

from app.auth.models import User
from app.auth.forms import LoginForm

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('auth.home'))
        flash('Incorrect email or password', 'error-message')
    return render_template('auth/login.html', form=form)
