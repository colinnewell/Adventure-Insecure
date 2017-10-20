from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Required, Email, Regexp, StopValidation
from app.csrf import generate_csrf, validate_csrf
from zxcvbn import password_strength


class StrongPassword():

    def __init__(self, min_score=2, message=None):
        self.message = message
        self.min_score = min_score

    def __call__(self, form, field):
        value = field.data
        if value:
            # FIXME: it would be good if
            # we could pick up the users
            # data to make use of the password_strength
            # functions feature to penalize repeating
            # personal data in the password field.
            info = password_strength(field.data)
            if info['score'] < self.min_score:
                if self.message is None:
                    message = field.gettext('Password must be stronger.  We estimate this password can be cracked in %s' % info['crack_time_display'])
                else:
                    message = self.message

                field.errors[:] = []
                raise StopValidation(message)


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
                             [Required(message='Must specify a password')],
                             render_kw={'autocomplete': 'off'})
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
                             [Required(message='Must specify a password'),
                              StrongPassword()])
    submit = SubmitField('Login')
