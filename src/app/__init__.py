from flask_bootstrap import Bootstrap
from flask import Flask, render_template, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
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
from app.menus.controller import menus
app.register_blueprint(menus)
from app.lunch.controller import lunch
app.register_blueprint(lunch)


@app.route('/')
def index():
    return render_template('index.html')

# FIXME: should move this out of the core app code.
from app.auth.models import User
from flask import session
def _get_user():
    if 'user_id' in session:
        try:
            u = User.query.filter_by(id=session['user_id']).one()
            return u
        except:
            pass
    return None

@app.context_processor
def inject_user():
    return dict(user=_get_user())
    
