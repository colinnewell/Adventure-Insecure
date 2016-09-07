from flask import Blueprint, render_template, \
    flash, session, redirect, url_for, current_app
from app.auth.utils import admin_required
from app.nginx.forms import ConfirmClearForm
from app.auth.models import User
import pexpect
import time

import logging

nginx = Blueprint('nginx', __name__, url_prefix='/nginx')


@nginx.route('/clear_cache', methods=['GET', 'POST'])
@admin_required
def clear_cache():
    form = ConfirmClearForm()
    if form.validate_on_submit():
        # FIXME: find their username from ldap
        # and their password from the session.
        # actually we could store the username
        # in the session.
        password = session['password']
        user = User.query.filter_by(id=session['user_id']).first()
        ldap = current_app.ldap
        uinfo = ldap.user_info_by_email(user.email, ['uid'])
        if uinfo:
            username = uinfo['attributes']['uid'][0]
            command = "ssh -o StrictHostKeyChecking=no %s@ssh 'sudo find /var/cache/nginx/ -type f -exec rm {} \;'" % username
            logging.debug('Running: ' + command)
            try:
                child = pexpect.spawn(command)
                child.expect('password:')
                time.sleep(0.1)
                child.sendline(password)
                time.sleep(0.5)
                child.expect(pexpect.EOF)

                flash("Cache cleared", "message")
                return redirect(url_for('menus.index'))
            except Exception as e:
                logging.warning(e)
                flash("Failed to clear cache", "error")
        else:
            flash('Only LDAP users can use this feature', 'error')
    return render_template('nginx/clear_cache.html', form=form)
