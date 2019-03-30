from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^series/$', views.SeriesView.as_view(), name='series'),
    url(r'^series/(?P<pk>\d+)$', views.SeriesDetailView.as_view(),
        name='series-details'),
]
