# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from classes.models import Classes, ExpRoom
from datetime import datetime, date
# from django.core.urlresolvers import reverse
# from django.contrib.auth.models import User
# # from django.core.files.storage import FileSystemStorage
# from django.conf import settings


class Student(models.Model):
    stu_auth_num = models.CharField(max_length=10, primary_key=True, unique=True, verbose_name=u"学号")
    password = models.CharField(max_length=256, verbose_name=u'密码', default='000000')
    stu_name = models.CharField(max_length=50, verbose_name=u"姓名")
    stu_grade = models.CharField(max_length=4, verbose_name=u'年级')
    stu_class = models.CharField(max_length=8, db_column="stu_class", verbose_name=u"班级")
    stu_major = models.CharField(max_length=100, verbose_name=u"专业")
    stu_sex_choices = (
        ('male', u'男'),
        ('female', u'女'),
    )
    stu_sex = models.CharField(max_length=6, choices=stu_sex_choices, blank=True)
    stu_email = models.EmailField(blank=True)
    stu_phone = models.CharField(max_length=11, verbose_name=u'电话', default=None, blank=True)
    logined_in = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True, verbose_name=u'活动账户')

    def __unicode__(self):
        return unicode(self.stu_auth_num)


def classreport_filename(instance, filename):
    import os
    ext = filename.split('.')[-1]
    filename = "%s-%s-%d-%d-%d-classreport.%s" %(instance.stu_id.stu_auth_num, instance.class_id.class_id, date.today().year, date.today().month, date.today().day, ext)
    return os.path.join('classreports', filename)


class StuClass(models.Model):
    stu_id = models.ForeignKey(Student, verbose_name=u'学生姓名')
    class_id = models.ForeignKey(Classes, verbose_name=u'已选课程')
    already_hours = models.IntegerField()
    class_report = models.FileField(blank=True, upload_to=classreport_filename, default=None)
    class_grades = models.IntegerField(choices=((i, i)for i in range(1, 100)), blank=True)
    class_is_start = models.BooleanField(default=False)
    class_is_finished = models.BooleanField(default=False)
    report_date = models.DateField(default=date.today(), blank=True)
    teacher_commit = models.CharField(blank=True, verbose_name=u'评价', max_length=200)
    @property
    def remain_hours(self):
        if self.already_hours >= self.class_id.class_hours:
            return 0
        else:
            return self.class_id.class_hours - self.already_hours

    def __unicode__(self):
        return unicode(self.stu_id) + '-' + unicode(self.class_id.class_name)


#u"在正式部署时去掉blank=true，这里是为了开发时同步数据库方便"
class StuSelExpTime(models.Model):
    exproom_id = models.ForeignKey(ExpRoom)
    stu_id = models.ForeignKey(Student, verbose_name=u'学号')
    hours = models.IntegerField()
    time_week = models.IntegerField(default=1)
    seat_num = models.IntegerField(default=0, blank=False)
    is_start = models.BooleanField(default=False, blank=True)
    is_finished = models.BooleanField(default=False, blank=True)
    is_missed = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return unicode(self.exproom_id)
#unicode(self.stu_id) +

def update_filename(instance, filename):
    import os
    ext = filename.split('.')[-1]
    filename = "%s-%d-%d-%d-%d-expreport.%s" % (instance.stu_id.stu_auth_num, instance.stu_class.class_id.class_id, date.today().year, date.today().month, date.today().day, ext)
    return os.path.join('expreports', filename)


class StuDoExp(models.Model):
    stu_id = models.ForeignKey(Student)
    stuseltime_id = models.ForeignKey(StuSelExpTime)
    start_time = models.DateTimeField(default=datetime.now(), blank=True)
    end_time = models.DateTimeField(blank=True, default=datetime.now())
    stu_class = models.ForeignKey(StuClass)
    stu_exp_report = models.FileField(blank=True, upload_to=update_filename)
    #remember to modify the two fields
    # stu_exp_report_path = models.FilePathField(blank=True)
    teacher_comment = models.TextField(blank=True)
    stu_start_ip = models.IPAddressField(blank=True)
    stu_finish_ip = models.IPAddressField(blank=True)
    is_finished = models.BooleanField(blank=True, default=False)
    exp_grade = models.CharField(blank=True, max_length=20)
    comment = models.CharField(blank=True, max_length=200)

    def __unicode__(self):
        return unicode(self.stu_id.stu_auth_num) + unicode(self.stu_class.class_id.class_name)

    @property
    def hours(self):
        return self.stuseltime_id.hours
