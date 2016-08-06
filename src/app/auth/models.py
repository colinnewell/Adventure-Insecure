from app import db
from app.security import secure_token
from app.base_model import Base
from sqlalchemy.sql import text


class SignupAttempt(Base):

    __tablename__ = 'signup_attempts'

    email = db.Column(db.String(128), nullable=False, unique=True)
    registration_code = db.Column(db.String(128), nullable=False)

    def __init__(self, email, registration_code):

        self.email = email
        self.registration_code = registration_code

    def __repr__(self):
        return "<Signup attempt from %s: %r, %r>" % (self.date_created, self.email, self.registration_code)

    @classmethod
    def AttemptFor(cls, email):
        return cls(email, secure_token())


class User(Base):

    __tablename__ = 'users'

    name = db.Column(db.String(128), nullable=False)

    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, server_default=text('false'))

    # FIXME: should allow deactivation of users.

    def __init__(self, name, email, password, admin=False):

        self.name = name
        self.email = email
        self.password = password
        self.admin = admin

    def __repr__(self):
        return "<User %r, %r>" % (self.name, self.email)
