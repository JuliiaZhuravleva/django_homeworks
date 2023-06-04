from datetime import datetime

from django.shortcuts import render

from books.models import Book


def __book_objects_to_dict__(book_objects):
    books = []
    for book in book_objects:
        books.append({
            'name': book.name,
            'author': book.author,
            'pub_date': book.pub_date.strftime("%Y-%m-%d")
        })
    return books


def __get_nearest_dates__(current_date):
    nearest_dates = {'prev_date': None, 'next_date': None}
    dates_objects = list(Book.objects.order_by('pub_date').values_list('pub_date', flat=True).distinct())
    unique_dates = []
    for date in dates_objects:
        unique_dates.append(date)
    current_date_index = unique_dates.index(current_date)
    if current_date_index != 0:
        nearest_dates['prev_date'] = dates_objects[current_date_index - 1].strftime("%Y-%m-%d")
    if current_date_index != len(dates_objects) - 1:
        nearest_dates['next_date'] = dates_objects[current_date_index + 1].strftime("%Y-%m-%d")
    return nearest_dates


def books_view(request):
    template = 'books/books_list.html'
    book_objects = Book.objects.all()
    books = __book_objects_to_dict__(book_objects)
    context = {'books': books}
    return render(request, template, context)


def books_list_by_date_view(request, date: datetime):
    template = 'books/books_list_by_date.html'
    book_objects = Book.objects.filter(pub_date=date)
    books = __book_objects_to_dict__(book_objects)
    nearest_dates = __get_nearest_dates__(date.date())
    print(nearest_dates)
    context = {'books': books, 'nearest_dates': nearest_dates}
    return render(request, template, context)
