from django.contrib import admin

from .models import Series, NewItems


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'genres')


@admin.register(NewItems)
class NewItemsAdmin(admin.ModelAdmin):
    list_display = ('series_name', 'episode_name', 'episode_date')
