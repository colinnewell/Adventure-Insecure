from flask_wtf import Form
from wtforms import StringField, SubmitField
from app.auth.forms import OwnCSRF


class OrderForm(OwnCSRF, Form):
    title = StringField('Order')
    submit = SubmitField('Add')


class OrderLineForm(OwnCSRF, Form):
    request = StringField('Request')
    submit = SubmitField('Add')
