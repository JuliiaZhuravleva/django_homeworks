from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    articles = Article.objects.all().prefetch_related('scopes__tag')
    context = {'object_list': articles}

    return render(request, template, context)
