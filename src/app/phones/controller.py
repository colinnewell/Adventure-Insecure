from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort

from werkzeug import check_password_hash, generate_password_hash

from app.phones.models import OfficeNumber
from app.phones.forms import SearchForm

from app import db
from app.auth.utils import login_required
from flask import current_app
from sqlalchemy.sql import text


phones = Blueprint('phones', __name__, url_prefix='/phones')

@phones.route('/search', methods=['GET'])
@login_required
def search():
    form = SearchForm(request.args)
    result = {}
    if form.validate_on_submit():
        result['set'] = True
        phone = form.phone_number.data
        # FIXME: should probably order this so that we can
        # allow for more complex scenarios.
        office = OfficeNumber.query.filter(text("'%s' like '%%' || number_prefix" % phone)).first()
        if office:
            result['company'] = office

    return render_template('phones/search.html', form=form, result=result)
