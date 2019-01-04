import scrapy


class LostfilmItems(scrapy.Item):
    series_name = scrapy.Field()
    seasons_info = scrapy.Field()
