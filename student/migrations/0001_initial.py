# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import student.models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StuClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('already_hours', models.IntegerField()),
                ('class_report', models.FileField(default=None, upload_to=student.models.classreport_filename, blank=True)),
                ('class_grades', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (64, 64), (65, 65), (66, 66), (67, 67), (68, 68), (69, 69), (70, 70), (71, 71), (72, 72), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (78, 78), (79, 79), (80, 80), (81, 81), (82, 82), (83, 83), (84, 84), (85, 85), (86, 86), (87, 87), (88, 88), (89, 89), (90, 90), (91, 91), (92, 92), (93, 93), (94, 94), (95, 95), (96, 96), (97, 97), (98, 98), (99, 99)])),
                ('class_is_start', models.BooleanField(default=False)),
                ('class_is_finished', models.BooleanField(default=False)),
                ('report_date', models.DateField(default=datetime.date(2015, 4, 5), blank=True)),
                ('teacher_commit', models.CharField(max_length=200, verbose_name='\u8bc4\u4ef7', blank=True)),
                ('class_id', models.ForeignKey(verbose_name='\u5df2\u9009\u8bfe\u7a0b', to='classes.Classes')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('stu_auth_num', models.CharField(max_length=10, unique=True, serialize=False, verbose_name='\u5b66\u53f7', primary_key=True)),
                ('password', models.CharField(default='000000', max_length=256, verbose_name='\u5bc6\u7801')),
                ('stu_name', models.CharField(max_length=50, verbose_name='\u59d3\u540d')),
                ('stu_grade', models.CharField(max_length=4, verbose_name='\u5e74\u7ea7')),
                ('stu_class', models.CharField(max_length=8, verbose_name='\u73ed\u7ea7', db_column='stu_class')),
                ('stu_major', models.CharField(max_length=100, verbose_name='\u4e13\u4e1a')),
                ('stu_sex', models.CharField(blank=True, max_length=6, choices=[('male', '\u7537'), ('female', '\u5973')])),
                ('stu_email', models.EmailField(max_length=75, blank=True)),
                ('stu_phone', models.CharField(default=None, max_length=11, verbose_name='\u7535\u8bdd', blank=True)),
                ('logined_in', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='\u6d3b\u52a8\u8d26\u6237')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StuDoExp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(default=datetime.datetime(2015, 4, 5, 17, 58, 10, 458000), blank=True)),
                ('end_time', models.DateTimeField(default=datetime.datetime(2015, 4, 5, 17, 58, 10, 458000), blank=True)),
                ('stu_exp_report', models.FileField(upload_to=student.models.update_filename, blank=True)),
                ('teacher_comment', models.TextField(blank=True)),
                ('stu_start_ip', models.IPAddressField(blank=True)),
                ('stu_finish_ip', models.IPAddressField(blank=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('exp_grade', models.CharField(max_length=20, blank=True)),
                ('comment', models.CharField(max_length=200, blank=True)),
                ('stu_class', models.ForeignKey(to='student.StuClass')),
                ('stu_id', models.ForeignKey(to='student.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StuSelExpTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hours', models.IntegerField()),
                ('time_week', models.IntegerField(default=1)),
                ('seat_num', models.IntegerField(default=0)),
                ('is_start', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('is_missed', models.BooleanField(default=False)),
                ('exproom_id', models.ForeignKey(to='classes.ExpRoom')),
                ('stu_id', models.ForeignKey(verbose_name='\u5b66\u53f7', to='student.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='studoexp',
            name='stuseltime_id',
            field=models.ForeignKey(to='student.StuSelExpTime'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stuclass',
            name='stu_id',
            field=models.ForeignKey(verbose_name='\u5b66\u751f\u59d3\u540d', to='student.Student'),
            preserve_default=True,
        ),
    ]
