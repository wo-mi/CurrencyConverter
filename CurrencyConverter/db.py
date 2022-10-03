import os
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


if not os.path.exists("cache"):
    os.makedirs("cache")

engine = create_engine("sqlite:///cache/cache.db")

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()


class Request(Base):
    __tablename__ = "request"
    id = Column(Integer, primary_key=True)
    code = Column(String)
    date = Column(Date)
    json = Column(String)

    def __init__(self, code=None, date=None, json=None):
        self.code = code
        self.date = date
        self.json = json


Base.metadata.create_all(bind=engine)
