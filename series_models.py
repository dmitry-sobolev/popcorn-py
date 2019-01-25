from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

declarative_base = declarative_base()


def db_connect():
    return create_engine(URL(**{
        'drivername': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': '',
        'password': '',
        'database': 'scrapy'
    }))


def create_series_table(engine):
    declarative_base.metadata.create_all(engine)


class Series(declarative_base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    date = Column('date', Integer)
    genres = Column('genres', String)
