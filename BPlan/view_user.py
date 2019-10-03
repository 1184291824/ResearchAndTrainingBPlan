from django.shortcuts import render, HttpResponse, redirect
from .models import User, LoginRecord, InventoryOperation
from django.contrib.auth import logout
# from django.core.paginator import Paginator
# import datetime
from .request import *
# from .VerificationCode import verification_code_check


# Create your views here.


def login_html(request):
    """返回登录界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 0:
        # if whether_mobile(request) is False:
        return render(request, 'PC/user/login.html')
        # else:
        #     return HttpResponse('mobile')
    else:
        return redirect('BPlan:index')


def login_check(request):
    """检查账户密码是否正确"""
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_password = request.POST['user_password']
        # print(request.session.get('Code', '0'))
        # if verification_code_check(request):
        try:
            user = User.objects.get(user_id__exact=user_id)
            if user_password == user.user_password:
                request.session['login_status'] = 1
                request.session['user_id'] = user.user_id
                request.session['user_name'] = user.user_name
                login_agent = get_agent(request)  # 获取登录的设备信息
                ip = get_ip(request)  # 获取登录的ip
                # location = get_location(ip)  # 通过IP查询地理位置
                login_record = LoginRecord.add_login_record(  # 增加一条登录记录
                    user,
                    login_ip=ip,
                    login_browser=login_agent['browser'],
                    login_system=login_agent['system'],
                    login_device=login_agent['device'],
                    # login_location=location,
                )
                login_record.save()  # 保存登录记录
                return HttpResponse("successLogin")  # 返回登录成功
            else:
                return HttpResponse("passwordWrong")  # 返回密码错误
        except User.DoesNotExist:
            return HttpResponse("idDoesNotExist")  # 返回用户不存在
        # else:
        #     return HttpResponse('codeWrong')  # 返回验证码错误
    else:
        return redirect('BPlan:index')


def login_logout(request):
    """用户注销"""
    logout(request)
    return redirect('BPlan:index')


def register_html(request):
    """返回基础注册界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 0:
        # group_list = Group.objects.all().exclude(group_id__iexact='9161040G00')
        # if whether_mobile(request) is False:
        return render(request, 'PC/user/register.html', {
            # 'group_list': group_list,
            'user_identity_choice': User.USER_IDENTITY_CHOICE,
            'user_question_choice': User.USER_QUESTION_CHOICE,
            'user_gender_choice': User.USER_GENDER_CHOICE,
        })
        # else:
        #     return HttpResponse('mobile')
    else:
        return redirect('BPlan:index')


def register_check(request):
    """检查注册信息，如果正确就添加用户"""
    if request.method == 'POST':
        # if verification_code_check(request):
        user_id = request.POST['user_id']
        if User.objects.filter(user_id__exact=user_id):
            return HttpResponse('idExist')
        user_password = request.POST['user_password']
        # user_group = request.POST['user_group']
        # group = Group.objects.get(pk=user_group)
        user = User.add_user(user_id=user_id, user_password=user_password)
        user.user_gender = (request.POST['user_gender'] == 'True')
        user.user_name = request.POST['user_name']
        user.user_identity = int(request.POST['user_identity'])
        user.user_question = int(request.POST['user_question'])
        user.user_question_answer = request.POST['user_question_answer']
        user.save()
        return HttpResponse('success')  # for Ajax
        # return HttpResponse('codeWrong')
    return redirect('BPlan:index')


def change_password_html(request):
    """返回更改密码的页面"""
    user_id = request.session.get('user_id', '')
    user_question_choice = User.USER_QUESTION_CHOICE
    # if whether_mobile(request) is False:
    return render(request, 'PC/user/changePassword.html', {
        'user_id': user_id,
        'user_question_choice': user_question_choice,
    })
    # else:
    #     return HttpResponse('mobile')


def change_password_check(request):
    """检查密码更改的信息，如果正确就更改密码"""
    if request.method == 'POST':
        # if verification_code_check(request):
        user_id = request.POST['user_id']
        try:
            user = User.objects.get(user_id__exact=user_id)
            if int(request.POST['user_question']) == user.user_question \
                    and request.POST['user_question_answer'] == user.user_question_answer:
                user.user_password = request.POST['user_password']
                user.save()
                logout(request)
                return HttpResponse('success')
            else:
                return HttpResponse('questionWrong')
        except User.DoesNotExist:
            return HttpResponse('idDoesNotExist')
        # return HttpResponse('codeWrong')
    else:
        return redirect('BPlan:index')


def change_question_html(request):
    """返回更改密保问题的界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        user_question_choice = User.USER_QUESTION_CHOICE
        # if whether_mobile(request) is False:
        return render(request, 'PC/user/changeQuestion.html', {
            'user_question_choice': user_question_choice,
        })
        # else:
        #     return HttpResponse('mobile')
    else:
        return redirect('BPlan:index')


def change_question_check(request):
    """验证密码的正确性，修改密保问题"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1 and request.method == 'POST':
        # if verification_code_check(request):
        user_id = request.session['user_id']
        user = User.objects.get(user_id__exact=user_id)
        if user.user_password == request.POST['user_password']:
            user.user_question = int(request.POST['user_question'])
            user.user_question_answer = request.POST['user_question_answer']
            user.save()
            return HttpResponse('success')
        else:
            return HttpResponse('passwordWrong')
        # return HttpResponse('codeWrong')
    else:
        return redirect('BPlan:index')


def change_personal_information(request):
    """返回个人信息/修改个人信息界面"""
    if request.session.get('login_status', 0):
        if request.method == 'GET':
            user = User.objects.get(user_id__exact=request.session['user_id'])
            if request.GET.get('page', 'show') == 'change':
                return render(request, 'PC/user/changePersonalInformationChange.html', {'user': user})
            else:
                inventory_base = InventoryOperation.objects.filter(inventory_operation_user__exact=user.user_id)
                inventory_in_num = inventory_base.filter(inventory_operation_category=0).count()
                inventory_out_num = inventory_base.filter(inventory_operation_category=1).count()
                inventory_create_num = inventory_base.filter(inventory_operation_category=2).count()
                return render(request, 'PC/user/changePersonalInformationShow.html', {
                    'user': user,
                    'inventory_in_num': inventory_in_num,
                    'inventory_out_num': inventory_out_num,
                    'inventory_create_num': inventory_create_num,
                })

        elif request.method == 'POST':
            # if verification_code_check(request):
            user = User.objects.get(user_id__exact=request.session['user_id'])
            user.user_name = request.POST['user_name']
            user.user_gender = (request.POST['user_gender'] == 'True')
            # user.user_identity = int(request.POST['user_identity'])
            user.save()
            return HttpResponse('success')
            # else:
            #     return HttpResponse('codeWrong')
    else:
        return redirect('BPlan:index')


def login_record_html(request):
    """返回登录记录的界面"""
    if request.session.get('login_status', 0):
        user_id = request.session['user_id']
        log_list = LoginRecord.objects.filter(login_user__user_id__exact=user_id).order_by("-login_time")  # 按登录时间的倒序排列
        # page = request.GET.get('page', 1)
        # paginator = Paginator(log_list, 10)  # 分页，每页10项
        # log_display = paginator.get_page(page)
        return render(request, 'PC/user/loginRecordShow.html', {
            'paginator': log_list[0:12]  # 仅显示最近的12条登录记录
        })
    else:
        return redirect('BPlan:index')
