"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from datetime import datetime

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

from books.views import books_view, books_list_by_date_view

from django.urls import register_converter


class DateConverter:
    regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    format = '%Y-%m-%d'

    def to_python(self, value: str) -> datetime:
        return datetime.strptime(value, self.format)

    def to_url(self, value: datetime) -> str:
        return value.strftime(self.format)


register_converter(DateConverter, 'date')

urlpatterns = [
    path('', lambda request: redirect('/books/')),
    path('books/', books_view, name='books'),
    path('books/<date:date>/', books_list_by_date_view, name=''),
    path('admin/', admin.site.urls),
]
