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


def create_new_items_table(engine):
    declarative_base.metadata.create_all(engine)


class Series(declarative_base):
    __tablename__ = 'new_items'

    id = Column(Integer, primary_key=True)
    series_name = Column('series_name', String)
    episode_name = Column('episode_name', String)
    episode_date = Column('episode_date', String)
