from sqlalchemy.orm import sessionmaker
from models import db_connect, create_series_table, Series, \
    create_new_items_table, NewItems


class BasePipeline(object):
    create_table_func = None
    model_class = None

    def __init__(self):
        engine = db_connect()
        self.create_table_func()
        self.session = sessionmaker(bind=engine)

    def process_item(self, item):
        session = self.session()
        new_items = self.model_class(**item)

        try:
            session.add(new_items)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class NewItemsPipeline(BasePipeline):
    create_table_func = create_new_items_table
    model_class = NewItems


class SeriesPipeline(BasePipeline):
    create_table_func = create_series_table
    model_class = Series
