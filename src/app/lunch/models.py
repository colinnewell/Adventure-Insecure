from app import db

from app.base_model import Base

class Order(Base):

    __tablename__ = 'lunch_order'

    order = db.Column(db.Text, nullable=False)
    order_for = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, order, order_for):

        self.order = order
        self.order_for = order_for

    def __repr__(self):
        return "<Order %s - %s>" % (self.link_text, self.filename)

