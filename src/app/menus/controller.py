from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort, current_app
from flask.helpers import send_from_directory
from app import db
from werkzeug import secure_filename
from app.auth.utils import login_required
from app.menus.models import Menu
from app.menus.forms import BulkUploadForm, MenuAdminForm
from zipfile import ZipFile
from tarfile import TarFile
import os
import magic
import shutil


menus = Blueprint('menus', __name__, url_prefix='/menus')

@menus.route('/', methods=['GET'])
@login_required
def index():
    # FIXME: should order them
    menus = Menu.query.all()
    return render_template('menus/index.html', menus=menus)


# FIXME: ensure they are logged in,
# heck, we should make sure they are an admin.
@menus.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = BulkUploadForm(request.form)
    if form.validate_on_submit() and 'menu' in request.files:
        file = request.files['menu']
        filename = secure_filename(file.filename)
        errors = []
        added = []
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if filename.lower().endswith(".zip"):
            with ZipFile(file, mode='r') as z:
                # FIXME: get path from config.
                z.extractall(upload_folder)
        # FIXME: allow zipped tarballs too.
        # .tgz, .tar.gz, .tar.bz2, tar.xz?
        elif filename.lower().endswith(".tar"):
            # do a path combine
            # save this in a temporary path
            # and clean it up when we're done.
            local_filename = os.path.join(upload_folder, filename)
            file.save(local_filename)
            with TarFile.open(local_filename, mode='r') as t:
                # FIXME: get path from config.
                t.extractall(upload_folder)
        elif filename.lower().endswith(".pdf"):
            local_filename = os.path.join(upload_folder, filename)
            file.save(local_filename)
        else:
            errors.append("Please upload a pdf, zip or tar file.")

        # check for new files, are they pdf's?
        for root, dirs, files in os.walk(upload_folder):
            for name in files:
                # FIXME: check file extension too.
                fullname = os.path.join(root, name)
                info = magic.from_file(fullname)
                if 'PDF' in info and fullname.lower().endswith('.pdf'):
                    # lets do something
                    # move the file
                    # create a Menu object.
                    try:
                        shutil.move(fullname, current_app.config['MENUS_FOLDER'])
                        m = Menu(name, name, session['user_id'])
                        db.session.add(m)
                        db.session.commit()
                        added.append(m)
                    except shutil.Error as e:
                        errors.append("Unable to add {0}: {1}".format(name, e))
                        # FIXME: do something.
                    except:
                        print("Unexpected exception")
                        raise
                else:
                    errors.append("Rejected {0} because it's not a PDF".format(name))

                try:
                    # it might not still be there, being really lazy here.
                    os.remove(fullname)
                except:
                    pass
        if len(added) > 0:
            # redirect to general admin
            return redirect(url_for('menus.menu_admin'))
        else:
            flash("Failed to upload any files. " + ", ".join(errors), "error-message")

    return render_template('menus/upload.html', form=form)



@menus.route('/menu/<path:filename>', methods=['GET'])
@login_required
def menu(filename):
    return send_from_directory(current_app.config['MENUS_FOLDER'],
                               filename, as_attachment=False)


class MenuList:
    def __init__(self, menus):
        self.menus = menus

@menus.route('/menu_admin', methods=['GET', 'POST'])
@login_required
def menu_admin():
    menus = MenuList(Menu.query.all())
    form = MenuAdminForm(request.form, obj=menus)
    if form.validate_on_submit():
        fields = form.menus
        for menu in fields.entries:
            if menu.delete.data:
                menu_folder = current_app.config['MENUS_FOLDER']
                fullname = os.path.join(menu_folder, menu.filename.data)
                db.session.delete(menu.object_data)
                os.remove(fullname)
            else:
                text = menu.link_text.data
                menu.object_data.link_text = text
        db.session.commit()
        return redirect(request.path)
    return render_template('menus/menu_admin.html', form=form)
