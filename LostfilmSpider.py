import scrapy
from LostfilmItems import LostfilmItems


class LostfilmSpider(scrapy.Spider):
    name = 'lstflm_spider'
    allowed_dominas = ['www.lostfilm.tv']
    start_urls = ['https://www.lostfilm.tv/series/The_Expanse/seasons']

    def parse(self, response):
        my_selector = scrapy.Selector(response)
        all_data = my_selector.xpath('//*[@id="left-pane"]')
        for info in all_data:
            item = LostfilmItems()
            item['series_name'] = info.xpath('/html/head/title/text('
                                             ')').extract()
            item['all_info'] = info.xpath('//*[@id="left-pane"]/div['
                                          '6]').extract()
        yield item
