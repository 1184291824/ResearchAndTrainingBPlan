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
    if request.method is 'POST':
        user_id = request.POST['user_id']
        user_password = request.POST['user_password']
        try:
            user = User.objects.get(user_id__exact=user_id)
            if user_password == user.user_password:
                request.session['login_status'] = 1
                request.session['user_id'] = user.user_id
                return HttpResponse("true")
            else:
                return HttpResponse("passwordWrong")
        except User.DoesNotExist:
            return HttpResponse("idDoesNotExist")
    else:
        return redirect('BPlan:login_html')

