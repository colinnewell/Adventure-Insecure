from app import db
from app.base_model import Base


class OfficeNumber(Base):

    __tablename__ = 'office_numbers'

    name = db.Column(db.String(128), nullable=False, unique=True)
    number_prefix = db.Column(db.String(128), nullable=False)
    main_number = db.Column(db.String(128), nullable=False)
