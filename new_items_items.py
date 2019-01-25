import scrapy


class NewItemsItems(scrapy.Item):
    series_name = scrapy.Field()
    episode_name = scrapy.Field()
    episode_date = scrapy.Field()
