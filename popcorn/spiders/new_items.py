from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from datetime import datetime, timedelta
from typing import List
from popcorn.items import NewItemsItem


class LostfilmNewSpider(CrawlSpider):
    name = 'new_items_spider'
    allowed_dominas = ['www.lostfilm.tv']
    start_urls = ['https://www.lostfilm.tv/new/page_1']
    last_page = None

    # правила перехода по страницам
    rules = [Rule(LinkExtractor(
        allow=(r'/new/page_\d{,2}\b',)),
        follow=True, callback='parse_page', process_links='finish_module'), ]

    def parse_page(self, response):
        my_selector = Selector(response)
        info4search = my_selector.xpath('//div[@class="body"]')
        item = NewItemsItem()

        for info in info4search:
            # названия сериалов в одном списке
            series_name = info.xpath(
                '//div[@class="name-ru"]/text()').extract()
            # название эпизода и дата выхода эпизода в одном списке
            episode_info = info.xpath(
                '//div[@class="alpha"]/text()').extract()

        # название эпизода и дата выхода в отдельных списках
        episode_name, episode_date = [], []
        for i in range(len(series_name)):
            episode_name.append(episode_info[i + i])
            preparation_date = episode_info[i + i + 1]
            episode_date.append(preparation_date[-10:])

        stop_time = datetime.now() - timedelta(7)
        for j in range(len(series_name)):
            date = episode_date[j]
            if datetime.strptime(date, '%d.%m.%Y') > stop_time:
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
