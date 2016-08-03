from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, FieldList, FormField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Required, EqualTo, Regexp
from app.auth.forms import OwnCSRF

class MenuAdminField(Form):
    filename = StringField('Filename')
    link_text = StringField('Description')
    delete = BooleanField('Delete')


class MenuAdminForm(OwnCSRF, Form):
    menus = FieldList(FormField(MenuAdminField))
    submit_it = SubmitField('Save')

class BulkUploadForm(OwnCSRF, Form):
    menu = FileField('Menus')
    submit = SubmitField('Upload')
