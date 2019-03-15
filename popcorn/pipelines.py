from scrapy_djangoitem import DjangoItem


class PopcornPipeline(object):
    def __init__(self, uri):
        self.uri = uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(uri=crawler.settings.get('DB_URI'))

    def open_spider(self, spider):
        spider.before_start()

    def process_item(self, item: DjangoItem, spider):
        item.save()
        return item
