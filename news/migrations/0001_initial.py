# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models
import news.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default='\u672a\u5206\u7c7b', max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='\u6807\u9898')),
                ('contents', DjangoUeditor.models.UEditorField(verbose_name='\u6b63\u6587', blank=True)),
                ('create_date', models.DateTimeField(default=datetime.datetime(2015, 4, 5, 17, 58, 10, 447000))),
                ('attachment', models.FileField(upload_to=news.models.get_file_path)),
                ('author', models.ForeignKey(verbose_name='\u53d1\u5e03\u4eba', to='master.Administrator')),
                ('category', models.ForeignKey(verbose_name='\u5206\u7c7b', to='news.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
