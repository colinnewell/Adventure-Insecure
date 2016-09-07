from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Required, Email, Regexp
from app.csrf import generate_csrf, validate_csrf


class OwnCSRF():
    # actually uses env/lib/python3.5/site-packages/flask_wtf/form.py
    def generate_csrf_token(self, csrf_context):
        if not self.csrf_enabled:
            return None
        return generate_csrf(self.SECRET_KEY, self.TIME_LIMIT)

    def validate_csrf_token(self, field):
        if not self.csrf_enabled:
            return True
        if not validate_csrf(field.data, self.SECRET_KEY, self.TIME_LIMIT):
            raise ValidationError(field.gettext('CSRF token missing'))


class LoginForm(OwnCSRF, Form):
    email = StringField('Email Address', [Email(),
                      Required(message='This is required')])
    password = PasswordField('Password',
                             [Required(message='Must specify a password')])
    submit = SubmitField('Login')


class SignupForm(OwnCSRF, Form):
    email = StringField('Email Address', [Email(),
                      Required(message='This is required'),
                      Regexp('.*@(minnow|babel).com$', message='Only company email addresses can be used.')
                      ])
    submit = SubmitField('Signup')


class RegistrationForm(OwnCSRF, Form):
    token = StringField('Token', [Required(message='This is required')])
    name = StringField('Name', [Required(message='This is required')])
    password = PasswordField('Password',
                             [Required(message='Must specify a password')])
    submit = SubmitField('Login')
