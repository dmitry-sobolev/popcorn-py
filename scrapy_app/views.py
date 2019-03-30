from django.shortcuts import render
from django.views import generic

from .models import Series, NewItems


def index(request):
    num_series = Series.objects.all().count()
    num_newitems = NewItems.objects.all().count()
    return render(request, 'index.html',
                  context={'num_series': num_series, 'num_newitems': num_newitems}, )


class SeriesView(generic.ListView):
    model = Series
    paginate_by = 30


class SeriesDetailView(generic.DetailView):
    model = Series
