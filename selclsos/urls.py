# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
import student.views
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'selclsos.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', student.views.index, name='index'),
    url(r'^index/$', student.views.index, name='index'),
    url(r'^master/', include('master.urls', namespace='master', app_name='master')),
    url(r'^student/', include('student.urls', namespace='student', app_name='student')),
    url(r'^news/', include('news.urls', namespace='news', app_name='news')),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
)