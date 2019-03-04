import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from datetime import datetime
from typing import List
from http.cookies import SimpleCookie
import json

from popcorn.items import NewItemsItem
from .base import BaseMixin


class LogInError(Exception):
    def __init__(self, text):
        LogInError.txt = text


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
        if not isinstance(site_ans, dict):
            raise LogInError("Login failed! Unknown error.")

        is_success = site_ans.get('success', False)
        if not is_success:
            raise LogInError("Login failed! Need captcha.")

        if site_ans['success'] is True:
            raw_data = str(response.headers['Set-Cookie'], encoding='ascii')
            cookie = SimpleCookie()
            cookie.load(raw_data)
            self.cookies = cookie
            return response.follow('https://www.lostfilm.tv/new/page_0',
                                   callback=self.parse,
                                   cookies=self.cookies)

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

            page_request = scrapy.Request(page_link, cookies=cookies_for_page,
                                          callback=self.parse_download_link)
            page_request.meta['item'] = item

            yield page_request

        if item is None:
            self.last_page = int(response.meta['link_text'])

    def parse_download_link(self, response):
        response.meta['item']['download_link'] = response.url
        yield response.meta['item']

    def finish_module(self, links: List):
        if self.last_page is None:
            return links

        return [l for l in links if
                l.text.isalnum() and int(l.text) < self.last_page]

    def _build_request(self, rule, link):
        r = super(LostfilmNewSpider, self)._build_request(rule, link)
        r.cookies = self.cookies
        return r
