from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os
from app.auth.controllers import auth

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
#
#from models import Employee

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

app.register_blueprint(auth)

@app.route('/')
def hello():
    return "Hello World!"

