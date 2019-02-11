from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from datetime import datetime
from typing import List

from popcorn.items import NewItemsItem
from .base import BaseMixin


class LostfilmNewSpider(BaseMixin, CrawlSpider):
    name = 'new_items_spider'
    allowed_dominas = ['www.lostfilm.tv']
    start_urls = ['https://www.lostfilm.tv/new/page_1']
    rules = [Rule(LinkExtractor(
        allow=(r'/new/page_\d{,2}\b',)),
        follow=True, callback='parse_page', process_links='finish_module'), ]
    last_page = None
    last_episode_date = None

    def before_start(self, session):
        self.last_episode_date, = session.execute(
            'select max(episode_date) from new_items').first()

    def parse_page(self, response):
        my_selector = Selector(response)
        info4search = my_selector.css('.row')
        item = None

        for info in info4search:
            series_name = info.css('.name-ru').xpath('./text()').extract()
            episode_name, episode_date_words = info.css('.alpha').xpath('./text()').extract()
            episode_date_words = episode_date_words[-10:]
            episode_date = datetime.strptime(episode_date_words, '%d.%m.%Y')

            if self.last_episode_date is not None and self.last_episode_date >= episode_date:
                break
            item = NewItemsItem()
            item['series_name'] = series_name
            item['episode_name'] = episode_name
            item['episode_date'] = episode_date
            yield item

        if item is None:
            self.last_page = int(response.meta['link_text'])

    def finish_module(self, links: List):
        if self.last_page is None:
            return links

        return [l for l in links if
                l.text.isalnum() and int(l.text) < self.last_page]
