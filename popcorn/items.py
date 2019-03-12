from scrapy_app.models import NewItems, Series
from scrapy_djangoitem import DjangoItem


class NewItemsItem(DjangoItem):
    django_model = NewItems

    def model(self):
        return NewItems(**self)

    # def save(self, commit=False):
    #     return super().save(commit)


class SeriesItem(DjangoItem):
    django_model = Series

    def model(self):
        return Series(**self)

    # def save_or_update(self, pipeline):
    #     if True:
    #         pipeline.for_save(self.save(commit=False))
    #     else:
    #         pipeline.for_update(self.save(commit=False))
