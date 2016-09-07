from flask import Blueprint, request, render_template, \
    session, redirect, url_for
from app.auth.utils import login_required
from app.lunch.models import Order, OrderLine
from app.lunch.forms import OrderForm, OrderLineForm
from app import db


lunch = Blueprint('lunch', __name__, url_prefix='/lunch')


@lunch.route('/', methods=['GET'])
@login_required
def index():
    # FIXME: should order them
    # func.date_trunc('day', Order.date_created)=func.date_trunc('day', func.now())
    # FIXME: can I do something for SQLite too?
    #orders = Order.query.filter(text("date_trunc('day', date_created)=date_trunc('day', now())")).all()
    orders = Order.query.all()
    return render_template('lunch/index.html', orders=orders)

@lunch.route('/add_order', methods=['GET', 'POST'])
@login_required
def add_order():
    form = OrderForm(request.form)
    if form.validate_on_submit():
        title = form.title.data
        o = Order(title)
        db.session.add(o)
        db.session.commit()
        return redirect(url_for('lunch.index'))
    return render_template('lunch/add_order.html', form=form)

@lunch.route('/order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def order(order_id):
    order = Order.query.filter_by(id=order_id).one()
    form = OrderLineForm(request.form)
    if form.validate_on_submit():
        r = form.request.data
        l = OrderLine(order_id, r, session['user_id'])
        db.session.add(l)
        db.session.commit()
        return redirect(request.url)
    return render_template('lunch/order.html', form=form, order=order)
