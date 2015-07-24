# -*- coding: utf-8 -*-
from django import forms
from models import Student


class StudentLogForm(forms.Form):
    stu_id = forms.CharField(label=u'学号',required=True)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)
    required_css_class = 'required'


class ChangePassForm(forms.Form):
    newpass1 = forms.CharField(label=u'新密码', widget=forms.PasswordInput, required=True)
    newpass2 = forms.CharField(label=u'再输一次', widget=forms.PasswordInput, required=True)


class MyInfoForm(forms.Form):
    stu_name = forms.CharField(label=u'姓名')
    stu_grade = forms.CharField(label=u'年级')
    stu_class = forms.CharField(label=u'班级')
    stu_major = forms.CharField(label=u'专业')
    stu_phone = forms.CharField(label=u'手机')
    stu_sex_choices = (
        ('male', u'男'),
        ('female', u'女'),
    )
    stu_sex = forms.CharField(label=u'性别', widget=forms.Select(choices=stu_sex_choices), required=False)
    password1 = forms.CharField(label=u'新密码', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label=u'确认新密码', widget=forms.PasswordInput, required=False)
    password = forms.CharField(label=u'原密码', widget=forms.PasswordInput, required=False)

class ReportForm(forms.Form):
    report = forms.FileField(label=u'提交实验报告')

class ClassReportForm(forms.Form):
    class_report = forms.FileField(label=u'')
