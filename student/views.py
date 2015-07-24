# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
import hashlib
from models import Student, StuClass
from news.models import News
import forms
from master.models import SysTime
from classes.models import Classes, ExpRoom
from student.models import StuSelExpTime, StuDoExp
from datetime import date, datetime
from django.utils import timezone
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views.static import serve
import os

#u'学生首页'
def index(request):
    if request.session.get('stu_auth_num', False):
        student = Student.objects.get(stu_auth_num=int(request.session['stu_auth_num']))
        news_list = News.objects.all().order_by('create_date')
        form = forms.StudentLogForm
        return render(
            request,
            'student/index.html',
            {'form': form,'student': student, 'news_list': news_list}
        )
    else:
        form = forms.StudentLogForm
        news_list = News.objects.all().order_by('create_date')
        context = {'news_list': news_list, 'form': form}
        return render(request, 'student/index.html', context)


def index2(request):
    form = forms.StudentLogForm
    message = u'登录超时，请重新登录'
    return render(
        request,
        'student/index2.html',
        {'form': form, 'message': message}
    )


#u'学生登录验证'
def stulogin(request):
    if request.method == 'POST':
        form = forms.StudentLogForm(request.POST)
        if form.is_valid():
            stu_id = form.cleaned_data['stu_id']
            student = Student.objects.get(pk=stu_id)
            stu_pass_hash = hashlib.md5(form.cleaned_data['password']).hexdigest()
            if stu_pass_hash == student.password and student.is_active:
                request.session['stu_auth_num'] = student.stu_auth_num
                return render(
                    request,
                    'student/work/index.html',
                    {'student': student, 'news_list': News.objects.all().order_by("-create_date")}
                )
            else:
                form = forms.StudentLogForm
                message = u'您的帐号已经被禁用！'
                return render(
                    request,
                    'student/index2.html',
                    {'form': form, 'message': message}
                )

        else:
            return HttpResponse(u'您的输入有误')
    else:
        return HttpResponseRedirect("/")


#u'登出'
def stulogout(request):
    try:
        del request.session['stu_auth_num']
        request.session.flush()
        return index(request)
    except:
        return index(request)


# u'修该密码'
def changepass(request):
    if request.session.get('stu_auth_num', False):
        student = Student.objects.get(stu_name=request.session['stu_auth_num'])
        form = forms.ChangePassForm(request.POST)
        changeform = forms.ChangePassForm
        if form.is_valid():
            newpass1 = form.cleaned_data['newpass1']
            newpass2 = form.cleaned_data['newpass2']
            if newpass1 == newpass2:
                newpass = hashlib.md5(newpass1).hexdigest()
                student.password = newpass
                student.save()
                context = {'successmessage': u'修改成功'}
                del request.session['student']
                request.session.flush()
                return render(request, 'student/success.html', context)
            else:
                failmessage = u'两次密码不一致'
                context = {'failmessage': failmessage, 'form': changeform}
                return render(request, 'student/change.html', context)
        else:
            failmessage = ''
            context = {'failmessage': failmessage, 'form': changeform}
            return render(request, 'student/change.html', context)
    else:
        return HttpResponseRedirect('/student/index2')


def work(request):
    if request.session.get('stu_auth_num', False):
        student = Student.objects.get(stu_auth_num=int(request.session['stu_auth_num']))
        return render(
            request,
            'student/work/index.html',
            {'student': student}
        )
    else:
        return HttpResponseRedirect('/student/index2')


class Myinfo(View):
    form_class = forms.MyInfoForm
    template_name = 'student/work/info/myinfo.html'

    def get(self, request):
        if request.session.get('stu_auth_num', False):
            student = Student.objects.get(pk=request.session['stu_auth_num'])
            form = self.form_class(
                initial={
                    'stu_name': student.stu_name,
                    'stu_class': student.stu_class,
                    'stu_grade': student.stu_grade,
                    'stu_major': student.stu_major,
                    'stu_sex': student.stu_sex,
                    'stu_phone': student.stu_phone,
                    'password1': '',
                    'password2': '',
                    'password': '',
                }
            )
            return render(
                request,
                self.template_name,
                {'form': form, 'student': student}
            )
        else:
            return HttpResponseRedirect('/student/index2')

    def post(self, request):
        if request.session.get('stu_auth_num', False):
            form = self.form_class(request.POST)
            if form.is_valid():
                student = Student.objects.get(pk=request.session['stu_auth_num'])
                student.stu_name = form.cleaned_data['stu_name']
                student.stu_class = form.cleaned_data['stu_class']
                student.stu_grade = form.cleaned_data['stu_grade']
                student.stu_sex = str(form.cleaned_data['stu_sex'])
                student.stu_major = form.cleaned_data['stu_major']
                student.stu_phone = form.cleaned_data['stu_phone']
                student.save()
                if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                    if student.password == hashlib.md5(form.cleaned_data['password1']).hexdigest():
                        student.password = hashlib.md5(form.cleaned_data['password1']).hexdigest()
                        student.save()
                else:
                    pass
                message = u'修改成功'
                return render(
                    request,
                    self.template_name,
                    {'message': message},
                )
            else:
                message = u'操作失败'
                form = self.form_class
                return render(
                    request,
                    self.template_name,
                    {'message': message, 'form': form},
                )
        else:
            return HttpResponseRedirect('/student/index2')


class StuViewMyClasses(ListView):
    template_name = 'student/work/class/stuviewclass.html'
    context_object_name = 'stu_class_list'
    try:
        systime = SysTime.objects.get(pk=1)
    except:
        systime = SysTime(
            startyear=date.today().year - 1,
            endyear=date.today().year,
            semester=1,
            startday=date.today(),
        )
        systime.save()
    termlist = (systime.startyear, systime.endyear, systime.semester)
    class_this_year = Classes.objects.filter(startyear=termlist[0]).filter(endyear=termlist[1]).filter(semester=termlist[2])
    queryset = SysTime.objects.get(pk=1)

    def get_context_data(self, **kwargs):
        self.student = Student.objects.get(pk=self.request.session['stu_auth_num'])
        context = super(StuViewMyClasses, self).get_context_data(**kwargs)
        self.stu_class = StuClass.objects.filter(stu_id=self.student)
        self.class_this_term = list()
        self.class_ever = list()
        for obj in self.stu_class:
            if obj.class_id in self.class_this_year:
                self.class_this_term.append(obj)
            else:
                self.class_ever.append(obj)
        context['class_this_term'] = self.class_this_term
        context['class_ever'] = self.class_ever
        context['systime'] = self.systime
        return  context


class StuClassDetailView(ListView):
    template_name = 'student/work/class/stuclassdetail.html'
    context_object_name = 'systime'

    def get_queryset(self):
        return SysTime.objects.get(pk=1)

    def get_context_data(self, **kwargs):
        context = super(StuClassDetailView, self).get_context_data(**kwargs)
        self.student = Student.objects.get(pk=int(self.request.session['stu_auth_num']))
        self.stu_class = StuClass.objects.get(class_id=self.args[0], stu_id=Student.objects.get(stu_auth_num=int(self.request.session['stu_auth_num'])))
        context['stu_class'] = self.stu_class
        try:
            stu_do_exp = StuDoExp.objects.filter(stu_class=self.stu_class).filter(stu_id=self.student)
        except:
            stu_do_exp = None
        context['stu_do_exp_list'] = stu_do_exp
        context['form'] = forms.ClassReportForm
        return context

class StuClassReportUpload(View):
    form = forms.ClassReportForm
    template_name = 'student/work/class/stuclassdetail.html'

    def post(self, request, classid):
        if request.session.get('stu_auth_num', False):
            class_id = Classes.objects.get(class_id=int(classid))
            student = Student.objects.get(pk=request.session['stu_auth_num'])
            form = forms.ClassReportForm(request.POST, request.FILES)
            if form.is_valid():
                print request.session['stu_auth_num']
                report = form.cleaned_data['class_report']
                if report.content_type not in settings.REPORT_CONTENT_TYPE:
                    error_message = u'只允许上传pdf文件'
                try:
                    stu_class = StuClass.objects.get(stu_id=student, class_id=class_id)
                    if (stu_class.deadline - date.today()).days >= 0:
                        stu_class.class_report = report
                        stu_class.report_date = date.today()
                        stu_class.class_is_finished = True
                        stu_class.save()
                        message = u'上传成功'
                    else:
                        message = u'已经超过截至日期，您不能上传实验报告。'
                except:
                    stu_class = None
                    message = u'something is wrong.'
                try:
                    stu_do_exp_list = StuDoExp.objects.filter(stu_class=stu_class).filter(stu_id=student)
                except:
                    stu_do_exp_list = None
                systime = SysTime.objects.get(pk=1)
                form = forms.ClassReportForm
                print stu_class
                return render(
                    request,
                    self.template_name,
                    {'form': form, 'message': message, 'stu_class': stu_class, 'stu_do_exp_list': stu_do_exp_list, 'systime': systime}
                )
        else:
            return HttpResponse("/index2/")

#u'学生选课或者退选课程'
class StuEditClass(View):
    template_name = 'student/work/class/chooseclass.html'

    def get(self, request, action, class_id):
        if request.session.get('stu_auth_num', False):
            systime = SysTime.objects.get(pk=1)
            allow_class = systime.allow_class
            student = Student.objects.get(stu_auth_num=request.session['stu_auth_num'])
            try:
                clas = Classes.objects.get(class_id=int(class_id))
                clas_this_year = (systime.startyear == clas.startyear) and (systime.endyear == clas.endyear) and (systime.semester == clas.semester)
                clas_allowed_edit = clas_this_year and (clas.class_for == student.stu_grade)
            except:
                clas = None
                clas_this_year = False
                clas_allowed_edit = False
            if allow_class:
                if action == 'join':
                    if clas_allowed_edit and clas.is_allowed_choose:
                        try:
                            stu_classes = StuClass.objects.filter(stu_id=student).get(class_id=clas)
                            if stu_classes:
                                message = u''
                        except:
                            stu_clas = StuClass(
                                stu_id=student,
                                class_id=clas,
                                already_hours=0,
                                class_grades=-1,
                            )
                            stu_clas.save()
                            clas.stu_num_now += 1
                            clas.save()
                            message = u'选择成功'
                    else:
                        message = u''
                elif action == 'quit':
                    stu_clas = StuClass.objects.get(class_id=int(class_id), stu_id=student)
                    try:
                        studoexp = StuDoExp.objects.get(stu_id=student, stu_class=stu_clas)
                    except:
                        studoexp = None
                    if (not studoexp) and clas_allowed_edit and clas.is_allowed_choose and (stu_clas.already_hours !=0):
                        stu_clas.delete()
                        clas.stu_num_now -= 1
                        clas.save()
                        message = u'退选成功'
                    else:
                        message = u'操作失败，您可能已经进行了该课程的实验。'
                else:
                    message = u''
            else:
                message = u'当前时间不允许选课！'
            class_all = Classes.objects.filter(class_for=student.stu_grade).filter(startyear=systime.startyear).filter(endyear=systime.endyear).filter(semester=systime.semester)
            class_not_choose = list()
            class_all = list(class_all)
            try:
                class_choose_stuclass_objects = StuClass.objects.filter(stu_id=student)
                class_choose = list()
                for stu_class in class_choose_stuclass_objects:
                    class_choose.append(stu_class.class_id)
                for class_id in class_all:
                    if class_id not in class_choose:
                        class_not_choose.append(class_id)
                return render(
                    request,
                    self.template_name,
                    {'message': message, 'allow_choose': allow_class, 'class_not_choose': class_not_choose, 'class_choose': class_choose}
                )
            except:
                class_choose = None
                class_not_choose = list(class_all)
                return render(
                    request,
                    self.template_name,
                    {'message': message, 'allow_choose': allow_class, 'class_not_choose': class_not_choose, 'class_choose': class_choose}
                )
        else:
            return HttpResponseRedirect('/student/index2')

def if_exp_outdate(exproom):
    today = date.today()
    systime = SysTime.objects.get(pk=1)
    startday = systime.startday
    days = 1 + (datetime.combine(today, datetime.now().time()) - datetime.combine(startday, datetime.now().time())).days
    nowweek = divmod(days, 7)[0]
    day = divmod(days,7)[1]
    if day:
        nowweek += 1
    else:
        day = 7
    day_dict = {1: u'一', 2: u'二', 3: u'三', 4: u'四', 5: u'五', 6: u'六', 7: u'日'}
    weekday = day_dict[day]
    #u"下面try/except获取今天所有的实验时间"
    if exproom.week < nowweek:
        return True
    elif exproom.week == nowweek:
        expweekday = 0
        for keys,values in day_dict:
            if values == exproom.weekday:
                expweekday = keys
        if day >= expweekday:
            return False
        else:
            return True
    else:
        return False


#u'学生选实验时间与退选'
class EditExpRoom(View):
    template_name = 'student/work/exproom/editexproom.html'

    def get(self, request):
        if request.session.get('stu_auth_num', False):
            student = Student.objects.get(stu_auth_num=request.session['stu_auth_num'])
            systime = SysTime.objects.get(pk=1)
            allow_choose = systime.allow_exproom
            if allow_choose:
                try:
                    exproom_all = ExpRoom.objects.filter(semester_start_year=systime.startyear).filter(semester=systime.semester).order_by("week")
                    exproom_all = list(exproom_all)
                    exproom_choose = list()
                    exproom_not_choose = list()
                    try:
                        stu_sel_time_objects = StuSelExpTime.objects.filter(
                            stu_id=Student.objects.get(
                                stu_auth_num=student.stu_auth_num
                            )
                        )
                        for obj in stu_sel_time_objects:
                            exproom_choose.append(obj.exproom_id)
                        for exproom in exproom_all:
                            if  (exproom not in exproom_choose) and (exproom.force_major == u'不限' or exproom.force_major == student.stu_major):
                                exproom_not_choose.append(exproom)
                        if not exproom_not_choose:
                            message_wuxuan = u'当前无可选时间'
                        else:
                            message_wuxuan = ''
                        return render(
                            request,
                            self.template_name,
                            {'message_wuxuan': message_wuxuan, 'allow_choose': allow_choose, 'exproom_choose': exproom_choose, 'exproom_not_choose': exproom_not_choose}
                        )
                    except:
                        return render(
                            request,
                            self.template_name,
                            {
                                'allow_choose': allow_choose,
                                'message_weixuan': u'您还未选择任何时间',
                                'exproom_choose': None,
                                'exproom_not_choose': exproom_all
                            }
                        )
                except:
                    message_wuxuan = u'当前无可选时间'
                    return render(
                        request,
                        self.template_name,
                        {'allow_choose': allow_choose, 'message_wuxuan': message_wuxuan, 'exproom_choose': None, 'exproom_not_choose': None}
                    )
            else:
                exproom_choose = list()
                try:
                    stu_sel_time_objects = StuSelExpTime.objects.filter(
                        stu_id=Student.objects.get(
                            stu_auth_num=student.stu_auth_num
                        )
                    )
                    for obj in stu_sel_time_objects:
                        exproom_choose.append(obj.exproom_id)
                except:
                    exproom_choose = None
                return render(
                    request,
                    self.template_name,
                    {'message_not_allow': u'当前不允许选时间', 'exproom_choose': exproom_choose}
                )
        else:
            return HttpResponseRedirect('/student/index2')

    def post(self, request):
        if request.session.get('stu_auth_num', False):
            print 1
            student = Student.objects.get(stu_auth_num=request.session['stu_auth_num'])
            systime = SysTime.objects.get(pk=1)
            allow_choose = systime.allow_exproom
            if allow_choose:
                exproom_all = ExpRoom.objects.filter(semester_start_year=systime.startyear).filter(semester=systime.semester).order_by("week")
                exproom_all = list(exproom_all)
                exproom_choose = list()
                exproom_not_choose = list()
                try:
                    stu_sel_time_objects = StuSelExpTime.objects.filter(
                        stu_id=Student.objects.get(
                            stu_auth_num=student.stu_auth_num
                        )
                    )
                    for obj in stu_sel_time_objects:
                        exproom_choose.append(obj.exproom_id)
                    for exproom in exproom_all:
                        if exproom not in exproom_choose and (exproom.force_major == u'不限' or exproom.force_major == student.stu_major):
                            exproom_not_choose.append(exproom)
                except:
                    for exproom in exproom_all:
                        if exproom.force_major == u'不限' or exproom.force_major == student.stu_major:
                            exproom_not_choose.append(exproom)
                if request.POST['action'] == 'join':
                    join_exproom_list = request.POST.getlist('join_list')
                    for join_exproom_id in join_exproom_list:
                        exproom = ExpRoom.objects.get(classroomid=int(join_exproom_id))
                        if exproom in exproom_not_choose and (exproom.stu_num_now < exproom.machinenum):
                            stu_sel_time = StuSelExpTime(
                                exproom_id=exproom,
                                stu_id=student,
                                hours=exproom.endclass - exproom.startclass,
                                time_week=exproom.week,
                                seat_num=exproom.stu_num_now+1,
                            )
                            stu_sel_time.save()
                            try:
                                stu_do_exp = StuDoExp.objects.get(stuseltime_id=stu_sel_time)
                            except:
                                stu_do_exp = StuDoExp(
                                    stu_id=student,
                                    stuseltime_id=stu_sel_time,

                                )
                            exproom.stu_num_now += 1
                            exproom.save()
                            exproom_not_choose.remove(exproom)
                            exproom_choose.append(exproom)
                            if exproom.stu_num_now == exproom.machinenum:
                                exproom.is_full = True
                                exproom.save()
                            else:
                                pass
                        else:
                            pass
                    return render(
                        request,
                        self.template_name,
                        {'allow_choose': allow_choose, 'message': u'操作成功', 'exproom_choose': exproom_choose, 'exproom_not_choose': exproom_not_choose}
                    )
                elif request.POST['action'] == 'quit':
                    quit_exproom_list = request.POST.getlist('quit_list')
                    for quit_exproom_id in quit_exproom_list:
                        exproom = ExpRoom.objects.get(classroomid=int(quit_exproom_id))
                        stu_sel_time = StuSelExpTime.objects.get(exproom_id=exproom, stu_id=student)
                        try:
                            stu_sel_time.delete()
                            exproom.stu_num_now -= 1
                            exproom.save()
                            exproom_choose.remove(exproom)
                            exproom_not_choose.append(exproom)
                        except:
                            pass
                    return render(
                        request,
                        self.template_name,
                        {'allow_choose':allow_choose, 'message': u'操作成功', 'exproom_choose': exproom_choose, 'exproom_not_choose': exproom_not_choose}
                    )
                else:
                    return render(
                        request,
                        self.template_name,
                        {'message': u'您的操作有误'}
                    )
        else:
            return HttpResponseRedirect('/student/index2')


def startexp(request):
    template_name = 'student/work/doexp/startexp.html'
    if request.session.get('stu_auth_num', False):
        student = Student.objects.get(stu_auth_num=request.session['stu_auth_num'])
        today = date.today()
        systime = SysTime.objects.get(pk=1)
        startday = systime.startday
        days = 1 + (datetime.combine(today, datetime.now().time()) - datetime.combine(startday, datetime.now().time())).days
        nowweek = divmod(days, 7)[0]
        day = divmod(days, 7)[1]
        if day:
            nowweek += 1
        else:
            day = 7
        day_dict = {1: u'一', 2: u'二', 3: u'三', 4: u'四', 5: u'五', 6: u'六', 7: u'日'}
        weekday = day_dict[day]
        try:
            exproom_list = ExpRoom.objects.filter(semester_start_year=systime.startyear).filter(semester_end_year=systime.endyear).filter(semester=systime.semester).filter(week=nowweek).filter(weekday=weekday)
        except:
            exproom_list = list()
        stu_sel_time_today = list()
        for exproom in exproom_list:
            try:
                stu_sel_time_today.append(
                    StuSelExpTime.objects.filter(stu_id=student).get(exproom_id=exproom)
                )
            except:
                pass
        if not stu_sel_time_today:
            no_time_message = u'您并未选择当前的时间进行实验'
        else:
            no_time_message = None
        return render(
            request,
            template_name,
            {
                'stu_sel_time_today': stu_sel_time_today,
                # 'exproom_now': exproom_now,
                'no_time_message': no_time_message
            }
        )


def if_doexp_today(student, exproom):
    today = date.today()
    systime = SysTime.objects.get(pk=1)
    startday = systime.startday
    days = 1 + (datetime.combine(today, datetime.now().time()) - datetime.combine(startday, datetime.now().time())).days
    nowweek = divmod(days, 7)[0]
    day = divmod(days,7)[1]
    if day:
        nowweek += 1
    else:
        day = 7
    day_dict = {1: u'一', 2: u'二', 3: u'三', 4: u'四', 5: u'五', 6: u'六', 7: u'日'}
    weekday = day_dict[day]
    #u"下面try/except获取今天所有的实验时间"
    try:
        exproom_list = ExpRoom.objects.filter(
            semester_start_year=systime.startyear
        ).filter(
            semester_end_year=systime.endyear
        ).filter(
            semester=systime.semester
        ).filter(
            week=nowweek
        ).filter(
            weekday=weekday
        )
    except:
        exproom_list = list()
    #u"如果参数中的时间属于今天的，那么查找学生选择的记录"
    result = {'cunzai': '', 'start': ''}
    if exproom in exproom_list:
        try:
            stu_sel_exp_today = StuSelExpTime.objects.get(
                exproom_id=exproom,
                stu_id=student,
            )
            result['cunzai'] = True
            result['start'] = (stu_sel_exp_today.is_start and not stu_sel_exp_today.is_finished)
        except:
            result['cunzai'] = False
            result['start'] = False
    return result


class DoExp(View):
    template_name = 'student/work/doexp/doexp.html'
    form2 = forms.ReportForm


    def get(self, request, classroomid):
        if request.session.get('stu_auth_num', False):
            student = Student.objects.get(stu_auth_num=request.session['stu_auth_num'])
            exproom = ExpRoom.objects.get(classroomid=classroomid)
            stu_sel_time = StuSelExpTime.objects.get(stu_id=student, exproom_id=exproom)
            result = if_doexp_today(student, exproom)
            request.session['exproom'] = exproom.classroomid
            if result['cunzai']:
                if not result['start']:
                    stu_classes_all = StuClass.objects.filter(stu_id=student)
                    stu_classes = list()
                    for objects in stu_classes_all:
                        if objects.already_hours < objects.class_id.class_hours:
                            stu_classes.append((objects, objects.class_id.class_hours - objects.already_hours))
                    return render(
                        request,
                        self.template_name,
                        {
                            'form2': self.form2,
                            'stu_classes': stu_classes,
                            'do_exproom': stu_sel_time,
                            'start': result['start']}
                    )
                elif result['start']:
                    studoexp = StuDoExp.objects.filter(
                        stu_id=student
                    ).get(
                        stuseltime_id=stu_sel_time
                    )
                    return render(
                        request,
                        self.template_name,
                        {'stu_do_exp': studoexp, 'start': True, 'form2': self.form2}
                    )
            else:
                return HttpResponse(u"您并未选择该实验!")
        else:
            return HttpResponseRedirect('/student/index2')

    def post(self, request, classroomid):
        import os
        if request.session.get('stu_auth_num', False):
            student = Student.objects.get(stu_auth_num=request.session['stu_auth_num'])
            exproom = ExpRoom.objects.get(classroomid=int(classroomid))
            result = if_doexp_today(student, exproom)
            if result['cunzai'] and (not result['start']):
                stu_class = StuClass.objects.get(stu_id=student, class_id=int(request.POST['class_name']))
                stu_sel_time = StuSelExpTime.objects.get(stu_id=student, exproom_id=exproom)
                if stu_class.class_id.class_hours > stu_class.already_hours:
                    stu_do_exp = StuDoExp(
                        stu_id=student,
                        stuseltime_id=stu_sel_time,
                        stu_class=stu_class,
                        start_time=timezone.now(),
                        stu_start_ip=request.META.get('REMOTE_ADDR'),
                        # end_time=datetime.now(),
                        stu_finish_ip=request.META.get('REMOTE_ADDR')
                    )
                    stu_do_exp.save()
                    stu_sel_time.is_start = True
                    stu_sel_time.save()
                else:
                    message = u'您的操作有误'
                    stu_do_exp = None
                return render(
                    request,
                    self.template_name,
                    {'stu_do_exp': stu_do_exp, 'start': stu_sel_time.is_start, 'form2': self.form2}
                )
            elif result['cunzai'] and result['start']:
                form = forms.ReportForm(request.POST, request.FILES)
                stu_sel_time = StuSelExpTime.objects.get(
                    stu_id=student,
                    exproom_id=exproom,
                )
                stu_do_exp = StuDoExp.objects.get(
                    stu_id=student,
                    stuseltime_id=stu_sel_time,
                )
                if form.is_valid():
                    if not stu_do_exp.stu_exp_report:
                        stu_do_exp.end_time = timezone.now()
                        stu_do_exp.stu_finish_ip = request.META.get('REMOTE_ADDR')
                    report = form.cleaned_data['report']
                    if report.content_type not in settings.REPORT_CONTENT_TYPE:
                        error_message = u'只允许上传pdf文件'
                        return render(
                            request,
                            self.template_name,
                            {'start': True, 'stu_do_exp': stu_do_exp, 'form2': self.form2, 'error_message': error_message}
                        )
                    if stu_do_exp.stu_exp_report:
                        os.remove(stu_do_exp.stu_exp_report.path)
                        stu_do_exp.stu_exp_report = None
                    stu_do_exp.stu_exp_report = report
                    stu_do_exp.end_time = datetime.now()
                    stu_do_exp.is_start = False
                    stu_do_exp.is_finished = True
                    stu_do_exp.save()
                    stuclass = StuClass.objects.filter(stu_id=student).get(class_id=stu_do_exp.stu_class.class_id)
                    stuclass.already_hours += stu_sel_time.hours
                    stuclass.save()
                return render(
                    request,
                    self.template_name,
                    {'start': True, 'stu_do_exp': stu_do_exp, 'form2': self.form2}
                )
            else:
                return HttpResponse(u'您的操作有误')
        else:
            return HttpResponseRedirect("/student/index2")


class ExpHistoryView(ListView):
    template_name = 'student/work/doexp/exphistory.html'
    context_object_name = 'stu_do_exp_list'

    def get_queryset(self):
        self.student = Student.objects.get(pk=self.request.session['stu_auth_num'])
        return StuDoExp.objects.filter(stu_id=self.student).order_by('-end_time')


class NewsView(ListView):
    template_name = 'student/work/news/viewnews.html'
    queryset = News.objects.all().order_by('-create_date')
    context_object_name = 'news_list'


def newsdetail(request, newsid):
    news = News.objects.get(pk=int(newsid))
    return render(
        request,
        'student/work/news/newsdetail.html',
        {'news': news}
    )


def deleteclassreport(request, classid):
    if request.session.get('stu_auth_num', False):
        student = Student.objects.get(stu_auth_num=request.session['stu_auth_num'])
        class_id = Classes.objects.get(class_id=int(classid))
        stuclass = StuClass.objects.get(stu_id=student, class_id=class_id)
        form = forms.ClassReportForm
        try:
            os.remove(stuclass.class_report.path)
            stuclass.class_report = None
        except:
            stuclass.class_report = None
        stuclass.save()
        stu_do_exp_list = StuDoExp.objects.filter(stu_class=stuclass)
        return render(
            request,
            'student/work/class/stuclassdetail.html',
            {'form':form, 'message': u'删除成功，请重新上传', 'stu_class': stuclass, 'stu_do_exp_list': stu_do_exp_list}
        )

    else:
        return HttpResponseRedirect('/student/index2')


