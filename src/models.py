from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    zip_code = Column(String)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
