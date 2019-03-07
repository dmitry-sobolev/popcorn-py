from django.db import models
from sqlalchemy.ext.declarative import declarative_base

my_declarative_base = declarative_base()


class Series(models.Model):

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    date = models.IntegerField()
    genres = models.CharField(max_length=200)


class NewItems(models.Model):

    series_name = models.CharField(max_length=200)
    episode_name = models.CharField(max_length=200)
    episode_date = models.DateTimeField()
    download_link = models.CharField(max_length=200)
