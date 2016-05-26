from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort
from werkzeug import secure_filename

from app.menus.models import Menu
from app.menus.forms import BulkUploadForm

menus = Blueprint('menus', __name__, url_prefix='/menus')

# FIXME: create a regular upload too.

# FIXME: ensure they are logged in,
# heck, we should make sure they are an admin.
@menus.route('/bulk_upload', methods=['GET', 'POST'])
def bulk_upload():
    user = session['user_id']
    form = BulkUploadForm(request.form)
    import pdb; pdb.set_trace()
    if form.validate_on_submit() and form.menu.has_file():
        filename = secure_filename(form.menu.data.filename)
        form.menu.data.save('uploads/' + filename)
        # then open the menus with the zip library
        # and extract them to be served up.
        # create a Menu object.
        # take the zip file
        # and upload the pdfs
        pass
    return render_template('menus/upload.html', form=form)

