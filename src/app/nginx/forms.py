from flask_wtf import Form
from wtforms import SubmitField
from app.auth.forms import OwnCSRF


class ConfirmClearForm(OwnCSRF, Form):
    submit = SubmitField('Confirm')
