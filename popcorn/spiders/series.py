import scrapy
import json

from popcorn.items import SeriesItem


class LostfilmSeriesSpider(scrapy.Spider):
    name = 'series_spider'
    allowed_dominas = ['www.lostfilm.tv']
    start_urls = [
        'https://www.lostfilm.tv/ajaxik.php?act=serial&type=search&o=0']

    def parse(self, response):
        stop_num = 0
        while stop_num <= 330:
            next_urls = (
             'https://www.lostfilm.tv/ajaxik.php?act=serial&type=search&o={}'
            ).format(stop_num)
            stop_num += 10
            yield response.follow(next_urls, callback=self.parse_data)

    def parse_data(self, response):
        results = json.loads(response.body)

        for info in results['data']:
            yield SeriesItem(
                id=info['id'],
                title=info['title'],
                date=info['date'],
                genres=info['genres']
            )
