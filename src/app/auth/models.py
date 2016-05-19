from app import db
from app.security import secure_token


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


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

    def __init__(self, name, email, password):

        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r, %r>" % (self.name, self.email)
