# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('class_id', models.AutoField(serialize=False, primary_key=True)),
                ('class_name', models.CharField(max_length=100, verbose_name='\u8bfe\u7a0b\u540d\u79f0')),
                ('class_hours', models.IntegerField(verbose_name='\u8bfe\u65f6\u957f\u5ea6')),
                ('class_for', models.CharField(max_length=4, verbose_name='\u5b66\u751f\u5e74\u7ea7')),
                ('add_date', models.DateTimeField(default=datetime.datetime(2015, 4, 5, 17, 58, 10, 427000), verbose_name='\u6dfb\u52a0\u65e5\u671f', blank=True)),
                ('is_allowed_choose', models.CharField(default='\u5f00\u653e', max_length=50, verbose_name='\u662f\u5426\u5173\u95ed', choices=[('\u5f00\u653e', '\u5f00\u653e'), ('\u5173\u95ed', '\u5173\u95ed')])),
                ('exp_time_control', models.BooleanField(default=False, verbose_name='\u6307\u5b9a\u4e0a\u8bfe\u65f6\u95f4', choices=[(True, '\u6307\u5b9a'), (False, '\u4e0d\u6307\u5b9a')])),
                ('comment', models.TextField(default=None, verbose_name='\u5907\u6ce8', blank=True)),
                ('stu_num_now', models.IntegerField(default=0, verbose_name='\u5df2\u9009\u4eba\u6570')),
                ('startyear', models.IntegerField(default=2014, verbose_name='\u4ece\u5b66\u5e74')),
                ('endyear', models.IntegerField(default=2015, verbose_name='\u81f3\u5b66\u5e74')),
                ('semester', models.IntegerField(verbose_name='\u5f53\u524d\u5b66\u671f', choices=[(1, '\u7b2c\u4e00\u5b66\u671f'), (2, '\u7b2c\u4e8c\u5b66\u671f')])),
                ('teacher_list', models.CharField(max_length=100, verbose_name='\u4efb\u8bfe\u6559\u5e08')),
                ('deadline', models.DateField(verbose_name='\u622a\u81f3\u65e5\u671f', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClassTeacherShip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('classes', models.ForeignKey(to='classes.Classes')),
                ('teacher', models.ForeignKey(to='master.Administrator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExpRoom',
            fields=[
                ('classroomid', models.AutoField(serialize=False, primary_key=True)),
                ('semester_start_year', models.IntegerField(default=2014)),
                ('semester_end_year', models.IntegerField(default=2015)),
                ('semester', models.CharField(max_length=1, choices=[('1', '1'), ('2', '2')])),
                ('week', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('weekday', models.CharField(max_length=9, choices=[('\u4e00', '\u5468\u4e00'), ('\u4e8c', '\u5468\u4e8c'), ('\u4e09', '\u5468\u4e09'), ('\u56db', '\u5468\u56db'), ('\u4e94', '\u5468\u4e94'), ('\u516d', '\u5468\u516d'), ('\u65e5', '\u5468\u65e5')])),
                ('startclass', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14)])),
                ('endclass', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14)])),
                ('machinenum', models.IntegerField()),
                ('roomnum', models.IntegerField(default=0)),
                ('advise_class', models.CharField(default='\u4e0d\u9650', max_length=10, blank=True)),
                ('force_major', models.CharField(default='\u4e0d\u9650', max_length=50, blank=True)),
                ('is_full', models.BooleanField(default=False)),
                ('is_allowed_choose', models.BooleanField(default=True, verbose_name='', choices=[(True, '\u5f00\u653e'), (False, '\u5173\u95ed')])),
                ('stu_num_now', models.IntegerField(default=0, verbose_name='\u5df2\u9009\u4eba\u6570')),
                ('add_date', models.DateField(default=datetime.date(2015, 4, 5))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExpRoom2',
            fields=[
                ('classroomid', models.AutoField(serialize=False, primary_key=True)),
                ('semester_start_year', models.IntegerField(default=2014)),
                ('semester_end_year', models.IntegerField(default=2015)),
                ('semester', models.CharField(max_length=1, choices=[('1', '1'), ('2', '2')])),
                ('week', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('weekday', models.IntegerField(choices=[(1, '\u5468\u4e00'), (2, '\u5468\u4e8c'), (3, '\u5468\u4e09'), (4, '\u5468\u56db'), (5, '\u5468\u4e94'), (6, '\u5468\u516d'), (7, '\u5468\u65e5')])),
                ('machinenum', models.IntegerField()),
                ('startclass', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14)])),
                ('endclass', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14)])),
                ('is_full', models.BooleanField(default=False)),
                ('is_allowed_choose', models.BooleanField(default=True)),
                ('classes', models.ForeignKey(to='classes.Classes')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
