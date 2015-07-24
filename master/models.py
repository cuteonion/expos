# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime


class Administrator(models.Model):
    admin_name = models.CharField(max_length=30, null=True, blank=True)
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=256)
    admin_type = models.IntegerField(choices=((1, u'管理员'), (2, u'教师')), default=2, max_length=10, verbose_name=u'管理员类型')
    add_date = models.DateField(default=date.today())
    is_active = models.BooleanField(default=True, verbose_name=u'状态', choices=((True, u'激活'), (False, u'禁用')))

    def __unicode__(self):
        return self.admin_name

    @property
    def is_teacher(self):
        if self.admin_type == 2:
            return True

    def is_admin(self):
        if self.admin_type == 1:
            return True


class AdminLogin(models.Model):
    login_ip = models.IPAddressField()
    login_date = models.DateTimeField(default=datetime.now())
    login_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.login_name


class SysTime(models.Model):
    startyear = models.IntegerField(default=int(date.today().year)-1, verbose_name=u'从学年')
    endyear = models.IntegerField(default=int(date.today().year), verbose_name=u'至学年')
    semester = models.IntegerField(choices=((1, u'第一学期'), (2, u'第二学期')), verbose_name=u'当前学期')
    startday = models.DateField(blank=True)
    systime = models.DateField(default=date.today())
    status_choice = ((True, u'开放'), (False, u'关闭'))
    allow_class = models.BooleanField(default=True, choices=status_choice, verbose_name=u'允许选课')
    allow_exproom = models.BooleanField(default=True, choices=status_choice, verbose_name=u'允许选时间')


    def __unicode__(self):
        return str(self.systime)

