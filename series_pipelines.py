from sqlalchemy.orm import sessionmaker
from series_models import db_connect, create_series_table, Series


class SeriesPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_series_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item):
        session = self.Session()
        new_items = Series(**item)

        try:
            session.add(new_items)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
