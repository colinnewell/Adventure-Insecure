from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, FieldList, FormField, HiddenField
from app.auth.forms import OwnCSRF


class ConfirmClearForm(OwnCSRF, Form):
    submit = SubmitField('Confirm')


