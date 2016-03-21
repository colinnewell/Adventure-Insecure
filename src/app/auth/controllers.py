from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from werkzeug import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return "Login"
