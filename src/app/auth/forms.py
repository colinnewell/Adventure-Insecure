from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Email, EqualTo
from app.csrf import generate_csrf


class LoginForm(Form):
    email = StringField('Email Address', [Email(),
                      Required(message='This is required')])
    password = PasswordField('Password',
                             [Required(message='Must specify a password')])
    submit = SubmitField('Login')

    # actually uses env/lib/python3.5/site-packages/flask_wtf/form.py
    def generate_csrf_token(self, csrf_context):
        if not self.csrf_enabled:
            return None
        return generate_csrf(self.SECRET_KEY, self.TIME_LIMIT)


class SignupForm(Form):
    email = StringField('Email Address', [Email(),
                      Required(message='This is required')])
    submit = SubmitField('Signup')


class RegistrationForm(Form):
    name = StringField('Name', [Required(message='This is required')])
    password = PasswordField('Password',
                             [Required(message='Must specify a password')])
    submit = SubmitField('Login')
