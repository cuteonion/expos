# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from master.models import Administrator
from datetime import datetime
from DjangoUeditor.models import UEditorField
from datetime import date, datetime

# class Tags(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=40)
#
#     def __unicode__(self):
#         return self.name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, default=u'未分类')

    def __unicode__(self):
        return self.name


def get_file_path(instance, filename):
    import os
    ext = filename.split('.')[-1]
    filename = "%d-%d-%d-%s.%s" %(date.today().year, date.today().month, date.today().day, filename, ext)
    return os.path.join('files', filename)


class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False, verbose_name=u'标题')
    contents = UEditorField(
        u'正文',width=600, height=300, toolbars="full",imagePath="uploadimg/",filePath="uploadfile/", upload_settings={"imageMaxSize":1204000},blank=True)
    author = models.ForeignKey(Administrator, verbose_name=u'发布人')
    # tags = models.ManyToManyField(Tags, blank=True, verbose_name=u'标签')
    category = models.ForeignKey(Category, verbose_name=u'分类')
    now = datetime.now()
    create_date = models.DateTimeField(default=now)
    attachment = models.FileField(upload_to=get_file_path)

    def __unicode__(self):
        return self.title