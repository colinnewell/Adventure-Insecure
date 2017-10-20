from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FieldList, FormField
from flask_wtf.file import FileField
from app.auth.forms import OwnCSRF


class MenuAdminField(FlaskForm):
    filename = StringField('Filename', render_kw={'readonly': "readonly"})
    link_text = StringField('Description')
    delete = BooleanField('Delete')


class MenuAdminForm(OwnCSRF, FlaskForm):
    menus = FieldList(FormField(MenuAdminField, label=''))
    submit_it = SubmitField('Save')

class BulkUploadForm(OwnCSRF, FlaskForm):
    menu = FileField('Menus')
    submit = SubmitField('Upload')
