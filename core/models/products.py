from locale import currency
from tkinter import CASCADE
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, ForeignKey, null
from sqlalchemy.orm import relationship

from db._db import Base

class Currencies(Base):
    __tablename__="currencies"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    currency_name = Column(String(250), nullable=True)
    currency_sign = Column(String(50), nullable=True)
    parent = relationship("Products")


class Products(Base):
    __tablename__="products"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(250), nullable=True)
    price = Column(Integer, nullable=True)
    currency = Column(Integer, ForeignKey("currencies.id", ondelete=CASCADE))