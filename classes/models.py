# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
from master.models import Administrator

class Classes(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100, blank=False, verbose_name=u'课程名称')
    class_hours = models.IntegerField(blank=False, verbose_name=u'课时长度')
    class_for = models.CharField(max_length=4, verbose_name=u'学生年级')
    add_date = models.DateTimeField(default=datetime.now(), blank=True, verbose_name=u'添加日期')
    status_choice = ((u'开放', u'开放'), (u'关闭', u'关闭'))
    is_allowed_choose = models.CharField(max_length=50, choices=status_choice, default=u'开放', verbose_name=u'是否关闭')
    control_choice = ((True, u'指定'), (False, u'不指定'))
    exp_time_control = models.BooleanField(choices=control_choice, default=False, blank=True, verbose_name=u'指定上课时间')
    comment = models.TextField(blank=True, default=None, verbose_name=u'备注')
    stu_num_now = models.IntegerField(default=0, verbose_name=u'已选人数')
    startyear = models.IntegerField(default=int(date.today().year)-1, verbose_name=u'从学年')
    endyear = models.IntegerField(default=int(date.today().year), verbose_name=u'至学年')
    semester = models.IntegerField(choices=((1, u'第一学期'), (2, u'第二学期')), verbose_name=u'当前学期')
    teacher_list = models.CharField(verbose_name=u'任课教师', max_length=100)
    deadline = models.DateField(blank=True, verbose_name=u'截至日期')

    @property
    def thisyear(self):
        if self.add_date.year == date.today().year:
            return True

    def __unicode__(self):
        return unicode(self.class_name)


class ClassTeacherShip(models.Model):
    teacher = models.ForeignKey(Administrator)
    classes = models.ForeignKey(Classes)



class ExpRoom(models.Model):
    classroomid = models.AutoField(primary_key=True)
    #the semester start_year and over_year
    semester_start_year = models.IntegerField(default=datetime.now().year-1)
    semester_end_year = models.IntegerField(default=datetime.now().year)
    semester = models.CharField(max_length=1, choices=(('1', '1'), ('2', '2')))
    week = models.IntegerField(choices=((i, i) for i in range(1, 25)))
    weekday_choice = (
        (u'一', u'周一'),
        (u'二', u'周二'),
        (u'三', u'周三'),
        (u'四', u'周四'),
        (u'五', u'周五'),
        (u'六', u'周六'),
        (u'日', u'周日'),
    )
    weekday = models.CharField(choices=weekday_choice, max_length=9)
    startclass = models.IntegerField(choices=((i, i) for i in range(1, 15)))
    endclass = models.IntegerField(choices=((i, i) for i in range(1, 15)))
    machinenum = models.IntegerField()
    roomnum = models.IntegerField(default=0)
    advise_class = models.CharField(default=u'不限', blank=True, max_length=10)
    force_major = models.CharField(default=u'不限', blank=True, max_length=50)
    is_full = models.BooleanField(default=False)
    status_choice = ((True, u'开放'), (False, u'关闭'))
    is_allowed_choose = models.BooleanField(choices=status_choice, default=True, blank=True, verbose_name=u'')
    stu_num_now = models.IntegerField(default=0, verbose_name=u'已选人数')
    add_date = models.DateField(default=date.today())

    @property
    def yuliang(self):
        return self.machinenum - self.stu_num_now

    def weeknum(self):
        if self.weekday == u'一':
            return 1
        elif self.weekday == u'二':
            return 2
        elif self.weekday == u'三':
            return 3
        elif self.weekday == u'四':
            return 4
        elif self.weekday == u'五':
            return 5
        elif self.weekday == u'六':
            return 6
        elif self.weekday == u'七':
            return 7

    def __unicode__(self):
       return u'第' + str(self.week) + u'周   周'+ str(self.weekday) + \
              u" 第" + str(self.startclass) + "-" + str(self.endclass) + u'节'


class ExpRoom2(models.Model):
    classroomid = models.AutoField(primary_key=True)
    classes = models.ForeignKey(Classes)
    #the semester start_year and over_year
    semester_start_year = models.IntegerField(default=datetime.now().year-1)
    semester_end_year = models.IntegerField(default=datetime.now().year)
    semester = models.CharField(max_length=1, choices=(('1', '1'), ('2', '2')))
    week = models.IntegerField(choices=((i, i) for i in range(1, 25)))
    weekday_choice = (
        (1, u'周一'),
        (2, u'周二'),
        (3, u'周三'),
        (4, u'周四'),
        (5, u'周五'),
        (6, u'周六'),
        (7, u'周日'),
    )
    weekday = models.IntegerField(choices=weekday_choice)
    machinenum = models.IntegerField()
    startclass = models.IntegerField(choices=((i, i) for i in range(1, 15)))
    endclass = models.IntegerField(choices=((i, i) for i in range(1, 15)))
    is_full = models.BooleanField(default=False)
    is_allowed_choose = models.BooleanField(default=True)

    def __unicode__(self):
       return u'第' + str(self.week) + u'周 '+ \
              u'周' + str(self.weekday) + \
              u" 第" + str(self.startclass) +u'节 '+ u"至 " + \
              u'第'+ str(self.endclass)+ u'节'