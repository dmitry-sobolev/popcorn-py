from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

my_declarative_base = declarative_base()


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
    my_declarative_base.metadata.create_all(engine)


def create_new_items_table(engine):
    my_declarative_base.metadata.create_all(engine)


class Series(my_declarative_base):
    __tablename__ = 'series'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    date = Column('date', Integer)
    genres = Column('genres', String)


class NewItems(my_declarative_base):
    __tablename__ = 'new_items'

    id = Column(Integer, primary_key=True)
    series_name = Column('series_name', String)
    episode_name = Column('episode_name', String)
    episode_date = Column('episode_date', DateTime)
