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
        '</h1><h1>location:' + location + '</h1>' +
        request.META['HTTP_USER_AGENT']
    )


def index(request):
    login_status = request.session.get('login_status', 0)
    ask_status = request.session.get('ask_status', 0)
    if ask_status == 0:
        user = User.objects.get(user_name__exact='访客记录')
        login_agent = get_agent(request)  # 获取登录的设备信息
        ip = get_ip(request)  # 获取登录的ip
        location = get_location(ip)  # 通过IP查询地理位置
        login_record = LoginRecord.add_login_record(  # 增加一条登录记录
            user,
            login_ip=ip,
            login_browser=login_agent['browser'],
            login_system=login_agent['system'],
            login_device=login_agent['device'],
            login_location=location,
        )
        login_record.save()  # 保存登录记录
    request.session['ask_status'] = 1
    return HttpResponse('这是主页'+'login_status:'+str(login_status)+'ask_status:'+str(request.session['ask_status']))


def login_html(request):
    """返回登录界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 0:
        if whether_mobile(request) is False:
            return render(request, 'PC/login.html')
        else:
            return HttpResponse('mobile')
    else:
        return redirect('BPlan:index')


def login_check(request):
    """检查账户密码是否正确"""
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_password = request.POST['user_password']
        try:
            user = User.objects.get(user_id__exact=user_id)
            if user_password == user.user_password:
                request.session['login_status'] = 1
                request.session['user_id'] = user.user_id
                login_agent = get_agent(request)  # 获取登录的设备信息
                ip = get_ip(request)  # 获取登录的ip
                location = get_location(ip)  # 通过IP查询地理位置
                login_record = LoginRecord.add_login_record(  # 增加一条登录记录
                    user,
                    login_ip=ip,
                    login_browser=login_agent['browser'],
                    login_system=login_agent['system'],
                    login_device=login_agent['device'],
                    login_location=location,
                )
                login_record.save()  # 保存登录记录
                return HttpResponse("successLogin")  # 返回登录成功
            else:
                return HttpResponse("passwordWrong")  # 返回密码错误
        except User.DoesNotExist:
            return HttpResponse("idDoesNotExist")  # 返回用户不存在
    else:
        return redirect('BPlan:index')


def login_logout(request):
    """用户注销"""
    logout(request)
    return redirect('BPlan:index')


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
        return redirect('BPlan:index')


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
    return redirect('BPlan:index')


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
        return redirect('BPlan:index')


def register_check_more(request):
    """检查注册的更多信息，丰富用户的信息"""
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
    return redirect('BPlan:index')


def change_password_html(request):
    """返回更改密码的页面"""
    user_id = request.session.get('user_id', '')
    user_question_choice = User.USER_QUESTION_CHOICE
    if whether_mobile(request) is False:
        return render(request, 'PC/changePassword.html', {
            'user_id': user_id,
            'user_question_choice': user_question_choice,
        })
    else:
        return HttpResponse('mobile')


def change_password_check(request):
    """检查密码更改的信息，如果正确就更改密码"""
    if request.method == 'POST':
        user_id = request.POST['user_id']
        try:
            user = User.objects.get(user_id__exact=user_id)
            if request.POST['user_name'] == user.user_name\
                    and int(request.POST['user_question']) == user.user_question \
                    and request.POST['user_question_answer'] == user.user_question_answer:
                user.user_password = request.POST['user_password']
                user.save()
                return HttpResponse('success')
            else:
                return HttpResponse('wrong')
        except User.DoesNotExist:
            return HttpResponse('idDoesNotExist')
    else:
        return redirect('BPlan:index')


def show_inventory_all_html(request):
    """返回所有的库存的摘要信息"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        inventory_list = Inventory.objects.all()
    # inventory_group = []
    # for inventory in inventory_list:
    #     inventory_group_dict = [
    #         # inventory.inventory_id,
    #         inventory.inventory_name,
    #         inventory.inventory_category,
    #         inventory.inventory_num+inventory.inventory_unit,
    #         inventory.inventory_details,
    #         # User.objects.get(user_id__exact=inventory.inventory_create_user).user_name,
    #         # inventory.inventory_create_time,
    #         # User.objects.get(user_id__exact=inventory.inventory_recent_change_user).user_name,
    #         # inventory.inventory_recent_change_time,
    #     ]
    #     inventory_group.append(inventory_group_dict)
        if whether_mobile(request) is False:
            return render(request, 'PC/showInventoryAll.html', {'inventory_list': inventory_list})
        else:
            return HttpResponse('mobile')
    else:
        return redirect('BPlan:index')


def show_inventory_detail_html(request):
    """返回某一库存的详细信息"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        inventory_pk = request.GET.get('id')
        try:
            inventory = Inventory.objects.get(pk=inventory_pk)
            if whether_mobile(request) is False:
                return render(request, 'PC/showInventoryDetail.html', {'inventory': inventory})
            else:
                return HttpResponse('mobile')
        except Inventory.DoesNotExist:
            return redirect('BPlan:show_inventory_all_html')
    else:
        return redirect('BPlan:index')
