from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Required, EqualTo, Regexp
from app.auth.forms import OwnCSRF

class MenuAdminField(Form):
    description = StringField('Description')
    delete = BooleanField('Delete')


class MenuAdminForm(OwnCSRF, Form):
    menu = FileField('Menus')
    submit = SubmitField('Upload')

class BulkUploadForm(OwnCSRF, Form):
    menu = FileField('Menus')
    submit = SubmitField('Upload')
