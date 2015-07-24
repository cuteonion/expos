# -*- coding: utf-8 -*-
from django import forms
from classes.models import Classes, ExpRoom





class AddExproom(forms.Form):
    semester_start_year = forms.CharField()
    semester_end_year = forms.CharField()
    semester = forms.IntegerField()
    week = forms.IntegerField(widget=forms.Select((i,i) for i in range(1,25)))
    weekday_choice = (
        (1, u'周一'),
        (2, u'周二'),
        (3, u'周三'),
        (4, u'周四'),
        (5, u'周五'),
        (6, u'周六'),
        (7, u'周日'),
    )
    weekday = forms.IntegerField(widget=forms.Select(weekday_choice))
    startclass = forms.IntegerField(widget=forms.Select((i,i) for i in range(1,13)))
    endclass = forms.IntegerField(widget=forms.Select((i,i) for i in range(1,13)))