import scrapy
import json


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
        data_series = {}

        for info in results['data']:
            data_series['title'] = info['title']
            data_series['date'] = info['date']
            data_series['genres'] = info['genres']
            yield data_series
