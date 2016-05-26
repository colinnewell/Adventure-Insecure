from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort

from app.menus.models import Menu

menus = Blueprint('menus', __name__, url_prefix='/menus')

# FIXME: create a regular upload too.

# FIXME: ensure they are logged in,
# heck, we should make sure they are an admin.
@menus.route('/bulk_upload', methods=['GET', 'POST'])
def bulk_upload():
    user = session['user_id']
    form = BulkUploadForm(request.form)
    if form.validate_on_submit():
        # take the zip file
        # and upload the pdfs
        pass
    return render_template('menus/upload.html', form=form)

