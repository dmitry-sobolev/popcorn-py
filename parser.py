import bs4
import requests

# вставить адрес с сайта лостфильм.тв, раздел гид по сериям
httpAddress = 'https://www.lostfilm.tv/series/Rome/seasons'

# название сериала из адреса
seriesName = ((str(httpAddress)).split('/')[-2])
if '_' in seriesName:
    newName = seriesName.split('_')
    print(*newName)
else:
    print(seriesName)
print()

# делаю суп с необходимыми данными из страницы
httpFile = requests.get(httpAddress)
soup = bs4.BeautifulSoup(httpFile.text, 'html.parser')
dataSoup = soup.findAll(attrs={"class": "details"})

# количество сезонов
amountSeason = len(dataSoup)

# год выхода сезона и количество эпизодов из супа
i = 0
for data in dataSoup:
    strData = str(data)
    yearSeason = strData[strData.find('Год:'): strData.find('Год:') + 9]
    episodeAmount = strData[strData.find('Количество вышедших серий:'):
                            strData.find('Количество вышедших серий:') + 29]
    print('Сезон:', amountSeason - i)
    print(yearSeason)
    print(episodeAmount, end='\n\n')
    i += 1
