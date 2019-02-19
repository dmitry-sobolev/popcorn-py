from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

my_declarative_base = declarative_base()


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
    download_link = Column('download_link', String)
