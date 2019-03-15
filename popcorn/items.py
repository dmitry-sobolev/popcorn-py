from scrapy_app.models import NewItems, Series
from scrapy_djangoitem import DjangoItem


class NewItemsItem(DjangoItem):
    django_model = NewItems

    def model(self):
        return NewItems(**self)


class SeriesItem(DjangoItem):
    django_model = Series

    def model(self):
        return Series(**self)
