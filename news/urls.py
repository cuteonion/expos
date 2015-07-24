# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^detail/(?P<id>\d+)/$' , views.detail, name='detail'),
    url(r'^category/(?P<id>\d+)/$', views.news_category, name='news_category'),
    )
