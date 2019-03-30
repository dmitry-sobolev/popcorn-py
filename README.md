# popcorn-py
`site with links for TV series torrents`

### venv
```
pipenv install
```

### database
postgres, database named scrapy
```
python manage.py makemigrations
python manage.py migrate
```

### spiders
launch 
```
python manage.py crawl_series
python manage.py crawl_new_tems
```

### django
```
python manage.py createsuperuser
python manage.py runserver
```
