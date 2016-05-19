from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy
from app.csrf import generate_csrf, validate_csrf
import flask_wtf.csrf
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
Bootstrap(app)
Session(app)
flask_wtf.csrf.validate_csrf = validate_csrf
flask_wtf.csrf.generate_csrf = generate_csrf
flask_wtf.csrf.CsrfProtect(app)

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# note, this import needs to come after the definition of db.
from app.auth.controllers import auth
app.register_blueprint(auth)


@app.route('/')
def index():
    return render_template('index.html')
