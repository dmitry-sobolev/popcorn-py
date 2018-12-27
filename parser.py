import bs4
import requests
from urllib.parse import urlparse

# вставить адрес с сайта лостфильм.тв, раздел гид по сериям
http_address = 'https://www.lostfilm.tv/series/Futurama/seasons'

# название сериала из адреса
url_data = urlparse(http_address)
series_name = (url_data.path.split('/')[-2])
series_name = series_name.replace('_', ' ')

# делаю суп с необходимыми данными из страницы
http_file = requests.get(http_address)
soup = bs4.BeautifulSoup(http_file.text, 'html.parser')
data_soup = soup.findAll(attrs={"class": "details"})

# количество сезонов
amount_season = len(data_soup)

# год выхода сезона и количество эпизодов из супа
seasons_data = []
for i, data in enumerate(data_soup):
    str_data = str(data)
    year_season = str_data[str_data.find('Год:'): str_data.find('Год:') + 9]
    episode_amount = str_data[str_data.find('Количество вышедших серий:'):
                              str_data.find('Количество вышедших серий:') + 29]
    seasons_data.append(
        f'Сезон: {amount_season - i}\n{year_season}\n{episode_amount}\n\n')
print(f'{series_name}\n\n{"".join(seasons_data)}')
