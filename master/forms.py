# -*- coding: utf-8 -*-
from django import forms
from student.models import Student
import os
from django.forms.extras.widgets import SelectDateWidget
from news.models import News, Category

class MasterLoginForm(forms.Form):
    username = forms.CharField(label=u'帐号', max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label=u'密码', required=True)

class ChangePassForm(forms.Form):
    newpass1 = forms.CharField(label=u'新密码', widget=forms.PasswordInput, required=True)
    newpass2 = forms.CharField(label=u'再输一次', widget=forms.PasswordInput, required=True)


class SysTimeSetForm(forms.Form):
    startyear = forms.CharField(max_length=4, label=u'当前学年')
    endyear = forms.CharField(max_length=4, label=u'')
    semester = forms.CharField(
        max_length=1,
        label=u'当前学期',
        widget=forms.Select(
            choices=(
                (1, u'第一学期'),
                (2, u'第二学期'),
            )
        )
    )
    startday = forms.DateField(label=u'起始日期', widget=SelectDateWidget())




class OpenOrCloseForm(forms.Form):
    allow_class = forms.BooleanField(
        label=u'选课程',
        widget=forms.Select(
            choices=(
                (True, '开放'),
                (False, '关闭'),
            )
        ),
        required=False,
    )
    allow_exproom = forms.BooleanField(
        label=u'选时间',
        widget=forms.Select(
            choices=(
                (True, '开放'),
                (False, '关闭'),
            )
        ),
        required=False,
    )


class ImportStuForm(forms.Form):
    file = forms.FileField(label=u'选择一个文件', required=False, allow_empty_file=False)


class AddClassForm(forms.Form):
    class_name = forms.CharField(max_length=100,  label=u'课程名称')
    class_hours = forms.IntegerField(label=u'课程学时')
    class_for = forms.CharField(max_length=4, label=u'学生年级')
    deadline = forms.DateField(label=u'截至日期', widget=SelectDateWidget())
    comment = forms.CharField(label=u'课程说明', widget=forms.Textarea, required=False)

class OtheryearclassForm(forms.Form):
    startyear = forms.IntegerField(label=u'从')
    endyear = forms.IntegerField(label=u'至')
    semester = forms.IntegerField(label=u'学期', widget=forms.Select(choices=((2, u'第一学期'), (2, u'第二学期'))))


class EditClassForm(forms.Form):
    class_name = forms.CharField(max_length=100,  label=u'课程名称')
    class_hours = forms.IntegerField(label=u'课程学时')
    class_for = forms.CharField(max_length=4, label=u'学生年级')
    deadline = forms.DateField(label=u'截至日期', widget=SelectDateWidget())
    open_choice = ((u'开放', u'开放'), (u'关闭', u'关闭'))
    is_allowed_choose = forms.CharField(widget=forms.Select(choices=open_choice), label=u'允许选择')
    comment = forms.CharField(label=u'课程说明', widget=forms.TextInput, required=False)


class AddAdminForm(forms.Form):
    username = forms.CharField(label=u'登录账号', max_length=10)
    admin_name = forms.CharField(label=u'教师姓名', max_length=50)
    password = forms.CharField(label=u'设置密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'确认密码', widget=forms.PasswordInput)
    admin_type = forms.IntegerField(label=u'用户类型', widget=forms.Select(choices=((1, u'管理员'), (2, u'教师'))))


class EditAdminForm(forms.Form):
    admin_name = forms.CharField(label=u'教师姓名')
    admin_type = forms.IntegerField(label=u'用户类型', widget=forms.Select(choices=((1, u'管理员'), (2, u'教师'))))
    password1 = forms.CharField(label=u'修改密码', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label=u'确认密码', widget=forms.PasswordInput, required=False)

class AddStuByHandForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['stu_auth_num',
                  'stu_name',
                  'stu_grade',
                  'stu_class',
                  'stu_major',
                  'stu_phone']


class EditStuInfoForm(forms.Form):
    stu_name = forms.CharField(label=u'姓名')
    stu_grade = forms.CharField(label=u'年级')
    stu_class = forms.CharField(label=u'班级')
    stu_major = forms.CharField(label=u'专业')
    stu_sex_choices = (
        ('male', u'男'),
        ('female', u'女'),
    )
    stu_sex = forms.CharField(label=u'性别', widget=forms.Select(choices=stu_sex_choices), required=False)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput, required=False)


class AddExpRoomForm(forms.Form):
    week_choice = (
        (1, u'第一周'),
        (2, u'第二周'),
        (3, u'第三周'),
        (4, u'第四周'),
        (5, u'第五周'),
        (6, u'第六周'),
        (7, u'第七周'),
        (8, u'第八周'),
        (9, u'第九周'),
        (10, u'第十周'),
        (11, u'第十一周'),
        (12, u'第十二周'),
        (13, u'第十三周'),
        (14, u'第十四周'),
        (15, u'第十五周'),
        (16, u'第十六周'),
        (17, u'第十七周'),
        (18, u'第十八周'),
        (19, u'第十九周'),
        (20, u'第二十周'),
        (21, u'第二十一周'),
        (22, u'第二十二周'),
        (23, u'第二十三周'),
        (24, u'第二十四周'),
        (25, u'第二十五周'),
    )
    week = forms.IntegerField(label=u'教学周数', widget=forms.Select(choices=week_choice), required=True)
    weekday_choice = (
        (u'一', u'一'),
        (u'二', u'二'),
        (u'三', u'三'),
        (u'四', u'四'),
        (u'五', u'五'),
        (u'六', u'六'),
        (u'日', u'日'),
    )
    weekday = forms.CharField(label=u'星    期', widget=forms.Select(choices=weekday_choice))
    startclass = forms.IntegerField(widget=forms.Select(choices=((i, i) for i in range(1, 15))), label=u'起始节次')
    endclass = forms.IntegerField(widget=forms.Select(choices=((i, i) for i in range(1, 15))), label=u'结束节次')
    roomfiledir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'roomnumber.txt')
    roomfile = open(roomfiledir)
    lines = roomfile.readlines()
    room_choice = list()
    roomfile.close()
    for line in lines:
        room_choice.append((int(line), str(int(line))))
    roomnum = forms.IntegerField(label=u'上课教室', widget=forms.Select(choices=room_choice), required=True)
    machinenum = forms.IntegerField(label=u'机位数量')
    from classes.models import Classes
    try:
        classes = Classes.objects.filter().order_by("-add_date")
        clas = list()
        clas.append((u'不限', u'不限'))
        for objects in classes:
            if (objects.class_name, objects.class_name) not in clas:
                clas.append((objects.class_name, objects.class_name))
    except:
        clas = list()
        clas.append((u'不限', u'不限'))
    clas = tuple(clas)
    advise_class = forms.CharField(label=u'限选课程', widget=forms.Select(choices=clas), required=True)
    from student.models import Student
    major_list = [(u'不限', u'不限')]
    try:
        major_list_1 = Student.objects.values_list("stu_major", flat=True)
        major_list_1 = list(major_list_1)
        for major in major_list_1:
            if (major, major) not in major_list:
                major_list.append((major, major))
        major_list = tuple(major_list)
    except:
        major_list = tuple(major_list)
    force_major = forms.CharField(label=u'限选专业', widget=forms.Select(choices=major_list), required=True)


#u"此处需要重构，与AddExpRoomForm有大量重复的地方"
class EditExpRoomForm(forms.Form):
    week_choice = (
        (1, u'第一周'),
        (2, u'第二周'),
        (3, u'第三周'),
        (4, u'第四周'),
        (5, u'第五周'),
        (6, u'第六周'),
        (7, u'第七周'),
        (8, u'第八周'),
        (9, u'第九周'),
        (10, u'第十周'),
        (11, u'第十一周'),
        (12, u'第十二周'),
        (13, u'第十三周'),
        (14, u'第十四周'),
        (15, u'第十五周'),
        (16, u'第十六周'),
        (17, u'第十七周'),
        (18, u'第十八周'),
        (19, u'第十九周'),
        (20, u'第二十周'),
        (21, u'第二十一周'),
        (22, u'第二十二周'),
        (23, u'第二十三周'),
        (24, u'第二十四周'),
        (25, u'第二十五周'),
    )
    week = forms.IntegerField(label=u'教学周数', widget=forms.Select(choices=week_choice), required=True)
    weekday_choice = (
        (u'一', u'一'),
        (u'二', u'二'),
        (u'三', u'三'),
        (u'四', u'四'),
        (u'五', u'五'),
        (u'六', u'六'),
        (u'日', u'日'),
    )
    weekday = forms.CharField(label='星    期', widget=forms.Select(choices=weekday_choice))
    startclass = forms.IntegerField(widget=forms.Select(choices=((i, i) for i in range(1, 15))), label=u'起始节次')
    endclass = forms.IntegerField(widget=forms.Select(choices=((i, i) for i in range(1, 15))), label=u'结束节次')
    roomfiledir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'roomnumber.txt')
    roomfile = open(roomfiledir)
    lines = roomfile.readlines()
    roomfile.close()
    room_choice = list()
    for line in lines:
        room_choice.append((int(line), str(int(line))))
    roomnum = forms.IntegerField(label=u'上课教室', widget=forms.Select(choices=room_choice), required=True)
    machinenum = forms.IntegerField(label=u'机位数量')
    from classes.models import Classes
    try:
        classes = Classes.objects.filter().order_by("-add_date")
        clas = list()
        clas.append((u'不限', u'不限'))
        for objects in classes:
            if (objects.class_name, objects.class_name) not in clas:
                clas.append((objects.class_name, objects.class_name))
    except:
        clas = list()
        clas.append((u'不限', u'不限'))
    clas = tuple(clas)
    advise_class = forms.CharField(label=u'限选课程', widget=forms.Select(choices=clas), required=True)
    from student.models import Student
    major_list = [(u'不限', u'不限')]
    try:
        major_list_1 = Student.objects.values_list("stu_major", flat=True)
        major_list_1 = list(major_list_1)
        for major in major_list_1:
            if (major, major) not in major_list:
                major_list.append((major, major))
        major_list = tuple(major_list)
    except:
        major_list = tuple(major_list)
    force_major = forms.CharField(label=u'限选专业', widget=forms.Select(choices=major_list), required=True)
    allowed_choice = ((True, u'允许'), (False, u'不允许'))
    is_allowed_choose = forms.BooleanField(label=u'允许选择', widget=forms.Select(choices=allowed_choice), required=False)


class ViewOtherExpRoomForm(forms.Form):
    semester_start_year = forms.IntegerField(label=u'学年', required=True)
    semester_end_year = forms.IntegerField(label=u'', required=True)
    semester = forms.CharField(label=u'学期', widget=forms.Select(choices=(('1', u'第一学期'), ('2', u'第二学期'))), required=True)


class AddStudentToClassForm(forms.Form):
    student = forms.IntegerField(label=u'学号', required=True)

from  DjangoUeditor.widgets import UEditorWidget
from  DjangoUeditor.forms import UEditorField

class AddNewsForm(forms.Form):
    categorys = Category.objects.all()
    category_choice = ((category.id, category.name) for category in categorys)
    title = forms.CharField(label=u'标题', max_length=200)
    category = forms.IntegerField(widget=forms.Select(choices=category_choice), label=u'分类')
    contents = UEditorField("描述",initial="",width=800,height=600,imagePath="uploadimg/",filePath="uploadfile/")
    # contents = forms.CharField(label=u'正文', widget=forms.Textarea)
    attachment = forms.FileField(label=u'附件', required=False)


class AddCategoryForm(forms.Form):
    category = forms.CharField(label=u'添加类别')


class CommitClassForm(forms.Form):
    class_grades = forms.CharField(label=u'成绩',required=False)
    teacher_commit = forms.CharField(label=u'点评', widget=forms.Textarea, required=False)

class ClassReportForm(forms.Form):
    class_report = forms.FileField(label=u'')