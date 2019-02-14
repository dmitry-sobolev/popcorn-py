from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from popcorn.items import ModelMixin
from popcorn.models import my_declarative_base


class PopcornPipeline(object):
    def __init__(self, uri):
        self.uri = uri
        self.session: Session = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(uri=crawler.settings.get('DB_URI'))

    def open_spider(self, spider):
        engine = create_engine(self.uri)
        my_declarative_base.metadata.create_all(engine)
        session_cls = sessionmaker(bind=engine)
        self.session = session_cls()
        spider.before_start(self.session)

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item: ModelMixin, spider):
        item.insert(self.session)

        return item
