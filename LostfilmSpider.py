# регистрация для сайта (пока не требуется)
# log - WatneyMark
# pass - GiovanniVirginioSchiaparelli

import re
import scrapy
from LostfilmItems import LostfilmItems


class LostfilmSpider(scrapy.Spider):
    name = 'lstflm_spider'
    allowed_dominas = ['www.lostfilm.tv']
    start_urls = ['http://www.lostfilm.tv/series/The_Walking_Dead/seasons']

    def parse(self, response):
        my_selector = scrapy.Selector(response)
        all_data = my_selector.xpath('/html/body/div[2]/div[2]/div[1]/div[6]')
        for info in all_data:
            item = LostfilmItems()

            # имя сериала из title-ru
            series_name = info.xpath(
                '/html/body/div[2]/div[2]/div[1]/div[1]/h1/div[1]/text()'
            ).extract()

            # все divы с классом details
            info4search = info.xpath('//div[@class="details"]/text()')

            # годы выхода всех сезонов
            season_year = re.findall(r'Год: \d{4}', str(info4search))

            # количество серий во всех сезонах
            episodes = re.findall(r'Количество вышедших серий: \d+',
                                  str(info4search))

            # инфа по каждому сезону в сборе
            seasons_info = []
            for i in range(len(season_year)):
                seasons_info.append(
                    f'Сезон: {len(season_year) - i}. {season_year[0 + i]}.'
                    f' {episodes[0 + i]}.')

            item['series_name'] = series_name
            item['seasons_info'] = seasons_info

            yield item
