from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, FieldList, FormField, HiddenField
from app.auth.forms import OwnCSRF
from flask import request


class SearchForm(OwnCSRF, Form):

    phone_number = StringField('Phone Number') # FIXME: make it requried
    submit = SubmitField('Search')

    def is_submitted(self):
        return request and request.method == 'GET'

