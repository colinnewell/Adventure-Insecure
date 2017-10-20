from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from app.auth.forms import OwnCSRF


class OrderForm(OwnCSRF, FlaskForm):
    title = StringField('Order')
    submit = SubmitField('Add')


class OrderLineForm(OwnCSRF, FlaskForm):
    request = StringField('Request')
    submit = SubmitField('Add')
