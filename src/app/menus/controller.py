from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort, current_app
from werkzeug import secure_filename
from app.auth.utils import login_required
from app.menus.models import Menu
from app.menus.forms import BulkUploadForm, MenuAdminForm
from zipfile import ZipFile
from tarfile import TarFile
import os

menus = Blueprint('menus', __name__, url_prefix='/menus')


# FIXME: create a regular upload too.

# FIXME: ensure they are logged in,
# heck, we should make sure they are an admin.
@menus.route('/bulk_upload', methods=['GET', 'POST'])
@login_required
def bulk_upload():
    form = BulkUploadForm(request.form)
    if form.validate_on_submit() and 'menu' in request.files:
        file = request.files['menu']
        filename = secure_filename(file.filename)
        if filename.endswith(".zip"):
            with ZipFile(file, mode='r') as z:
                # FIXME: get path from config.
                z.extractall(current_app.config['UPLOAD_FOLDER'])
        # FIXME: allow zipped tarballs too.
        # .tgz, .tar.gz, .tar.bz2, tar.xz?
        elif filename.endswith(".tar"):
            # do a path combine
            # save this in a temporary path
            # and clean it up when we're done.
            local_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(local_filename)
            with TarFile.open(local_filename, mode='r') as t:
                # FIXME: get path from config.
                t.extractall(current_app.config['UPLOAD_FOLDER'])
        else:
            # add a validation error.
            pass
    return render_template('menus/upload.html', form=form)

@menus.route('/menu_admin', methods=['GET', 'POST'])
@login_required
def menu_admin():
    pass
