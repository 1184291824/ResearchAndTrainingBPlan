# API for WeChat miniProgram
# Attention: csrf is OFF in the WXApi, the verification method is wx_AppId

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # 局部禁用csrf
from .models import *
from django.contrib.auth import logout
from django.core.paginator import Paginator
import datetime
from .request import *
from .VerificationCode import verification_code_check


wx_AppId = 'wxb627d1c46bb3a79c'  # 微信小程序的AppId


@csrf_exempt  # 局部禁用csrf
def wx_login_check(request):
    """登录验证"""
    result = {  # json格式数据
        'status': '',  # 访问状态('success' or 'fail')
        'information': '',  # 返回的信息
    }
    if request.session.get('login_status', 0) == 0 and request.method == 'POST' and request.POST.get('wx_AppId') == wx_AppId:
        # 看是否已经登录，访问的方式是否为POST，微信的AppId是否正确
        result['status'] = 'success'  # 返回成功状态
        if verification_code_check(request, "POST") is True:  # 检查验证码是否正确
            user_id = request.POST['user_id']  # 获得用户账号
            try:
                user = User.objects.get(user_id__exact=user_id)  # 从数据库中找这个用户，如果不错在报DoesNotExist的错误
                user_password = request.POST['user_password']
                if user.user_password == user_password:  # 检查用户的密码是否正确
                    result['information'] = 'successLogin'  # 密码正确，返回成功登录
                    request.session['login_status'] = 1  # 往session里存放登录成功的信息
                    request.session['user_id'] = user_id  # 往session里存放账号
                    request.session['user_name'] = user.user_name  # 往session里存放用户姓名
                else:
                    result['information'] = 'passwordWrong'  # 密码错误
            except User.DoesNotExist:
                result['information'] = 'idDoesNotExist'  # 用户不存在
        else:
            result['information'] = 'codeWrong, your code is'+request.POST['code']+',but the right code is'+request.session['Code']  # 验证码错误
    else:
        result['status'] = 'fail'  # 访问出错，返回fail
    return JsonResponse(result)


@csrf_exempt  # 局部禁用CSRF
def wx_logout(request):
    """注销"""
    result = {  # json格式数据
        'status': '',  # 访问状态('success' or 'fail')
    }
    if request.session.get('login_status', 0) == 1 and request.method == 'GET' and request.GET['wx_AppId'] == wx_AppId:
        result['status'] = 'success'
        logout(request)  # 注销，删除所有的session
    else:
        result['status'] = 'fail'
    return JsonResponse(result)
