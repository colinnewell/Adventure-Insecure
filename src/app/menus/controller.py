from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort, current_app
from flask.helpers import send_from_directory
from werkzeug import secure_filename
from app.auth.utils import login_required
from app.menus.models import Menu
from app.menus.forms import BulkUploadForm, MenuAdminForm
from zipfile import ZipFile
from tarfile import TarFile
import os
import magic
from shutil import move


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

        # check for new files, are they pdf's?
        for root, dirs, files in os.walk(current_app.config['UPLOAD_FOLDER']):
            for name in files:
                fullname = os.path.join(root, name)
                info = magic.from_file(fullname)
                if 'PDF' in info:
                    # lets do something
                    # move the file
                    # create a Menu object.
                    print("Use " + fullname)
                    move(fullname, current_app.config['MENUS_FOLDER'])
                    # FIXME: create a menu object.
                else:
                    print("Whine about " + fullname)
                    # reject the file.
                # can we see pdf's
                # move them to a special directory within static.

    return render_template('menus/upload.html', form=form)



@menus.route('/menu/<path:filename>', methods=['GET'])
@login_required
def menu(filename):
    return send_from_directory(current_app.config['MENUS_FOLDER'],
                               filename, as_attachment=False)


@menus.route('/menu_admin', methods=['GET', 'POST'])
@login_required
def menu_admin():
    pass
