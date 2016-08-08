from app import db

from app.base_model import Base
from sqlalchemy.orm import relationship


class Order(Base):

    __tablename__ = 'order'

    title = db.Column(db.Text, nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Order %s - %s>" % (self.title)

class OrderLine(Base):

    __tablename__ = 'lunch_order'

    order = db.Column(db.Text, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', name="order_id_fkey"))
    order_for = db.Column(db.Integer, db.ForeignKey('users.id'))

    header = relationship("Order", foreign_keys=[order_id])

    def __init__(self, order_id, order, order_for):

        self.order = order
        self.order_for = order_for
        self.order_id = order_id

    def __repr__(self):
        return "<OrderLine %s - %s>" % (self.order)

