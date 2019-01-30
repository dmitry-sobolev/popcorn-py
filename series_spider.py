import scrapy
import json
from pipelines import SeriesPipeline
from models import db_connect


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

        all_tables = db_connect().execute(
            'select table_name from information_schema.tables')
        if ('series',) not in all_tables:

        # object_max_id = db_connect().execute(
        #     'select id from series where id = '
        #     '(select max(id) from series)')
        # for i in object_max_id:
        #     db_max_id = i[0]
            series_pipe_line = SeriesPipeline()
            for info in results['data']:
                # if db_max_id < int(info['id']):
                data_series['id'] = info['id']
                data_series['title'] = info['title']
                data_series['date'] = info['date']
                data_series['genres'] = info['genres']
                yield series_pipe_line.process_item(data_series)
