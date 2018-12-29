import scrapy


class LostfilmItems(scrapy.Item):
    series_name = scrapy.Field()
    all_info = scrapy.Field()
