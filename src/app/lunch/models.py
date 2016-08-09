from app import db

from app.base_model import Base
from sqlalchemy.orm import relationship


class Order(Base):

    __tablename__ = 'order_header'

    title = db.Column(db.Text, nullable=False)
    lines = relationship("OrderLine", back_populates="order")

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Order %s - %s>" % (self.title)


class OrderLine(Base):

    __tablename__ = 'order_line'

    request = db.Column(db.Text, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order_header.id', name="order_id_fkey"))
    order_for = db.Column(db.Integer, db.ForeignKey('users.id'))

    order = relationship("Order", foreign_keys=[order_id], back_populates="lines")
    user = relationship("User")

    def __init__(self, order_id, request, order_for):

        self.request = request
        self.order_for = order_for
        self.order_id = order_id

    def __repr__(self):
        return "<OrderLine %s - %s>" % (self.order)

