from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import logout
from django.utils import timezone
from .request import *

# Create your views here.


def test(request):
    login_information = get_agent(request)
    ip = get_ip(request)
    location = get_location(ip)
    # return HttpResponse(
    #     '<h1>browser:' + login_information['browser'] +
    #     '</h1><h1>system:' + login_information['system'] +
    #     '</h1><h1>device:' + login_information['device'] +
    #     '</h1><h1>ip:' + ip +
    #     '</h1><h1>location:' + location + '</h1>' +
    #     request.META['HTTP_USER_AGENT']
    # )

    return JsonResponse(login_information)


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
                request.session['user_name'] = user.user_name
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
        # return HttpResponse('success')  # for Ajax
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


def inventory_show_all_html(request):
    """返回所有的库存的摘要信息"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        inventory_list = Inventory.objects.all()
        if whether_mobile(request) is False:
            return render(request, 'PC/inventoryShowAll.html', {'inventory_list': inventory_list})
        else:
            return HttpResponse('mobile')
    else:
        return redirect('BPlan:index')


def inventory_show_detail_html(request):
    """返回某一库存的详细信息"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        inventory_id = request.GET.get('id')
        try:
            inventory = Inventory.objects.get(inventory_id__exact=inventory_id)
            create_user = User.objects.get(user_id__exact=inventory.inventory_create_user).user_name
            change_user = User.objects.get(user_id__exact=inventory.inventory_recent_change_user).user_name
            if whether_mobile(request) is False:
                return render(request, 'PC/inventoryShowDetail.html', {
                    'inventory': inventory,
                    'create_user': create_user,
                    'change_user': change_user,
                })
            else:
                return HttpResponse('mobile')
        except Inventory.DoesNotExist:
            return redirect('BPlan:inventory_show_all_html')
    else:
        return redirect('BPlan:index')


def inventory_create_html(request):
    """返回创建新的库存的界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        if whether_mobile(request) is False:
            return render(request, 'PC/inventoryCreate.html')
        else:
            return HttpResponse('mobile')
    else:
        return redirect('BPlan:index')


def inventory_change_html(request):
    """返回出库入库的界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        change_type = int(request.GET.get('type', 2))
        if change_type < 0 or change_type > 1:
            return redirect('BPlan:inventory_show_all_html')

        inventory_id = request.GET.get('id', 0)
        try:
            inventory = Inventory.objects.get(inventory_id__exact=inventory_id)
        except Inventory.DoesNotExist:
            return redirect('BPlan:inventory_show_all_html')

        if whether_mobile(request) is False:
            return render(request, 'PC/inventoryChange.html', {
                'change_type': change_type,
                'inventory_id': inventory.inventory_id,
                'inventory_name': inventory.inventory_name,
                'inventory_num': inventory.inventory_num,
            })
        else:
            return HttpResponse('mobile')
    else:
        return redirect('BPlan:index')


def inventory_create_add(request):
    """创建新的库存"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1 and request.method == 'POST':
        inventory_id = request.POST['inventory_id']
        if Inventory.objects.filter(inventory_id__exact=inventory_id):
            return HttpResponse('idExist')
        inventory_name = request.POST['inventory_name']
        inventory_category = request.POST['inventory_category']
        inventory_num = int(request.POST['inventory_num'])
        inventory_unit = request.POST['inventory_unit']
        inventory_details = request.POST['inventory_details']
        inventory_create_user = request.session['user_id']  # 获取创建人的id
        inventory = Inventory.add_inventory(  # 增加库存
            inventory_id=inventory_id,
            inventory_name=inventory_name,
            inventory_category=inventory_category,
            inventory_num=inventory_num,
            inventory_unit=inventory_unit,
            inventory_details=inventory_details,
            inventory_create_user=inventory_create_user,
        )
        inventory.save()  # 保存生效
        # request.session['inventory_operation_category'] = 2

        '''这里请加入添加库存记录的函数'''
        InventoryOperation.add_inventory_operation(
            inventory_operation_user=inventory.inventory_create_user,
            inventory_operation_user_name=request.session.get('user_name'),
            inventory_operation_user_ip=get_ip(request),
            inventory_operation_category=2,
            inventory_operation_num=inventory.inventory_num,
            inventory_num=inventory.inventory_num,
            inventory_operation_object=inventory
        ).save()

        return HttpResponse('success')
    else:
        return redirect('BPlan:index')


def inventory_change_add(request):
    """出入库存"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1 and request.method == 'POST':
        inventory_id = request.POST['inventory_id']
        inventory = Inventory.objects.get(inventory_id__exact=inventory_id)
        inventory_operation_num = int(request.POST['inventory_operation_num'])
        inventory_operation_category = int(request.POST['inventory_operation_category'])
        if inventory_operation_category == 0:
            inventory.inventory_num += inventory_operation_num
        else:
            if inventory_operation_num <= inventory.inventory_num:
                inventory.inventory_num -= inventory_operation_num
            else:
                return HttpResponse('outToMany')
        inventory.inventory_recent_change_user = request.session['user_id']  # 记录用户更改人的id
        inventory.save()  # 保存生效

        '''这里请加入添加库存记录的函数'''
        InventoryOperation.add_inventory_operation(
            inventory_operation_user=inventory.inventory_recent_change_user,
            inventory_operation_user_name=request.session.get('user_name'),
            inventory_operation_user_ip=get_ip(request),
            inventory_operation_category=inventory_operation_category,
            inventory_operation_num=inventory_operation_num,
            inventory_num=inventory.inventory_num,
            inventory_operation_object=inventory
        ).save()

        return HttpResponse('success')
    else:
        return redirect('BPlan:index')


def inventory_operation_html_inventory(request):
    """显示某个库存的操作记录"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        inventory_id = request.GET.get('id')
        inventory_operation = InventoryOperation.objects.\
            filter(inventory_operation_object__inventory_id__exact=inventory_id).\
            order_by('-inventory_operation_create_time')
        if inventory_operation:
            return render(request, 'PC/inventoryOperationInventory.html', {'inventory_operation': inventory_operation})
        else:
            return redirect('BPlan:inventory_show_all_html')
    else:
        return redirect('BPlan:index')


def inventory_operation_html_user(request):
    """显示某个人的操作记录"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        user_id = request.session.get('user_id')
        inventory_operation = InventoryOperation.objects.\
            filter(inventory_operation_user=user_id).\
            order_by('-inventory_operation_create_time')
        return render(request, 'PC/inventoryOperationUser.html', {'inventory_operation': inventory_operation})
    else:
        return redirect('BPlan:index')


def inventory_operation_check_user(request):
    """检查这个人是否有操作记录"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        user_id = request.session.get('user_id')
        inventory_operation = InventoryOperation.objects.\
            filter(inventory_operation_user=user_id).\
            order_by('-inventory_operation_create_time')
        if inventory_operation:
            return HttpResponse('success')
        else:
            return HttpResponse('DoesNotExist')
    else:
        return redirect('BPlan:index')



