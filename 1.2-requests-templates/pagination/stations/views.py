import csv
from pprint import pprint

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


csv.register_dialect("csv_commas_no_quote", delimiter=',', quoting=csv.QUOTE_MINIMAL, escapechar="\\")

with open(settings.BUS_STATION_CSV, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, dialect='csv_commas_no_quote')
    stations = []
    for row in reader:
        stations.append(row)


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(stations, 10)
    page = paginator.get_page(page_number)
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'index.html', context)
