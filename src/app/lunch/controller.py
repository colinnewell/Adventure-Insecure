from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for, abort
from werkzeug import secure_filename
from app.auth.utils import login_required
from sqlalchemy.sql import func, text
from app.lunch.models import Order, OrderLine
import os

lunch = Blueprint('lunch', __name__, url_prefix='/lunch')


@lunch.route('/', methods=['GET'])
@login_required
def index():
    # FIXME: should order them
    # func.date_trunc('day', Order.date_created)=func.date_trunc('day', func.now())
    orders = Order.query.filter(text("date_trunc('day', date_created)=date_trunc('day', now())")).all()
    return render_template('lunch/index.html', orders=orders)

@lunch.route('/add_order', methods=['GET', 'POST'])
@login_required
def add_order():
    return render_template('lunch/add_order.html')
