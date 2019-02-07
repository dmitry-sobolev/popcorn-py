from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from datetime import datetime
from typing import List
from popcorn.items import NewItemsItem
from sqlalchemy import create_engine


class LostfilmNewSpider(CrawlSpider):
    name = 'new_items_spider'
    allowed_dominas = ['www.lostfilm.tv']
    start_urls = ['https://www.lostfilm.tv/new/page_1']
    rules = [Rule(LinkExtractor(
        allow=(r'/new/page_\d{,2}\b',)),
        follow=True, callback='parse_page', process_links='finish_module'), ]
    last_page = None

    def parse_page(self, response):
        my_selector = Selector(response)
        info4search = my_selector.xpath('//div[@class="body"]')
        item = NewItemsItem()

        for info in info4search:
            series_name = info.xpath(
                '//div[@class="name-ru"]/text()').extract()
            episode_info = info.xpath(
                '//div[@class="alpha"]/text()').extract()
        episode_name, episode_date = [], []
        for i in range(len(series_name)):
            episode_name.append(episode_info[i + i])
            preparation_date = episode_info[i + i + 1]
            episode_date.append(preparation_date[-10:])

        engine = create_engine(
            'postgres://postgres@localhost:5432/postgres')
        new_items_table = engine.execute('select * from new_items')
        if new_items_table.rowcount == 0:
            for j in range(len(series_name)):
                item['series_name'] = series_name[0 + j]
                item['episode_name'] = episode_name[0 + j]
                item['episode_date'] = datetime.strptime(
                    (episode_date[0 + j]), '%d.%m.%Y')
                yield item

        else:
            last_episode_date_object = engine.execute(
                'select * from new_items where episode_date = '
                '(select max(episode_date) from new_items)'
                'order by id limit 1')
            for i in last_episode_date_object:
                last_episode_date = i[3]
                for j in range(len(series_name)):
                    if last_episode_date < datetime.strptime(
                            (episode_date[0 + j]), '%d.%m.%Y'):
                        item['series_name'] = series_name[0 + j]
                        item['episode_name'] = episode_name[0 + j]
                        item['episode_date'] = datetime.strptime(
                            (episode_date[0 + j]), '%d.%m.%Y')
                        yield item

        if len(item) == 0:
            self.last_page = int(response.meta['link_text'])

    def finish_module(self, links: List):
        if self.last_page is None:
            return links

        return [l for l in links if
                l.text.isalnum() and int(l.text) < self.last_page]
