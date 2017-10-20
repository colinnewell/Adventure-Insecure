from flask_wtf import FlaskForm
from wtforms import SubmitField
from app.auth.forms import OwnCSRF


class ConfirmClearForm(OwnCSRF, FlaskForm):
    submit = SubmitField('Confirm')
