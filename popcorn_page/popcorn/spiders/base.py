from scrapy.spiders import CrawlSpider


class BaseMixin(CrawlSpider):
    def before_start(self, session):
        pass
