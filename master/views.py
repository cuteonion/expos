# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
import forms
from master.models import Administrator, SysTime
from classes.models import *
from student.models import *
import hashlib
import xlrd
from datetime import date
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from news.models import News, Category
from django.conf import settings


#u'管理员默认首页（其实也就是登录页面）'
def index(request):
    """
    u'管理员默认首页，/master/'
    """
    username = request.session.get('username', False)
    if username:
        return HttpResponseRedirect('/master/work')
    else:
        form = forms.MasterLoginForm
        error_message = ''
        return render(request, 'master/login.html', {'form': form, 'error_message': error_message})


#u'管理员登录View'
def masterlogin(request):
    """
    u'管理员登录验证'
    """
    if request.method == 'POST':
        form = forms.MasterLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                administrator = Administrator.objects.get(username=username)
            except:
                administrator = None
            if administrator and (hashlib.md5(password).hexdigest() == administrator.password) and administrator.is_active:
                request.session['username'] = administrator.username
                request.session.set_expiry(0)
                if administrator.admin_type == 1:
                    request.session['admin_type'] = 1
                elif administrator.admin_type == 2:
                    request.session['admin_type'] =2
                else:
                    pass
                return HttpResponseRedirect('/master/work')
            else:
                context = {'error_message': u'用户名与密码不符或您的帐号已被禁用', 'form': form}
                return render(request, 'master/login.html', context)
        else:
            context = {'error_message': u'用户名与密码不符或您的帐号已被禁用', 'form': form}
            return render(request, 'master/login.html', context)
    else:
        return HttpResponseRedirect('/master')

def isadmin(username):
    admin = Administrator.objects.get(username=username)
    if admin.admin_type == 1:
        return True
    else:
        return False

#u'后台管理页面'
def work(request):
    username = request.session.get('username', False)
    if username:
        admin = Administrator.objects.get(username=request.session['username'])
        if admin.admin_type == 1:
            admin = True
        else:
            admin = False
        return render(request, 'master/work.html', {'admin': admin})
    else:
        return index(request)


#u'管理员注销'
def masterlogout(request):
    try:
        del request.session['username']
        request.session.flush()
        return index(request)
    except:
        return index(request)


#u'管理员修改密码'
def changepass(request):
    if request.session.get('username', False):
        administrator = Administrator.objects.get(username=request.session['username'])
        form = forms.ChangePassForm(request.POST)
        changeform = forms.ChangePassForm
        if form.is_valid():
            newpass1 = form.cleaned_data['newpass1']
            newpass2 = form.cleaned_data['newpass2']
            print(newpass1)
            if newpass1 == newpass2:
                newpass = hashlib.md5(newpass1).hexdigest()
                administrator.password = newpass
                administrator.save()
                context = {'successmessage': u'修改成功', 'admin': isadmin(request.session['username'])}
                del request.session['username']
                request.session.flush()
                return render(request, 'master/success.html', context)
            else:
                failmessage = u'两次密码不一致'
                context = {'failmessage': failmessage, 'form': changeform, 'admin': isadmin(request.session['username'])}
                return render(request, 'master/change.html', context)
        else:
            failmessage = ''
            context = {'failmessage': failmessage, 'form': changeform, 'admin': isadmin(request.session['username'])}
            return render(request, 'master/change.html', context)
    else:
        return HttpResponseRedirect('/master')


#u'添加管理员'
def addadmin(request):
    if request.session.get('username', False):
        admin = Administrator.objects.get(username=request.session['username'])
        if admin.admin_type == 1:
            allow = True
        else:
            allow = False
        if request.method == 'POST' and allow:
            form = forms.AddAdminForm(request.POST)
            if form.is_valid():
                try:
                    admin = Administrator.objects.get(username=form.cleaned_data['username'])
                    print admin
                    message = u'添加失败，用户名已经存在'
                    admin_list = Administrator.objects.all()
                    return render(
                        request,
                        'master/addadmin.html',
                        {'message': message, 'admin_list': admin_list, 'form': forms.AddAdminForm, 'admin': isadmin(request.session['username'])}
                    )
                except:
                    password = form.cleaned_data['password'],
                    password2 = form.cleaned_data['password2'],
                    if password == password2:
                        admin = Administrator(
                            admin_name=form.cleaned_data['admin_name'],
                            username=form.cleaned_data['username'],
                            password=hashlib.md5(form.cleaned_data['password']).hexdigest(),
                            admin_type=form.cleaned_data['admin_type'],
                        )
                        admin.save()
                        message = u'添加成功'
                        admin_list = Administrator.objects.all()
                        return render(
                            request,
                            'master/addadmin.html',
                            {'message': message, 'admin_list': admin_list, 'form': None, 'admin': isadmin(request.session['username'])}
                        )
                    else:
                        message = u'添加失败'
                        admin_list = Administrator.objects.all()
                        return render(
                            request,
                            'master/addadmin.html',
                            {'message': message, 'admin_list': admin_list, 'form': forms.AddAdminForm, 'admin': isadmin(request.session['username'])}
                        )
            else:
                message = u'添加失败'
                admin_list = Administrator.objects.all()
                return render(
                    request,
                    'master/addadmin.html',
                    {'form': forms.AddAdminForm, 'message': message, 'admin_list': admin_list,  'admin': isadmin(request.session['username'])}
                )
        else:
            admin_list = Administrator.objects.all()
            form = forms.AddAdminForm
            return render(
                request,
                'master/addadmin.html',
                {'message': None, 'admin_list': admin_list, 'form': form, 'admin': isadmin(request.session['username'])}
            )
    else:
        return HttpResponseRedirect('/master')


def forbidadmin(request, username):
    if request.session.get('username', False):
        admin = Administrator.objects.get(username=request.session['username'])
        if admin.admin_type == 1:
            try:
                user = Administrator.objects.get(username=username)
                user.is_active = False
                user.save()
                message = u'禁用成功'
            except:
                message = u'操作失败'
            admin_list = Administrator.objects.all()
            return render(
                request,
                'master/mastermanage/mastermanage.html',
                {'form': forms.AddAdminForm, 'message':message, 'admin_list': admin_list, 'admin': isadmin(request.session['username'])}
            )
    else:
        return HttpResponseRedirect('/master')

def activeadmin(request, username):
    if request.session.get('username', False):
        admin = Administrator.objects.get(username=request.session['username'])
        if admin.admin_type == 1:
            try:
                user = Administrator.objects.get(username=username)
                user.is_active = True
                user.save()
                message = u'禁用成功'
            except:
                message = u'操作失败'
            admin_list = Administrator.objects.all()
            return render(
                request,
                'master/mastermanage/mastermanage.html',
                {'form': forms.AddAdminForm, 'message':message, 'admin_list': admin_list, 'admin': isadmin(request.session['username'])}
            )
    else:
        return HttpResponse('/master')


class AdminListView(ListView):
    queryset = Administrator.objects.all()
    context_object_name = 'admin_list'
    template_name = 'master/mastermanage/mastermanage.html'

    def get_context_data(self, **kwargs):
        context = super(AdminListView, self).get_context_data(**kwargs)
        context['admin'] = isadmin(self.request.session['username'])
        context['form'] = forms.AddAdminForm,
        return context


class EditAdminView(View):
    template_name = 'master/mastermanage/editadmin.html'
    form_class = forms.EditAdminForm

    def get(self, request, username):
        if request.session.get('username', False):
            admin = Administrator.objects.get(username=request.session.get('username'))
            if admin.admin_type == 1:
                teacher = Administrator.objects.get(username=username)
                print teacher
                form = self.form_class(
                    initial={
                        'admin_name':teacher.admin_name,
                        'admin_type':teacher.admin_type,
                    }
                )
                return render(
                    request,
                    self.template_name,
                    {'form': form, 'teacher': teacher, 'admin': isadmin(request.session['username'])}
                )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request, username):
        if request.session.get('username', False):
            admin = Administrator.objects.get(username=request.session['username'])
            if admin.admin_type == 1:
                teacher = Administrator.objects.get(username=username)
                form = self.form_class(request.POST)
                if form.is_valid():
                    teacher.admin_name=form.cleaned_data['admin_name']
                    teacher.admin_type=form.cleaned_data['admin_type']
                    teacher.save()
                    if form.cleaned_data['password1'] and (form.cleaned_data['password1'] == form.cleaned_data['password2']):
                        teacher.password = hashlib.md5(form.cleaned_data['password1']).hexdigest()
                        teacher.save()
                    message = u'修改成功'
                else:
                    message = u'您的输入有误'
                form = self.form_class(
                    initial={
                        'admin_name':teacher.admin_name,
                        'admin_type':teacher.admin_type,
                    }
                )
                return render(
                    request,
                    self.template_name,
                    {'form': form, 'message': message, 'teacher': teacher, 'admin': isadmin(request.session['username'])}
                )
        else:
            return HttpResponseRedirect('/master')


#u'关闭或者开放选课'
class OpenOrClose(View):
    form_class = forms.OpenOrCloseForm
    template_name = 'master/syssetting/openorclose.html'

    def get(self, request):
        if request.session.get('username', False):
            try:
                systime = SysTime.objects.get(pk=1)
                form = self.form_class(
                    initial={
                        'allow_class': systime.allow_class,
                        'allow_exproom': systime.allow_exproom,
                    }
                )
                message = u'当前选课与选取实验时间情况'
                return render(
                    request,
                    self.template_name,
                    {'form': form, 'message': message, 'admin': isadmin(request.session['username'])}
                )
            except:
                systime = SysTime(
                    stratyear=int(date.today().year)-1,
                    endyear=int(date.today().year),
                    semester=1,
                    allow_class=True,
                    allow_exproom=True,
                )
                systime.save()
                form = self.form_class(
                    initial={
                        'allow_class': systime.allow_class,
                        'allow_exproom': systime.allow_exproom,
                    }
                )
                return render(
                    request,
                    self.template_name,
                    {'form': form, 'admin': isadmin(request.session['username']), 'admin': isadmin(request.session['username'])}
                )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request):
        if request.session.get('username', False):
            form = self.form_class(request.POST)
            systime = SysTime.objects.get(pk=1)
            if form.is_valid():
                systime.allow_class = form.cleaned_data['allow_class']
                systime.allow_exproom = form.cleaned_data['allow_exproom']
                systime.save()
                message = u'当前选课与选取实验时间情况'
                form = self.form_class(
                    initial={
                        'allow_class': systime.allow_class,
                        'allow_exproom': systime.allow_exproom,
                    }
                )
                return render(
                    request,
                    self.template_name,
                    {'form': form, 'message': message, 'admin': isadmin(request.session['username'])}
                )
        else:
            return HttpResponseRedirect('/master')


#u'系统时间设置'
class SysTimeSet(View):
    form_class = forms.SysTimeSetForm
    template_name = 'master/syssetting/systimeset.html'

    def get(self, request):
        if request.session.get('username', False):
            try:
                systime = SysTime.objects.get(pk=1)
            except:
                systime = SysTime(
                    startyear=date.today().year-1,
                    endyear=date.today().year,
                    semester=1,
                    startday=date.today()

                )
                systime.save()
            finally:
                form = self.form_class(
                    initial={
                        'startyear': systime.startyear,
                        'endyear': systime.endyear,
                        'semester': systime.semester,
                        'startday': systime.startday,
                    }
                )
                return render(
                    request,
                    self.template_name,
                    {'form': form, 'admin': isadmin(request.session['username'])}
                )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request):
        if request.session.get('username', False):
            form = self.form_class(request.POST)
            if form.is_valid():
                systime = SysTime.objects.get(pk=1)
                systime.startyear = form.cleaned_data['startyear']
                systime.endyear = form.cleaned_data['endyear']
                systime.semester = form.cleaned_data['semester']
                systime.startday = form.cleaned_data['startday']
                systime.save()
                message = u'修改成功'
            else:
                message = u'您的输入有误'
                form = self.form_class
            return render(
                request,
                self.template_name,
                {'message': message, 'form': form, 'admin': isadmin(request.session['username'])}
            )
        else:
            return HttpResponseRedirect('/master')


#u'从excel中导入学生信息'
def importstudents(request):
    if request.session.get('username', False):
        if request.method == 'POST':
            form = forms.ImportStuForm(request.FILES)
            if form.is_valid():
                try:
                    files = request.FILES['file']
                    data = xlrd.open_workbook(file_contents=files.read())
                    table = data.sheets()[0]
                    nrows = table.nrows
                    try:
                        stu_list = list()
                        for i in range(1, nrows):
                            row = table.row_values(i)
                            student = Student(
                                stu_auth_num=int(row[0]),
                                password=hashlib.md5(str(int(row[0]))).hexdigest(),
                                stu_name=row[1],
                                stu_grade=str(int(row[2])),
                                stu_class=str(int(row[3])),
                                stu_major=row[4])
                            student.save()
                            stu_list.append(student)
                        messages = (u'已导入成功以下学生的信息',)
                        return render(
                            request,
                            'master/student/importstudents.html',
                            {'messages': messages, 'stu_list': stu_list, 'admin': isadmin(request.session['username'])}
                        )
                    except:
                        messages = (u'请按照提示排列学生信息',)
                        showimage = True
                        form = forms.ImportStuForm
                        return render(
                            request,
                            'master/student/importstudents.html',
                            {'form': form, 'messages': messages, 'showimage': showimage, 'admin': isadmin(request.session['username'])}
                        )
                except:
                    messages = (u'请上传excel文件',)
                    showimage = True
                    form = forms.ImportStuForm
                    return render(
                        request,
                        'master/student/importstudents.html',
                        {'form': form, 'messages': messages, 'showimage': showimage, 'admin': isadmin(request.session['username'])}
                    )
            else:
                return HttpResponse("SOMETHING WRONG")
        else:
            messages = (
                u'请导入excel文件(.xls结尾)',
                u"请按照\"学号\"，\"姓名\"，\"年级\"，\"班号\"，\"专业\"的顺序排列学生信息",
                u"默认密码为学号",
            )
            form = forms.ImportStuForm
            image = True
            return render(
                request,
                'master/student/importstudents.html',
                {'messages': messages, 'form': form, 'image': image, 'admin': isadmin(request.session['username'])}
            )
    else:
        return HttpResponseRedirect('/master')


#u'手动添加学生'
def addstubyhand(request):
    if request.session.get('username', False):
        if request.method == 'POST':
            form = forms.AddStuByHandForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.password = hashlib.md5(str(form.cleaned_data['stu_auth_num'])).hexdigest()
                student.save()
                message = u'添加成功'
                return render(
                    request,
                    'master/student/addstubyhand.html',
                    {'message': message, 'form': None, 'student': student, 'admin': isadmin(request.session['username'])}
                )
            else:
                message = u'您的输入有误'
                form = forms.AddStuByHandForm
                return render(
                    request,
                    'master/student/addstubyhand.html',
                    {'form': form, 'message': message, 'admin': isadmin(request.session['username'])}
                )
        else:
            form = forms.AddStuByHandForm
            return render(
                request,
                'master/student/addstubyhand.html',
                {'form': form, 'message': None, 'admin': isadmin(request.session['username'])}
            )
    else:
        return HttpResponseRedirect('/master')


#u'查看学生信息'
def viewstuinfo(request):
    if request.session.get('username', False):
        if request.method == 'POST':
            first = False
            if request.POST['action'] == 'bynum':
                student = Student.objects.filter(
                    stu_auth_num=str(request.POST['stu_auth_num'])
                )
            elif request.POST['action'] == 'bygrade':
                student = Student.objects.filter(stu_grade=str(request.POST['stu_grade']))
                return render(
                    request,
                    'master/student/viewstuinfo.html',
                    {'bynum': False, 'student': student, 'admin': isadmin(request.session['username'])}
                )
            elif request.POST['action'] == 'byclassormajor':
                if request.POST['stu_class'] and request.POST['stu_major']:
                    student = Student.objects.filter(
                        stu_class=request.POST['stu_class'],
                        stu_major=request.POST['stu_major'],
                    )
                elif request.POST['stu_class']:
                    student = Student.objects.filter(stu_class=request.POST['stu_class'])
                elif request.POST['stu_major']:
                    student = Student.objects.filter(stu_major=request.POST['stu_major'])
                else:
                    first = True
                    student = None
            else:
                first = True
                student = None
        else:
            first = True
            student = None
        return render(
            request,
            'master/student/viewstuinfo.html',
            {'first': first, 'student': student, 'admin': isadmin(request.session['username'])},
        )
    else:
        return HttpResponseRedirect('/master')


def forbidonestudent(request, stu_auth_num):
    if request.session.get('username', False):
        student = Student.objects.get(stu_auth_num=stu_auth_num)
        student.is_active = False
        student.save()
        message = u'禁用成功'
        return render(
            request,
            'master/student/viewstuinfo.html',
            {'message': message, 'admin': isadmin(request.session['username'])}
        )
    else:
        return HttpResponseRedirect('/master')

def activeonestudent(request, stu_auth_num):
    if request.session.get('username', False):
        student = Student.objects.get(stu_auth_num=stu_auth_num)
        student.is_active = True
        student.save()
        message = u'启用成功'
        return render(
            request,
            'master/student/viewstuinfo.html',
            { 'message': message, 'admin': isadmin(request.session['username'])}
        )
    else:
        return HttpResponseRedirect('/master')

def forbidallstudent(request):
    if request.session.get('username', False):
        student_list = request.POST.getlist('forbidlist')
        print student_list
        for student in student_list:
            stu = Student.objects.get(stu_auth_num=student)
            stu.is_active = False
            stu.save()
        return render(
            request,
            'master/student/viewstuinfo.html',
            { 'message': u'禁用成功', 'admin': isadmin(request.session['username'])}
        )
    else:
        return HttpResponseRedirect('/master')

def activeallstudent(request):
    if request.session.get('username', False):
        student_list = request.POST.getlist('forbidlist')
        print student_list
        for student in student_list:
            stu = Student.objects.get(stu_auth_num=student)
            stu.is_active = True
            stu.save()
        return render(
            request,
            'master/student/viewstuinfo.html',
            {'message': u'激活成功', 'admin': isadmin(request.session['username'])}
        )
    else:
        return HttpResponseRedirect('/master')
#u'修改学生信息'
class EditStuInfo(View):
    form_class = forms.EditStuInfoForm
    template_name = 'master/student/editstuinfo.html'

    def get(self, request, stu_auth_num):
        if request.session.get('username', False):
            student = Student.objects.get(pk=stu_auth_num)
            form = self.form_class(
                initial={
                    'stu_name': student.stu_name,
                    'stu_class': student.stu_class,
                    'stu_grade': student.stu_grade,
                    'stu_major': student.stu_major,
                    'stu_sex': student.stu_sex,
                    'password': '',
                }
            )
            return render(
                request,
                self.template_name,
                {'form': form, 'student': student, 'admin': isadmin(request.session['username'])}
            )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request, stu_auth_num):
        if request.session.get('username', False):
            form = self.form_class(request.POST)
            if form.is_valid():
                student = Student.objects.get(pk=stu_auth_num)
                student.stu_name = form.cleaned_data['stu_name']
                student.stu_class = form.cleaned_data['stu_class']
                student.stu_grade = form.cleaned_data['stu_grade']
                student.stu_sex = str(form.cleaned_data['stu_sex'])
                student.stu_major = form.cleaned_data['stu_major']
                student.save()
                if form.cleaned_data['password']:
                    student.password = hashlib.md5(form.cleaned_data['password']).hexdigest()
                    student.save()
                else:
                    pass
                message = u'修改成功'
                return render(
                    request,
                    self.template_name,
                    {'message': message, 'student': student, 'admin': isadmin(request.session['username'])},
                )
            else:
                message = u'操作失败'
                form = self.form_class
                return render(
                    request,
                    self.template_name,
                    {'message': message, 'form': form, 'admin': isadmin(request.session['username'])},
                )
        else:
            return HttpResponseRedirect('/master')


#u'添加课程'
def addclass(request):
    if request.session.get('username', False):
        if request.method == 'POST':
            form = forms.AddClassForm(request.POST)
            systime = SysTime.objects.get(pk=1)
            if form.is_valid():
                clas = Classes(
                    class_name=form.cleaned_data['class_name'],
                    class_hours=int(form.cleaned_data['class_hours']),
                    class_for=form.cleaned_data['class_for'],
                    is_allowed_choose=True,
                    comment=form.cleaned_data['comment'],
                    startyear=systime.startyear,
                    endyear=systime.endyear,
                    semester=systime.semester,
                    deadline=form.cleaned_data['deadline']
                )
                clas.save()
                teacher_username_list = request.POST.getlist('teacher_list')
                teacher_list = unicode()
                for teacher_username in teacher_username_list:
                    teacher_list += Administrator.objects.get(username=teacher_username).admin_name + u' '
                    classteachership = ClassTeacherShip(
                        teacher=Administrator.objects.get(username=teacher_username),
                        classes=clas,
                    )
                    classteachership.save()
                clas.teacher_list = teacher_list
                clas.save()
                messages = u'添加成功'
                class_list = Classes.objects.all()
                return render(
                    request,
                    'master/class/addclass.html',
                    {'messages': messages, 'class_list': class_list, 'admin': isadmin(request.session['username'])},
                )
            else:
                return render(
                    request,
                    'master/class/addclass.html',
                    {'form': forms.AddClassForm, 'message': u'您的输入有误', 'admin': isadmin(request.session['username'])}
                )
        else:
            form = forms.AddClassForm
            teacher_list = Administrator.objects.filter(is_active=True)
            return render(
                request,
                'master/class/addclass.html',
                {'form': form, 'teacher_list': teacher_list, 'admin': isadmin(request.session['username'])},
            )
    else:
        return HttpResponseRedirect('/master')


def showclasses(request):
    if request.session.get('username', False):
        teacher = Administrator.objects.get(username=request.session['username'])
        print teacher.admin_name
        print teacher.username
        systime = SysTime.objects.get(pk=1)
        class_all_list = Classes.objects.filter(startyear=systime.startyear).filter(endyear=systime.endyear).filter(semester=systime.semester)
        if teacher.admin_type == 2:
            print 1
            classteachership = ClassTeacherShip.objects.filter(teacher=teacher)
            class_list = list()
            for clas in classteachership:
                if clas.classes in class_all_list:
                    class_list.append(clas.classes)
        else:
            class_list = Classes.objects.filter(startyear=systime.startyear).filter(endyear=systime.endyear).filter(semester=systime.semester)
        form = forms.OtheryearclassForm
        return render(request, 'master/class/showclasses.html', {'form': form, 'class_list': class_list,  'admin': isadmin(request.session['username'])})
    else:
        return HttpResponseRedirect('/master')

def showotherclasses(request):
    if request.session.get('username', False):
        form = forms.OtheryearclassForm(request.POST)
        teacher = Administrator.objects.get(username=request.session['username'])
        if form.is_valid():
            if teacher.admin_type == 1:
                class_list = Classes.objects.filter(startyear=form.cleaned_data['startyear']).filter(endyear=form.cleaned_data['endyear']).filter(semester=form.cleaned_data['semester'])
                form = forms.OtheryearclassForm
                return render(request, 'master/class/showclasses.html', {'form': form, 'class_list': class_list,  'admin': isadmin(request.session['username'])})
            else:
                class_all_list = Classes.objects.filter(startyear=form.cleaned_data['startyear']).filter(endyear=form.cleaned_data['endyear']).filter(semester=form.cleaned_data['semester'])
                classteachership = ClassTeacherShip.objects.filter(teacher=teacher)
                class_list = list()
                for clas in classteachership:
                    if clas.classes in class_all_list:
                        class_list.append(clas.classes)
                return render(request, 'master/class/showclasses.html', {'form': form, 'class_list': class_list,  'admin': isadmin(request.session['username'])})
        else:
            return render(request, 'master/class/showclasses.html', {'form': form,  'admin': isadmin(request.session['username'])})

    else:
            return HttpResponseRedirect('/master')



class EditClass(View):
    form_class = forms.EditClassForm
    template_name = 'master/class/editclass.html'

    def get(self, request, class_id):
        if request.session.get('username', False):
            clas = Classes.objects.get(pk=int(class_id))
            form = self.form_class(
                initial={
                    'class_name': clas.class_name,
                    'class_hours': clas.class_hours,
                    'class_for': clas.class_for,
                    'is_allowed_choose': clas.is_allowed_choose,
                    'comment': clas.comment,
                    'deadline':clas.deadline,
                }
            )
            form2 = forms.AddStudentToClassForm
            try:
                student_list = StuClass.objects.filter(class_id=clas)
            except:
                student_list = None
            teacher_list = Administrator.objects.filter(is_active=True)
            return render(
                request,
                self.template_name,
                {'teacher_list': teacher_list, 'form': form, 'form2':form2, 'clas': clas, 'student_list': student_list, 'admin': isadmin(request.session['username'])}
            )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request, class_id):
        if request.session.get('username', False):
            clas = Classes.objects.get(pk=int(class_id))
            form = self.form_class(request.POST)
            if form.is_valid():
                clas.class_name = form.cleaned_data['class_name']
                clas.class_for = form.cleaned_data['class_for']
                clas.class_hours = int(form.cleaned_data['class_hours'])
                clas.is_allowed_choose = form.cleaned_data['is_allowed_choose']
                clas.comment = form.cleaned_data['comment']
                clas.deadline = form.cleaned_data['deadline']
                clas.save()
                teacher_username_list = request.POST.getlist('teacher_list')
                teacher_list = unicode()
                classteachership_list = ClassTeacherShip.objects.filter(classes=clas)
                for object in classteachership_list:
                    object.delete()
                for teacher_username in teacher_username_list:
                    teacher_list += Administrator.objects.get(username=teacher_username).admin_name + u'   '
                    classteachership = ClassTeacherShip(
                        teacher=Administrator.objects.get(username=teacher_username),
                        classes=clas,
                    )
                    classteachership.save()
                clas.teacher_list = teacher_list
                clas.save()
                message = u'修改成功'
                form = self.form_class(
                    initial={
                        'class_name': clas.class_name,
                        'class_hours': clas.class_hours,
                        'class_for': clas.class_for,
                        'is_allowed_choose': clas.is_allowed_choose,
                        'comment': clas.comment,
                        'deadline': clas.deadline,
                    }
                )
                teacher_list = Administrator.objects.filter(is_active=True)
                return render(
                    request,
                    self.template_name,
                    {'teacher_list': teacher_list, 'form': form, 'message': message, 'clas': clas, 'admin': isadmin(request.session['username'])}
                )
            else:
                message = u'您的输入有误'
                teacher_list = Administrator.objects.filter(is_active=True)
                form = self.form_class(
                    initial={
                        'class_name': clas.class_name,
                        'class_hours': clas.class_hours,
                        'class_for': clas.class_for,
                        'is_allowed_choose': clas.is_allowed_choose,
                        'comment': clas.comment,
                        'deadline': clas.deadline,
                    }
                )
                return render(
                    request,
                    self.template_name,
                    {'teacher_list': teacher_list, 'message': message, 'clas': clas, 'form': form, 'admin': isadmin(request.session['username'])}
                )
        else:
            return HttpResponseRedirect('/master')

#
# class ClassDetailView(ListView):
#     template_name = 'master/class/classdetailview.html'
#
#     def get_queryset(self):
#         self.clas = Classes.objects.get(pk=int(self.args[0]))
#         self.stu_class = StuClass.objects.filter(class_id=self.clas).order_by()
#
class AddStudentToClassView(View):
    form_class = forms.AddStudentToClassForm

    def post(self, request):
        if request.session.get('username', False):
            form = self.form_class(request.POST)
            if form.is_valid():
                stu_auth_num = form.cleaned_data['student']
                student = Student.objects.get(stu_auth_num=stu_auth_num)
                class_id = request.POST['classid']
                class_id = Classes.objects.get(class_id=int(class_id))
                try:
                    stu_clas = StuClass.objects.get(class_id=class_id, stu_id=student)
                    exsit = True
                    success = False
                    message_add_result = u'添加失败,该学生已存在该课程中'
                except:
                    if class_id.class_for == student.stu_grade:
                        stu_clas = StuClass(
                            stu_id=student,
                            class_id=class_id,
                            already_hours=0,
                        )
                        stu_clas.save()
                        class_id.stu_num_now += 1
                        class_id.save()
                        exsit = False
                        success = True
                        message_add_result = u'添加成功'
                    else:
                        exsit = False
                        success = False
                        message_add_result = u'课程面向的年级与学生年级不匹配'
                print success
                clas = Classes.objects.get(pk=int(class_id.class_id))
                form = forms.EditClassForm(
                    initial={
                        'class_name': clas.class_name,
                        'class_hours': clas.class_hours,
                        'class_for': clas.class_for,
                        'is_allowed_choose': clas.is_allowed_choose,
                        'comment': clas.comment,
                    }
                )
                form2 = forms.AddStudentToClassForm
                try:
                    student_list = StuClass.objects.filter(class_id=clas)
                except:
                    student_list = None
                return render(
                    request,
                    'master/class/editclass.html',
                    {'message_add_result': message_add_result, success: 'success', 'exsit': exsit, 'form': form, 'form2': form2, 'clas': clas, 'student_list': student_list, 'admin': isadmin(request.session['username'])}
                )

            else:
                return HttpResponse('/master/editclass/'+request.POST['classid'])


        else:
            return HttpResponseRedirect('/master')


class AddExpRoom(View):
    form_class = forms.AddExpRoomForm
    template_name = 'master/class/addexproom.html'

    def get(self, request):
        if request.session.get('username', False):
            form = self.form_class
            message = False
            exproom_list = False
            return render(
                request,
                self.template_name,
                {'form': form, 'message': message, 'exproom_list': exproom_list, 'admin': isadmin(request.session['username'])}
            )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request):
        if request.session.get('username', False):
            form = self.form_class(request.POST)
            if form.is_valid():
                exproom = ExpRoom(
                    semester_start_year=SysTime.objects.get(pk=1).startyear,
                    semester_end_year=SysTime.objects.get(pk=1).endyear,
                    semester=str(SysTime.objects.get(pk=1).semester),
                    week=int(form.cleaned_data['week']),
                    weekday=form.cleaned_data['weekday'],
                    startclass=int(form.cleaned_data['startclass']),
                    endclass=int(form.cleaned_data['endclass']),
                    roomnum=int(form.cleaned_data['roomnum']),
                    machinenum=int(form.cleaned_data['machinenum']),
                    advise_class=form.cleaned_data['advise_class'],
                    force_major=form.cleaned_data['force_major'],
                    is_full=False,
                    is_allowed_choose=True,
                    stu_num_now=0,
                )
                exproom.save()
                message = u'添加成功'
                print "ok"
                systime = SysTime.objects.get(pk=1)
                exproom_list = ExpRoom.objects.filter(semester=str(systime.semester)).filter(semester_start_year=systime.startyear).order_by("week")
                print "ok"
                return render(
                    request,
                    self.template_name,
                    {'message': message, 'exproom_list': exproom_list, 'admin': isadmin(request.session['username'])}
                )
            else:
                message = u'您的输入有误'
                return render(
                    request,
                    self.template_name,
                    {'message': message, 'admin': isadmin(request.session['username'])}
                )
        else:
            return HttpResponseRedirect('/master')


# class ViewExpRoomList(View):
#     form_class = forms.ViewOtherExpRoomForm
#     template_name = 'master/class/viewexproom.html'
#     systime = SysTime.objects.get(pk=1)
#
#     def exp_today(self):
#         today = date.today()
#         startday = self.systime.startday
#         days = 1 + (datetime.combine(today, datetime.now().time()) - datetime.combine(startday, datetime.now().time())).days
#         nowweek = divmod(days, 7)[0]
#         day = divmod(days,7)[1]
#         if day:
#             nowweek += 1
#         else:
#             day = 7
#         day_dict = {1: u'一', 2: u'二', 3: u'三', 4: u'四', 5: u'五', 6: u'六', 7: u'日'}
#         weekday = day_dict[day]
#         #u"下面try/except获取今天所有的实验时间"
#         try:
#             exproom_today = ExpRoom.objects.filter(
#                 semester_start_year=self.systime.startyear
#             ).filter(
#                 semester_end_year=self.systime.endyear
#             ).filter(
#                 semester=self.systime.semester
#             ).filter(
#                 week=nowweek
#             ).filter(
#                 weekday=weekday
#             )
#         except:
#             exproom_today = list()
#         return (exproom_today, nowweek, weekday)
#
#     def get(self, request):
#         semester_start_year = self.systime.startyear
#         semester = self.systime.semester
#         exproom_list = ExpRoom.objects.filter(semester=semester).filter(semester_start_year=semester_start_year).order_by("week")
#         return render(
#             request,
#             self.template_name,
#             {'exproom_list': exproom_list, 'form': self.form_class}
#         )
#
#     def post(self, request):
#         if request.session.get('username', False):
#             form = self.form_class(request.POST)
#             if form.is_valid():
#                 exproom_list = ExpRoom.objects.filter(
#                     semester=form.cleaned_data['semester']
#                 ).filter(
#                     semester_start_year=form.cleaned_data['semester_start_year']
#                 )
#                 return render(
#                     request,
#                     self.template_name,
#                     {'exproom_list': exproom_list, 'form': self.form_class}
#                 )
#         else:
#             return HttpResponseRedirect('/master')
#

class EditExpRoom(View):
    form_class = forms.EditExpRoomForm
    template_name = 'master/class/editexproom.html'

    def get(self, request, classroomid):
        if request.session.get('username', False):
            exproom = ExpRoom.objects.get(pk=int(classroomid))
            form = self.form_class(
                initial={
                    'week': exproom.week,
                    'weekday': exproom.weekday,
                    'startclass': exproom.startclass,
                    'endclass': exproom.endclass,
                    'roomnum': exproom.roomnum,
                    'machinenum': exproom.machinenum,
                    'advise_class': exproom.advise_class,
                    'force_major': exproom.force_major,
                    'is_allowed_choose': exproom.is_allowed_choose,
                }
            )
            message = False
            return render(
                request,
                self.template_name,
                {'form': form, 'message': message, 'exproom': exproom, 'admin': isadmin(request.session['username'])}
            )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request, classroomid):
        if request.session.get('username', False):
            exproom = ExpRoom.objects.get(pk=int(classroomid))
            form = self.form_class(request.POST)
            if form.is_valid():
                if (int(form.cleaned_data['machinenum']) < exproom.stu_num_now):
                    form = self.form_class(
                        initial={
                            'week': exproom.week,
                            'weekday': exproom.weekday,
                            'startclass': exproom.startclass,
                            'endclass': exproom.endclass,
                            'roomnum': exproom.roomnum,
                            'machinenum': exproom.machinenum,
                            'is_allowed_choose': exproom.is_allowed_choose,
                            'advise_class': exproom.advise_class,
                            'force_major': exproom.force_major,
                        }
                    )
                    return render(
                        request,
                        self.template_name,
                        {'form': form, 'message': u'机位数量不得小于已选人数', 'exproom': exproom, 'admin': isadmin(request.session['username'])}
                    )
                else:
                    exproom.week = int(form.cleaned_data['week'])
                    exproom.weekday = form.cleaned_data['weekday']
                    exproom.startclass = int(form.cleaned_data['startclass'])
                    exproom.endclass = int(form.cleaned_data['endclass'])
                    exproom.roomnum = int(form.cleaned_data['roomnum'])
                    exproom.machinenum = int(form.cleaned_data['machinenum'])
                    exproom.advise_class = form.cleaned_data['advise_class']
                    exproom.force_major = form.cleaned_data['force_major']
                    exproom.is_allowed_choose = bool(form.cleaned_data['is_allowed_choose'])
                    exproom.save()
                    message = u'修改成功'
                    form = self.form_class(
                        initial={
                            'week': exproom.week,
                            'weekday': exproom.weekday,
                            'startclass': exproom.startclass,
                            'endclass': exproom.endclass,
                            'roomnum': exproom.roomnum,
                            'machinenum': exproom.machinenum,
                            'advise_class': exproom.advise_class,
                            'force_major': exproom.force_major,
                            'is_allowed_choose': exproom.is_allowed_choose,
                        }
                    )
                    return render(
                        request,
                        self.template_name,
                        {'message': message, 'exproom': exproom, 'form': form, 'admin': isadmin(request.session['username'])}
                    )
            else:
                return self.get(request, classroomid)
        else:
            return HttpResponseRedirect('/master')


class AddStudentToExpRoomView(View):
    template_name = 'master/studoexp/studoexpcomment.html'
    form_class = forms.AddStudentToClassForm

    def post(self, request):
        if request.session.get('username', False):
            form = self.form_class(request.POST)
            exproom = ExpRoom.objects.get(pk=int(request.POST['exproomid']))
            if form.is_valid():
                student = Student.objects.get(pk=form.cleaned_data['student'])
                try:
                    stu_sel_time = StuSelExpTime.objects.get(stu_id=student, exproom_id=exproom)
                    existmessage = u'该学生已经选择了此时间'
                except:
                    stu_sel_time = StuSelExpTime(
                        stu_id=student,
                        exproom_id=exproom,
                        hours=0,
                        seat_num=exproom.stu_num_now+1,
                    )
                    stu_sel_time.save()
                    existmessage = u'添加成功'
            else:
                existmessage = u'添加失败'
            context = dict()
            context['existmessage'] = existmessage
            stu_already_start = list()
            for sel in StuSelExpTime.objects.filter(exproom_id=exproom).filter(is_start=True):
                student = sel.stu_id
                stu_already_start.append(StuDoExp.objects.get(stu_id=student, stuseltime_id=sel))
            context['stu_not_start'] = StuSelExpTime.objects.filter(exproom_id=exproom).filter(is_start=False)
            context['stu_already_start'] = stu_already_start
            context['exproom'] = exproom
            context['form1'] = forms.AddStudentToClassForm
            context['admin'] = isadmin(request.session['username'])
            return render(
                request,
                self.template_name,
                context
            )


class StuDoExpView(ListView):
    template_name = 'master/studoexp/studoexpview.html'
    context_object_name = 'exproom_this_year'
    try:
        systime = SysTime.objects.get(pk=1)
    except:
        systime = SysTime(
            startyar=date.today().year,
            endyear=date.today().year,
            semester=1,
        )
    queryset = ExpRoom.objects.filter(semester_start_year=systime.startyear).filter(semester_end_year=systime.endyear).filter(semester=systime.semester).order_by("-week")

    def exp_today(self):
        today = date.today()
        startday = self.systime.startday
        days = 1 + (datetime.combine(today, datetime.now().time()) - datetime.combine(startday, datetime.now().time())).days
        nowweek = divmod(days, 7)[0]
        day = divmod(days, 7)[1]
        if day:
            nowweek += 1
        else:
            day = 7
        day_dict = {1: u'一', 2: u'二', 3: u'三', 4: u'四', 5: u'五', 6: u'六', 7: u'日'}
        weekday = day_dict[day]
        #u"下面try/except获取今天所有的实验时间"
        try:
            exproom_today = ExpRoom.objects.filter(
                semester_start_year=self.systime.startyear
            ).filter(
                semester_end_year=self.systime.endyear
            ).filter(
                semester=self.systime.semester
            ).filter(
                week=nowweek
            ).filter(
                weekday=weekday
            )
        except:
            exproom_today = list()
        return (exproom_today, nowweek, weekday)

    def get_context_data(self, **kwargs):
        context = super(StuDoExpView, self).get_context_data(**kwargs)
        exproom_all = ExpRoom.objects.all()
        exproom_ever = list()
        for exproom in exproom_all:
            if exproom not in self.queryset:
                exproom_ever.append(exproom)
        context['exproom_ever'] = exproom_ever
        exp_today = self.exp_today()
        context['exproom_today'] = exp_today[0]
        context['today'] = date.today()
        context['nowweek'] = exp_today[1]
        context['day'] = exp_today[2]
        context['form'] =forms.ViewOtherExpRoomForm
        context['admin'] = isadmin(self.request.session['username'])
        return context

def showotherexproom(request):
    if request.session.get('username', False):
        form = forms.ViewOtherExpRoomForm(request.POST)
        if form.is_valid():
            startyear = int(form.cleaned_data['semester_start_year'])
            print startyear
            endyear = int(form.cleaned_data['semester_end_year'])
            print endyear
            semester = int(form.cleaned_data['semester'])
            print semester
            exproom_list = ExpRoom.objects.filter(semester_start_year=startyear).filter(semester_end_year=endyear).filter(semester=semester).order_by("-add_date")
            form = forms.ViewOtherExpRoomForm
            return render(
                request,
                'master/studoexp/studoexpview.html',
                {'form': form, 'exproom_list': exproom_list,  'admin': isadmin(request.session['username'])}
            )
        else:
            return render(request, 'master/studoexp/studoexpview.html', {'form': form,  'admin': isadmin(request.session['username'])})
    else:
            return HttpResponseRedirect('/master')



class StuDoExpComment(ListView):
    template_name = 'master/studoexp/studoexpcomment.html'
    context_object_name = 'stu_not_start'

    def get_queryset(self):
        self.exproom = ExpRoom.objects.get(classroomid=int(self.args[0]))
        return StuSelExpTime.objects.filter(exproom_id=self.exproom).filter(is_start=False)

    def get_context_data(self, **kwargs):
        context = super(StuDoExpComment, self).get_context_data(**kwargs)
        self.exproom = ExpRoom.objects.get(classroomid=int(self.args[0]))
        teacher = Administrator.objects.get(username=self.request.session['username'])
        teacher_class_list = ClassTeacherShip.objects.filter(teacher=teacher)
        class_list = list()
        stu_mine = list()
        stu_others = list()
        stu_not_start = list()
        for ship in teacher_class_list:
            class_list.append(ship.classes)
        #u'上面两行获得教师所任的课程列表'
        for sel in StuSelExpTime.objects.filter(exproom_id=self.exproom).filter(is_start=True):
            #u'对本次实验所有选择的学生生成的条目进行遍历'
            student = sel.stu_id
            try:
                a = StuDoExp.objects.get(stuseltime_id=sel).stu_class.class_id
                if a in class_list:
                    stu_mine.append(StuDoExp.objects.get(stu_id=student, stuseltime_id=sel))
                    #u'如何学生当前进行实验的课程在教师的课程列表中，把学生当前的实验记录加入stu_mine'
                else:
                    stu_others.append(StuDoExp.objects.get(stu_id=student, stuseltime_id=sel))
                #u'a为当前选择记录进行实验时所选的课程object'
            except:
                stu_not_start.append(sel)
                #u'否则，把该实验记录加入到stu_others'
        context['stu_mine'] = stu_mine
        context['stu_others'] = stu_others
        context['stu_not_start'] = stu_not_start
        context['exproom'] = self.exproom
        context['form1'] = forms.AddStudentToClassForm
        context['admin'] = isadmin(self.request.session['username'])
        return context


class CommitExpView(View):

    def post(self, request, stu_auth_num, sel_time_id):
        if request.session.get('username', False):
            stu_exp = StuDoExp.objects.get(stu_id=Student.objects.get(stu_auth_num=stu_auth_num), stuseltime_id=StuSelExpTime.objects.get(exproom_id=ExpRoom.objects.get(classroomid=sel_time_id)))
            stu_exp.exp_grade = request.POST['exp_grades']
            stu_exp.save()
            return HttpResponseRedirect('/master/commitstudentclass/' + str(stu_exp.stu_class.class_id.class_id)+'/'+str(stu_auth_num))
        else:
            return  HttpResponseRedirect('/master')

    def get(self, request, stu_auth_num, sel_time_id):
        if request.session.get('username', False):
            stu_exp = StuDoExp.objects.get(stu_id=Student.objects.get(stu_auth_num=stu_auth_num), stuseltime_id=StuSelExpTime.objects.get(exproom_id=ExpRoom.objects.get(classroomid=sel_time_id)))
            stu_exp.comment = request.GET['exp_comment']
            stu_exp.exp_grade = request.GET['exp_grades']
            stu_exp.save()
            return HttpResponseRedirect('/master/studoexpcomment/' + str(stu_exp.stuseltime_id.exproom_id.classroomid))
        else:
            return  HttpResponseRedirect('/master')

class AddNewsView(View):
    form_class = forms.AddNewsForm
    template_name = 'master/news/addnews.html'

    def get(self, request):
        if request.session.get('username', False):
            try:
                category_ = Category.objects.get(name=u'未分类')
            except:
                category_ = Category(
                    name=u'未分类',
                )
                category_.save()
            form = self.form_class
            return render(
                request,
                self.template_name,
                {'form': form, 'admin': isadmin(request.session['username'])}
            )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request):
        if request.session.get('username', False):
            author = Administrator.objects.get(username=request.session['username'])
            form = self.form_class(request.POST, request.FILES)
            print author.admin_type
            if form.is_valid():
                news = News(
                    title=form.cleaned_data['title'],
                    contents=form.cleaned_data['contents'],
                    attachment=form.cleaned_data['attachment'],
                    author=author,
                    category=Category.objects.get(id=int(form.cleaned_data['category'])),
                    create_date=datetime.now(),
                )
                news.save()
                return render(
                    request,
                    self.template_name,
                    {'news': news, 'message': u'添加成功', 'admin': isadmin(request.session['username'])}
                )
            else:
                return render(
                    request,
                    self.template_name,
                    {'message': u'您的输入有误', 'form': forms.AddNewsForm, 'admin': isadmin(request.session['username'])}
                )
class NewsListView(ListView):
    context_object_name = 'news_list'
    queryset = News.objects.all().order_by('-create_date')
    template_name = 'master/news/viewnews.html'

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['admin'] = isadmin(self.request.session['username'])
        teacher = Administrator.objects.get(username=self.request.session['username'])
        try:
            my_news = News.objects.filter(author=teacher)
        except:
            my_news = list()
        context['my_news'] = my_news
        return context

def deletenews(request, newsid):
    if request.session.get('username', False):
        news = News.objects.get(pk=int(newsid))
        news.delete()
        news_list = News.objects.all().order_by('-create_date')
        return render(
            request,
            'master/news/viewnews.html',
            {'news_list': news_list, 'admin': isadmin(request.session['username'])}
        )

class NewsDetail(ListView):
    template_name = 'master/news/newsdetail.html'
    queryset = News.objects.all()

    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        context['admin'] =  isadmin(self.request.session['username'])
        context['news'] = News.objects.get(pk=int(self.args[0]))
        return context


class CategoryNewsView(ListView):
    context_object_name = 'news_list'
    template_name = 'master/news/viewnews.html'

    def get_queryset(self):
        return News.objects.filter(category=Category.objects.get(id=int(self.args[0])))

    def get_context_data(self, **kwargs):
        context = super(CategoryNewsView, self).get_context_data(**kwargs)
        context['admin'] = isadmin(self.request.session['username'])
        return context

def addcategory(request):
    if request.session.get('username', False):
        if request.method == 'POST':
            form = forms.AddCategoryForm(request.POST)
            if form.is_valid():
                category = Category(
                    name=form.cleaned_data['category']
                )
                category.save()
                message = u'添加成功'
            category_list = Category.objects.all()
            return render(
                request,
                'master/news/addcategotry.html',
                {'form': form, 'category_list': category_list, 'admin': isadmin(request.session['username'])}
            )
        elif request.method == 'GET':
            print 1
            form = forms.AddCategoryForm
            category_list = Category.objects.all()
            return render(
                request,
                'master/news/addcategotry.html',
                {'form':form, 'category_list': category_list, 'admin': isadmin(request.session['username'])}
            )
        else:
            pass

    else:
        return HttpResponseRedirect('/master')


class EditCategoryView(View):
    template_name = 'master/news/editcategory.html'
    form_class = forms.AddCategoryForm

    def get(self, request, id):
        if request.session.get('username', False):
            category = Category.objects.get(id=int(id))
            form = self.form_class(
                initial={
                    'name':category.name,
                }
            )
            category_list = Category.objects.all()
            return render(
                request,
                self.template_name,
                {'category': category, 'category_list': category_list,'form': form, 'admin': isadmin(self.request.session['username'])}
            )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request, id):
        if request.session.get('username', False):
            form = self.form_class(request.POST)
            if form.is_valid():
                category = Category.objects.get(id=int(id))
                category.name = form.cleaned_data['name']
                category.save()
                form = self.form_class(
                    initial={
                        'name':category.name,
                    }
                )
                category_list = Category.objects.all()
                return render(
                    request,
                    self.template_name,
                    {'category': category, 'category_list': category_list,'message': u'修改成功', 'form': form, 'admin': isadmin(self.request.session['username'])}
                )
        else:
            return HttpResponseRedirect('/master')

# def deletecategory(request, categoryid):
#     if request.session.get('username', False):
#         template_name = 'master/news/categorylist.html'
#         try:
#             category = Category.objects.get(pk=int(categoryid))
#             category_news = News.objects.filter(category=category)
#             for news in category_news:
#                 news.category = Category.objects.get(name=u'未分类')
#             category.delete()
#             context = dict()
#             context['category_list'] = Category.objects.all()
#             context['message'] = u'删除成功'
#             return render(
#                 request,
#                 template_name,
#                 context
#             )
#         except:
#             return HttpResponse('something is wrong')


class EditNews(View):

    def get(self, request, newsid):
        news = News.objects.get(pk=int(newsid))
        form = forms.AddNewsForm(
            initial={
                'title':news.title,
                'category':news.category.name,
                'contents':news.contents,
            }
        )
        return render(
            request,
            'master/news/editnews.html',
            {'form': form, 'news': news, 'admin': isadmin(self.request.session['username'])}
        )

    def post(self, request, newsid):
        news = News.objects.get(pk=int(newsid))
        form = forms.AddNewsForm(request.POST, request.FILES)
        if form.is_valid():
            news.title = form.cleaned_data['title']
            news.category = Category.objects.get(pk=int(form.cleaned_data['category']))
            news.contents = form.cleaned_data['contents']
            news.attachment = form.cleaned_data['attachment']
            news.save()
            message = u'修改成功'
        form = forms.AddNewsForm(
            initial={
                'title':news.title,
                'category':news.category.name,
                'contents':news.contents,
            }
        )
        return render(
            request,
            'master/news/newsdetail.html',
            {'form': form, 'message': message, 'news': news, 'admin': isadmin(self.request.session['username'])}
        )

class CommitStudentClass(View):
    template_name = 'master/class/commitclass.html'

    def get(self, request, classid, stu_auth_num):
        if request.session.get('username', False):
            classid = Classes.objects.get(class_id=int(classid))
            student = Student.objects.get(stu_auth_num=stu_auth_num)
            stu_class = StuClass.objects.get(class_id=classid, stu_id=student)
            stu_exp_list = StuDoExp.objects.filter(stu_class=stu_class)
            form = forms.CommitClassForm(
                initial={
                    'class_grades':stu_class.class_grades,
                    'teacher_commit':stu_class.teacher_commit,
                }
            )
            form1 = forms.ClassReportForm
            context = {'form': form, 'form1': form1, 'classid':classid, 'student':student, 'stu_class': stu_class, 'stu_exp_list': stu_exp_list}
            return render(
                request,
                self.template_name,
                context
            )
        else:
            return HttpResponseRedirect('/master')

    def post(self, request, classid, stu_auth_num):
        if request.session.get('username', False):
            classid = Classes.objects.get(class_id=int(classid))
            student = Student.objects.get(stu_auth_num=stu_auth_num)
            stu_class = StuClass.objects.get(class_id=classid, stu_id=student)
            stu_exp_list = StuDoExp.objects.filter(stu_class=stu_class)
            form = forms.CommitClassForm(request.POST)
            if form.is_valid():
                stu_class.teacher_commit = form.cleaned_data['teacher_commit']
                stu_class.class_grades = form.cleaned_data['class_grades']
                stu_class.save()
                message = u'保存成功'
            form = forms.CommitClassForm(
                initial={
                    'class_grades':stu_class.class_grades,
                    'teacher_commit':stu_class.teacher_commit,
                }
            )
            form1 = forms.ClassReportForm
            context = {'form1': form1, 'message':message, 'form': form, 'classid':classid, 'student':student, 'stu_class': stu_class, 'stu_exp_list': stu_exp_list}
            return render(
                request,
                self.template_name,
                context
            )
        else:
            return HttpResponseRedirect('/master')


def StuclassreportUpload(request, classid, stu_auth_num):
    if request.session.get('username', False):
        class_id = Classes.objects.get(class_id=int(classid))
        student = Student.objects.get(pk=stu_auth_num)
        form = forms.ClassReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.cleaned_data['class_report']
            if report.content_type not in settings.REPORT_CONTENT_TYPE:
                error_message = u'只允许上传pdf文件'
            try:
                stu_class = StuClass.objects.get(stu_id=student, class_id=class_id)
                stu_class.class_report = report
                stu_class.report_date = date.today()
                stu_class.class_is_finished = True
                stu_class.save()
                message = u'上传成功'
                form1 = forms.ClassReportForm
                stu_class = StuClass.objects.get(class_id=classid, stu_id=student)
                try:
                    stu_exp_list = StuDoExp.objects.filter(stu_class=stu_class)
                except:
                    stu_exp_list = None
                context = {'message': message, 'form1': form1, 'classid':class_id, 'student':student, 'stu_class': stu_class, 'stu_exp_list': stu_exp_list}
                return render(
                    request,
                    'master/class/commitclass.html',
                    context
                )
            except:
                return HttpResponseRedirect('/master/commitstudentclass/'+str(classid)+str(stu_auth_num))
        else:
            return HttpResponseRedirect('/master/commitstudentclass/'+str(classid)+str(stu_auth_num))
    return  HttpResponseRedirect('/master')