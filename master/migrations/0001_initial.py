# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('admin_name', models.CharField(max_length=30, null=True, blank=True)),
                ('admin_id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=256)),
                ('admin_type', models.IntegerField(default=2, max_length=10, verbose_name='\u7ba1\u7406\u5458\u7c7b\u578b', choices=[(1, '\u7ba1\u7406\u5458'), (2, '\u6559\u5e08')])),
                ('add_date', models.DateField(default=datetime.date(2015, 4, 5))),
                ('is_active', models.BooleanField(default=True, verbose_name='\u72b6\u6001', choices=[(True, '\u6fc0\u6d3b'), (False, '\u7981\u7528')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdminLogin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_ip', models.IPAddressField()),
                ('login_date', models.DateTimeField(default=datetime.datetime(2015, 4, 5, 17, 58, 10, 423000))),
                ('login_name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SysTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startyear', models.IntegerField(default=2014, verbose_name='\u4ece\u5b66\u5e74')),
                ('endyear', models.IntegerField(default=2015, verbose_name='\u81f3\u5b66\u5e74')),
                ('semester', models.IntegerField(verbose_name='\u5f53\u524d\u5b66\u671f', choices=[(1, '\u7b2c\u4e00\u5b66\u671f'), (2, '\u7b2c\u4e8c\u5b66\u671f')])),
                ('startday', models.DateField(blank=True)),
                ('systime', models.DateField(default=datetime.date(2015, 4, 5))),
                ('allow_class', models.BooleanField(default=True, verbose_name='\u5141\u8bb8\u9009\u8bfe', choices=[(True, '\u5f00\u653e'), (False, '\u5173\u95ed')])),
                ('allow_exproom', models.BooleanField(default=True, verbose_name='\u5141\u8bb8\u9009\u65f6\u95f4', choices=[(True, '\u5f00\u653e'), (False, '\u5173\u95ed')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
