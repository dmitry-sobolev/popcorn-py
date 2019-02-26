import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from datetime import datetime
from typing import List
from http.cookies import SimpleCookie
import json
import requests

from popcorn.items import NewItemsItem
from .base import BaseMixin


class LostfilmNewSpider(BaseMixin, CrawlSpider):
    name = 'new_items_spider'
    allowed_dominas = ['www.lostfilm.tv']
    rules = [Rule(LinkExtractor(
        allow=(r'/new/page_\d{,2}\b',)),
        follow=True, callback='parse_page', process_links='finish_module'), ]
    last_page = None
    last_episode_date = None
    cookies = None

    def start_requests(self):
        return [scrapy.FormRequest('http://www.lostfilm.tv/ajaxik.php',
                                   formdata=self.settings.get('LOG_IN'),
                                   callback=self.logged_in)]

    def logged_in(self, response):
        site_ans = json.loads(response.text)
        try:
            if site_ans['success'] is True:
                raw_data = str(response.headers['Set-Cookie'], encoding='ascii')
                cookie = SimpleCookie()
                cookie.load(raw_data)
                self.cookies = cookie
                return response.follow('https://www.lostfilm.tv/new/page_0',
                                       callback=self.parse,
                                       cookies=self.cookies)
        except KeyError:
            print('Login failed! Need captcha or unknown error.')

    def before_start(self, session):
        self.last_episode_date, = session.execute(
            'select max(episode_date) from new_items').first()

    def parse_page(self, response):
        my_selector = Selector(response)
        info4search = my_selector.css('.row')
        item = None

        for info in info4search:

            series_code = info.css('.haveseen-btn').attrib['data-episode']
            page_link = 'http://lostfilm.tv/v_search.php?a=' + series_code
            cookies_for_page = {}
            for key, morsel in self.cookies.items():
                cookies_for_page[key] = morsel.value
            page_with_download_link = requests.post(page_link, cookies=cookies_for_page)
            page_text = page_with_download_link.text
            download_link = page_text[page_text.find('<a href="'):page_text.rfind('">эту ссылку</a>')][9:]

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
            item['download_link'] = download_link
            yield item

        if item is None:
            self.last_page = int(response.meta['link_text'])

    def finish_module(self, links: List):
        if self.last_page is None:
            return links

        return [l for l in links if
                l.text.isalnum() and int(l.text) < self.last_page]

    def _build_request(self, rule, link):
        r = super(LostfilmNewSpider, self)._build_request(rule, link)
        r.cookies = self.cookies
        return r
