from django.db import models
from django.urls import reverse


class Series(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    date = models.IntegerField()
    genres = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('series-details', args=[str(self.id)])

    class Meta:
        ordering = ['title']


class NewItems(models.Model):
    series_name = models.CharField(max_length=200)
    episode_name = models.CharField(max_length=200)
    episode_date = models.DateTimeField()
    download_link = models.CharField(max_length=200)
    series = models.ForeignKey('Series', on_delete=models.DO_NOTHING,
                               null=True)

    def __str__(self):
        return self.series_name
