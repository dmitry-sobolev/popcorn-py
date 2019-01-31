import abc

import scrapy
from sqlalchemy.dialects.postgresql import insert

from popcorn.models import NewItems, Series


class ModelMixin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def model(self):
        pass

    def insert(self, session):
        session.add(self.model())


class NewItemsItem(ModelMixin, scrapy.Item):
    series_name = scrapy.Field()
    episode_name = scrapy.Field()
    episode_date = scrapy.Field()

    def model(self):
        return NewItems(**self)


class SeriesItem(ModelMixin, scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    genres = scrapy.Field()

    def model(self):
        return Series(**self)

    def insert(self, session):
        model = self.model()
        table = model.metadata.tables[model.__tablename__]
        insert_stmt = insert(table).values(**self)
        insert_stmt = insert_stmt.on_conflict_do_update(index_elements=[table.c.id],
                                                        set_={'title': insert_stmt.excluded.title,
                                                              'date': insert_stmt.excluded.date,
                                                              'genres': insert_stmt.excluded.genres})
        session.execute(insert_stmt)
