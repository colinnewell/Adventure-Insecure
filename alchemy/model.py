from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
 
Base = declarative_base()
 
class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
class LunchOrder(Base):
    __tablename__ = 'lunch'

    id = Column(Integer, primary_key=True)
    # FIXME: perhaps select establishment?
    order = Column(Text())
 
