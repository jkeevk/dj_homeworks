import csv
from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

def get_stations(file_name):
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def index(request):
    return redirect(reverse('bus_stations'))

def bus_stations(request):
    CONTENT = get_stations('data-398-2018-08-30.csv')
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(CONTENT, 10)
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'bus_stations': page.object_list,
    }
    return render(request, 'stations/index.html', context)

