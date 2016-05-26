from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, EqualTo, Regexp
from app.auth.forms import OwnCSRF

class BulkUploadForm(OwnCSRF, Form):
    email = FileField('Menus', [Required(message='This is required')])
    submit = SubmitField('Upload')
