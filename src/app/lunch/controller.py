from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort
from werkzeug import secure_filename
from app.auth.utils import login_required
from app.lunch.models import Order
import os

lunch = Blueprint('lunch', __name__, url_prefix='/lunch')


