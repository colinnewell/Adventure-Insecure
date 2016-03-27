from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Email, EqualTo


class LoginForm(Form):
    email = StringField('Email Address', [Email(),
                      Required(message='This is required')])
    password = PasswordField('Password',
                             [Required(message='Must specify a password')])
    submit = SubmitField('Login')


class SignupForm(Form):
    email = StringField('Email Address', [Email(),
                      Required(message='This is required')])
    submit = SubmitField('Signup')


class RegistrationForm(Form):
    name = StringField('Name', [Required(message='This is required')])
    password = PasswordField('Password',
                             [Required(message='Must specify a password')])
    submit = SubmitField('Login')
