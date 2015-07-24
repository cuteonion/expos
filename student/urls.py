# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'index2/$', views.index2, name='index2'),
    url(r'^login/$', views.stulogin, name='login'),
    url(r'^stulogout/$', views.stulogout, name='stulogout'),
    url(r'^changepass/$', views.changepass, name='changepass'),
    url(r'^$', views.work, name='work'),
    url(r'work/$', views.work, name='work'),
    url(r'myinfo/$', views.Myinfo.as_view(), name='myinfo'),
    url(r'stuviewclass/$', views.StuViewMyClasses.as_view(), name='stuviewclass'),
    url(r'stuclassreportupload/(?P<classid>\d+)/$', views.StuClassReportUpload.as_view(), name='stuclassreportupload'),
    url(r'stuclassedit/(?P<action>\w+)/(?P<class_id>\d+)/$', views.StuEditClass.as_view(), name='stuclassedit'),
    url(r'stuclassdetail/([\d-]+)/$', views.StuClassDetailView.as_view(), name='stuclassdetail'),
    url(r'editexproom/$', views.EditExpRoom.as_view(), name='edit_exproom'),
    url(r'startexp/$', views.startexp, name='startexp'),
    url(r'doexp/(?P<classroomid>\d+)/$', views.DoExp.as_view(), name='doexp'),
    url(r'ExpHistory/$', views.ExpHistoryView.as_view(), name='exphistory'),
    url(r'viewnews/$', views.NewsView.as_view(), name='viewnews'),
    url(r'newsdetail/(?P<newsid>\d+)/$', views.newsdetail, name='newsdetail'),
    url(r'deleteclassreport/(?P<classid>\d+)/$', views.deleteclassreport, name='deleteclassreport'),

)