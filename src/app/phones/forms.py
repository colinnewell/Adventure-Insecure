from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from app.auth.forms import OwnCSRF
from flask import request


class SearchForm(OwnCSRF, Form):

    phone_number = StringField('Phone Number', [Required(message='Specify a number to look up')])
    submit = SubmitField('Search')

    def is_submitted(self):
        return request \
                and request.method == 'GET' \
                and 'submit' in request.args
