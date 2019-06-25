from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib.auth import logout
from django.utils import timezone
from .request import *

# Create your views here.


def test(request):
    login_information = get_agent(request)
    ip = get_ip(request)
    location = get_location(ip)
    return HttpResponse(
        '<h1>browser:' + login_information['browser'] +
        '</h1><h1>system:' + login_information['system'] +
        '</h1><h1>device:' + login_information['device'] +
        '</h1><h1>ip:' + ip +
        '</h1><h1>location:' + location + '</h1>'+
        request.META['HTTP_USER_AGENT']
    )


def login_html(request):
    """返回登录界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 0:
        if whether_mobile(request) is False:
            return render(request, 'PC/login.html')
        else:
            return HttpResponse('mobile')
    else:
        return redirect('BPlan:test')


def login_check(request):
    """检查账户密码是否正确"""
    if request.method is 'POST':
        user_id = request.POST['user_id']
        user_password = request.POST['user_password']
        try:
            user = User.objects.get(user_id__exact=user_id)
            if user_password == user.user_password:
                request.session['login_status'] = 1
                request.session['user_id'] = user.user_id
                return HttpResponse("successLogin")
            else:
                return HttpResponse("passwordWrong")
        except User.DoesNotExist:
            return HttpResponse("idDoesNotExist")
    else:
        return redirect('BPlan:login_html')


def register_html_base(request):
    """返回基础注册界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 0:
        group_list = Group.objects.all()
        if whether_mobile(request) is False:
            return render(request, 'PC/registerBase.html', {'group_list': group_list})
        else:
            return HttpResponse('mobile')
    else:
        return redirect('BPlan:test')


def register_check_base(request):
    """检查注册信息，如果正确就添加用户"""
    if request.method == 'POST':
        user_id = request.POST['user_id']
        if User.objects.filter(user_id__exact=user_id):
            return HttpResponse('idExist')
        user_password = request.POST['user_password']
        user_group = request.POST['user_group']
        group = Group.objects.get(pk=user_group)
        user = User.add_user(user_id=user_id, user_password=user_password, user_group=group)
        user.save()
        request.session['user_id'] = user_id
        request.session['lastPage'] = 'register/base/'
        return redirect('BPlan:register_html_more')
    return redirect('BPlan:test')


def register_html_more(request):
    """返回更多信息的注册界面"""
    last_page = request.session.get('lastPage', None)
    login_status = request.session.get('login_status', 0)
    if last_page == 'register/base/' and login_status == 0:
        user_identity_choice = User.USER_IDENTITY_CHOICE
        user_question_choice = User.USER_QUESTION_CHOICE
        if whether_mobile(request) is False:
            return render(request, 'PC/registerMore.html', {
                'user_identity_choice': user_identity_choice,
                'user_question_choice': user_question_choice,
            })
        else:
            return HttpResponse('mobile')
    else:
        return redirect('BPlan:test')


def register_check_more(request):
    """检查注册信息，如果正确就添加用户"""
    if request.method == 'POST':
        user_id = request.session['user_id']
        user = User.objects.get(user_id__exact=user_id)
        if request.POST['user_gender'] == 'girl':
            user.user_gender = False
        user.user_name = request.POST['user_name']
        user.user_identity = int(request.POST['user_identity'])
        user.user_question = int(request.POST['user_question'])
        user.user_question_answer = request.POST['user_question_answer']
        user.save()
        request.session['lastPage'] = 'register/more/'
        return HttpResponse('successRegister')
    return redirect('BPlan:test')
