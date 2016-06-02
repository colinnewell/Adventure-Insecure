from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Required, EqualTo, Regexp
from app.auth.forms import OwnCSRF

class BulkUploadForm(OwnCSRF, Form):
    menu = FileField('Menus')
    submit = SubmitField('Upload')
