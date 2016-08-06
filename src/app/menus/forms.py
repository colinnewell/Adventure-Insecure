from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, FieldList, FormField, HiddenField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Required, EqualTo, Regexp
from app.auth.forms import OwnCSRF


class MenuAdminField(Form):
    filename = StringField('Filename', render_kw={'readonly': "readonly"})
    link_text = StringField('Description')
    delete = BooleanField('Delete')


class MenuAdminForm(OwnCSRF, Form):
    menus = FieldList(FormField(MenuAdminField, label=''))
    submit_it = SubmitField('Save')

class BulkUploadForm(OwnCSRF, Form):
    menu = FileField('Menus')
    submit = SubmitField('Upload')
