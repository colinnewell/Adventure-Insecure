from app import db

from app.base_model import Base

class Menu(Base):

    __tablename__ = 'menus'

    filename = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(256), nullable=False)
    link_text = db.Column(db.String(256), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, filename, link_text):

        self.filename = filename
        self.link_text = link_text

    def __repr__(self):
        return "<Menu %s - %s>" % (self.link_text, self.filename)
