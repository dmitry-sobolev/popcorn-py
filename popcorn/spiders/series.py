import scrapy
import json

from popcorn.items import SeriesItem


class LostfilmSeriesSpider(scrapy.Spider):
    name = 'series_spider'
    allowed_dominas = ['www.lostfilm.tv']
    start_urls = [
        'https://www.lostfilm.tv/ajaxik.php?act=serial&type=search&o=0']
    counter = 0
    stop_signal = False

    def parse(self, response):
        while self.stop_signal is False:
            next_urls = (
             'https://www.lostfilm.tv/ajaxik.php?act=serial&type=search&o={}'
            ).format(self.counter)
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

        if len(results['data']) == 0:
            self.stop_signal = True
        else:
            self.counter += 10
