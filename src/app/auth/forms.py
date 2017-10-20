from flask_wtf import FlaskForm
from flask_wtf.csrf import _FlaskFormCSRF
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Required, Email, Regexp, StopValidation
from app.csrf import generate_csrf, validate_csrf
from zxcvbn import password_strength
import logging


logger = logging.getLogger(__name__)


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


class OwnCSRF(_FlaskFormCSRF):
    # reimplementing _FlaskFormCSRF to use our own
    # generate_csrf/validate_csrf methods.
    # rather brittle as it's vendored internal code.
    def generate_csrf_token(self, csrf_token_field):
        return generate_csrf(
            secret_key=self.meta.csrf_secret,
            token_key=self.meta.csrf_field_name
        )

    def validate_csrf_token(self, form, field):
        if g.get('csrf_valid', False):
            # already validated by CSRFProtect
            return

        try:
            validate_csrf(
                field.data,
                self.meta.csrf_secret,
                self.meta.csrf_time_limit,
                self.meta.csrf_field_name
            )
        except ValidationError as e:
            logger.info(e.args[0])
            raise


class LoginForm(OwnCSRF, FlaskForm):
    email = StringField('Email Address', [Email(),
                      Required(message='This is required')])
    password = PasswordField('Password',
                             [Required(message='Must specify a password')],
                             render_kw={'autocomplete': 'off'})
    submit = SubmitField('Login')


class SignupForm(OwnCSRF, FlaskForm):
    email = StringField('Email Address', [Email(),
                      Required(message='This is required'),
                      Regexp('.*@(minnow|babel).com$', message='Only company email addresses can be used.')
                      ])
    submit = SubmitField('Signup')


class RegistrationForm(OwnCSRF, FlaskForm):
    token = StringField('Token', [Required(message='This is required')])
    name = StringField('Name', [Required(message='This is required')])
    password = PasswordField('Password',
                             [Required(message='Must specify a password'),
                              StrongPassword()])
    submit = SubmitField('Login')
