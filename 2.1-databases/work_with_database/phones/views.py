import os

from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect

from phones.models import Phone


sort_by = {'name': 'name', 'min_price': 'price', 'max_price': '-price'}


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort', None)
    if sort:
        phones_objects = Phone.objects.order_by(sort_by[sort])
    else:
        phones_objects = Phone.objects.all()
    phones = []
    for p in phones_objects:
        phones.append({
            'name': p.name,
            'price': p.price,
            'image': p.image.url,
            'release_date': p.release_date,
            'lte_exists': p.lte_exists,
            'slug': p.slug
        })
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)[0]
    context = {
        'phone':
            {
                'name': phone.name,
                'price': phone.price,
                'image': phone.image.url,
                'release_date': phone.release_date,
                'lte_exists': phone.lte_exists,
                'slug': phone.slug}
        }
    return render(request, template, context)
