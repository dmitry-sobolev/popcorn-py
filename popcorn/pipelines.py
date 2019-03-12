from scrapy_djangoitem import DjangoItem


class PopcornPipeline(object):
    def __init__(self, uri):
        self.uri = uri
        # self.for_save = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(uri=crawler.settings.get('DB_URI'))

    def open_spider(self, spider):
        spider.before_start()

    # def close_spider(self, spider):
    #     cls = self.for_save[0].__class__
    #     cls.django_model.objects.bulk_create(self.for_save)

    def process_item(self, item: DjangoItem, spider):
        item.save()
        return item
