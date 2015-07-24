from django.shortcuts import render
from models import News, Category
from django.http import HttpResponse


def news_category(request, id):
    id = int(id)
    category_news = News.objects.filter(category_id=id)
    context = {'category_news': category_news}
    return render(request, 'news/category.html', context)

def detail(request, id):
    id = int(id)
    news = News.objects.get(id=id)
    context = {'news': news}
    return render(request, 'news/detail.html', context)
