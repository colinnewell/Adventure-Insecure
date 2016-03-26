from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
Bootstrap(app)

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# note, this import needs to come after the definition of db.
from app.auth.controllers import auth
app.register_blueprint(auth)


@app.route('/')
def hello():
    return "Hello World!"

db.create_all()
