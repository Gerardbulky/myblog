from django.shortcuts import render, get_object_or_404
from .models import News


def news_list(request):
    news = News.published.all()
    return render(request,
                 'letter/news/list.html',
                 {'news': news})


def news_detail(request, year, month, day, news):
    news = get_object_or_404(News, slug=news,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request,
                  'letter/news/details.html',
                  {'news': news})
