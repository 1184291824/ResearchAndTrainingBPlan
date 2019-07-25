from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from .models import *
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.utils import timezone
import datetime
from .request import *
from .VerificationCode import verification_code_check


# Create your views here.


def test(request):
    inventory_id = request.GET.get('id')
    return HttpResponse(inventory_id)


def whether_login(request):
    """判断是否处于登录状态"""
    login_status = request.session.get('login_status', 0)
    user_id = request.session.get('user_id', 0)
    user_name = request.session.get('user_name', 0)
    result = {
        'login_status': login_status,
        'user_id': user_id,
        'user_name': user_name,
    }
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def index(request):
    # login_status = request.session.get('login_status', 0)
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
    return render(request, 'PC/index.html')
    # return HttpResponse('这是主页'+'login_status:'+str(login_status)+'ask_status:'+str(request.session['ask_status']))


def login_html(request):
    """返回登录界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 0:
        # if whether_mobile(request) is False:
        return render(request, 'PC/login.html')
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
        if verification_code_check(request):
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
            return HttpResponse('codeWrong')  # 返回验证码错误
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
        group_list = Group.objects.all().exclude(group_id__iexact='9161040G00')
        # if whether_mobile(request) is False:
        return render(request, 'PC/register.html', {
            'group_list': group_list,
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
        if verification_code_check(request):
            user_id = request.POST['user_id']
            if User.objects.filter(user_id__exact=user_id):
                return HttpResponse('idExist')
            user_password = request.POST['user_password']
            user_group = request.POST['user_group']
            group = Group.objects.get(pk=user_group)
            user = User.add_user(user_id=user_id, user_password=user_password, user_group=group)
            user.user_gender = (request.POST['user_gender'] == 'True')
            user.user_name = request.POST['user_name']
            user.user_identity = int(request.POST['user_identity'])
            user.user_question = int(request.POST['user_question'])
            user.user_question_answer = request.POST['user_question_answer']
            user.save()
            return HttpResponse('success')  # for Ajax
        return HttpResponse('codeWrong')
    return redirect('BPlan:index')


def change_password_html(request):
    """返回更改密码的页面"""
    user_id = request.session.get('user_id', '')
    user_question_choice = User.USER_QUESTION_CHOICE
    # if whether_mobile(request) is False:
    return render(request, 'PC/changePassword.html', {
        'user_id': user_id,
        'user_question_choice': user_question_choice,
    })
    # else:
    #     return HttpResponse('mobile')


def change_password_check(request):
    """检查密码更改的信息，如果正确就更改密码"""
    if request.method == 'POST':
        if verification_code_check(request):
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
        return HttpResponse('codeWrong')
    else:
        return redirect('BPlan:index')


def change_question_html(request):
    """返回更改密保问题的界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        user_question_choice = User.USER_QUESTION_CHOICE
        # if whether_mobile(request) is False:
        return render(request, 'PC/changeQuestion.html', {
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
        if verification_code_check(request):
            user_id = request.session['user_id']
            user = User.objects.get(user_id__exact=user_id)
            if user.user_password == request.POST['user_password']:
                user.user_question = int(request.POST['user_question'])
                user.user_question_answer = request.POST['user_question_answer']
                user.save()
                return HttpResponse('success')
            else:
                return HttpResponse('passwordWrong')
        return HttpResponse('codeWrong')
    else:
        return redirect('BPlan:index')


def change_personal_information(request):
    """返回个人信息/修改个人信息界面"""
    if request.session.get('login_status', 0):
        if request.method == 'GET':
            user = User.objects.get(user_id__exact=request.session['user_id'])
            if request.GET.get('page', 'show') == 'change':
                return render(request, 'PC/changePersonalInformationChange.html', {'user': user})
            else:
                inventory_base = InventoryOperation.objects.filter(inventory_operation_user__exact=user.user_id)
                inventory_in_num = inventory_base.filter(inventory_operation_category=0).count()
                inventory_out_num = inventory_base.filter(inventory_operation_category=1).count()
                inventory_create_num = inventory_base.filter(inventory_operation_category=2).count()
                return render(request, 'PC/changePersonalInformationShow.html', {
                    'user': user,
                    'inventory_in_num': inventory_in_num,
                    'inventory_out_num': inventory_out_num,
                    'inventory_create_num': inventory_create_num,
                })

        elif request.method == 'POST':
            if verification_code_check(request):
                user = User.objects.get(user_id__exact=request.session['user_id'])
                user.user_name = request.POST['user_name']
                user.user_gender = (request.POST['user_gender'] == 'True')
                user.user_identity = int(request.POST['user_identity'])
                user.save()
                return HttpResponse('success')
            else:
                return HttpResponse('codeWrong')
    else:
        return redirect('BPlan:index')


def inventory_show_all_html(request):
    """返回所有的库存的摘要信息"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        inventory_list = Inventory.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(inventory_list, 6)
        inventory_display = paginator.get_page(page)
        return render(request, 'PC/inventoryShowAll.html', {
            'paginator': inventory_display,
        })
    else:
        return redirect('BPlan:index')


def inventory_show_detail_html(request):
    """返回某一库存的详细信息"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        inventory_id = request.GET.get('id')
        try:
            inventory = Inventory.objects.get(inventory_id__exact=inventory_id)
            return render(request, 'PC/inventoryShowDetail.html', {
                'inventory': inventory,
            })
        except Inventory.DoesNotExist:
            return redirect('BPlan:inventory_show_all_html')
    else:
        return redirect('BPlan:index')


def inventory_change_detail(request):
    """改变库存的详细信息"""
    if request.session.get('login_status', 0):
        if request.method == 'GET':
            inventory_id = request.GET.get('id')
            inventory = Inventory.objects.get(inventory_id__exact=inventory_id)
            return render(request, 'PC/inventoryChangeDetail.html', {
                'inventory': inventory,
            })
        elif request.method == 'POST':
            inventory_id = request.POST.get('inventory_id')
            inventory = Inventory.objects.get(inventory_id__exact=inventory_id)
            inventory.inventory_name = request.POST['inventory_name']
            inventory.inventory_category = request.POST['inventory_category']
            inventory.inventory_unit = request.POST['inventory_unit']
            inventory.inventory_details = request.POST['inventory_details']
            inventory.save()
            return HttpResponse('success')
    else:
        return redirect('BPlan:index')


def inventory_create_html(request):
    """返回创建新的库存的界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        # if whether_mobile(request) is False:
        return render(request, 'PC/inventoryCreate.html')
        # else:
        #     return HttpResponse('mobile')
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
        return render(request, 'PC/inventoryChange.html', {
            'change_type': change_type,
            'inventory_id': inventory.inventory_id,
            'inventory_name': inventory.inventory_name,
            'inventory_num': inventory.inventory_num,
        })
    else:
        return redirect('BPlan:index')


def inventory_create_add(request):
    """创建新的库存"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1 and request.method == 'POST':
        if verification_code_check(request) is False:
            return HttpResponse('codeWrong')
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
            inventory_create_user_name=request.session['user_name'],
        )
        inventory.save()  # 保存生效
        # request.session['inventory_operation_category'] = 2

        '''这里请加入添加库存记录的函数'''
        inventory_operation_user_agent = get_agent(request)  # 获取登录的设备信息
        InventoryOperation.add_inventory_operation(
            inventory_operation_user=inventory.inventory_create_user,
            inventory_operation_user_name=request.session.get('user_name'),
            inventory_operation_user_ip=get_ip(request),
            inventory_operation_user_browser=inventory_operation_user_agent['browser'],
            inventory_operation_user_system=inventory_operation_user_agent['system'],
            inventory_operation_user_device=inventory_operation_user_agent['device'],
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
        inventory.inventory_recent_change_user_name = request.session['user_name']
        inventory.save()  # 保存生效

        '''这里请加入添加库存记录的函数'''
        inventory_operation_user_agent = get_agent(request)  # 获取登录的设备信息
        InventoryOperation.add_inventory_operation(
            inventory_operation_user=inventory.inventory_recent_change_user,
            inventory_operation_user_name=request.session.get('user_name'),
            inventory_operation_user_ip=get_ip(request),
            inventory_operation_user_browser=inventory_operation_user_agent['browser'],
            inventory_operation_user_system=inventory_operation_user_agent['system'],
            inventory_operation_user_device=inventory_operation_user_agent['device'],
            inventory_operation_category=inventory_operation_category,
            inventory_operation_num=inventory_operation_num,
            inventory_num=inventory.inventory_num,
            inventory_operation_object=inventory,
        ).save()

        return HttpResponse('success')
    else:
        return redirect('BPlan:index')


def inventory_search(request):
    """查询库存"""
    if request.session.get('login_status', 0):
        if request.method == 'GET':
            search_type = request.GET.get('search_type', '')
            search = request.GET.get('search', '')
            if search_type and search:
                if search_type == 'inventory_id':
                    inventory = Inventory.objects.filter(inventory_id__contains=search)
                elif search_type == 'inventory_name':
                    inventory = Inventory.objects.filter(inventory_name__contains=search)
                elif search_type == 'inventory_details':
                    inventory = Inventory.objects.filter(inventory_details__contains=search)
                elif search_type == 'inventory_create_user_name':
                    inventory = Inventory.objects.filter(inventory_create_user_name__contains=search)
                elif search_type == 'inventory_recent_change_user_name':
                    inventory = Inventory.objects.filter(inventory_recent_change_user_name__contains=search)
                if inventory.exists() is False:
                    inventory = ''
            else:
                inventory = 'noSearch'
            return render(request, 'PC/inventorySearch.html', {
                'paginator': inventory,
                'search_type': search_type,
                'search': search,
            })
    else:
        return redirect('BPlan:index')


def inventory_operation_html(request):
    """显示操作记录"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1 and request.method == 'GET':
        if request.GET.get('type', 0) == 'inventory':
            inventory_id = request.GET.get('id')
            inventory_operation = InventoryOperation.objects.filter(
                inventory_operation_object__inventory_id__exact=inventory_id
            ).order_by('-inventory_operation_create_time')
        elif request.GET.get('type', 0) == 'user':
            user_id = request.session.get('user_id')
            inventory_operation = InventoryOperation.objects.filter(
                inventory_operation_user=user_id
            ).order_by('-inventory_operation_create_time')
        else:
            return render(request, 'PC/inventoryOperationSearch.html')
        if inventory_operation:
            return render(request, 'PC/inventoryOperationShow.html', {'paginator': inventory_operation})
        else:
            return render(request, 'PC/inventoryOperationShow.html', {
                'paginator': ''
            })
    else:
        return redirect('BPlan:index')


def login_record_html(request):
    """返回登录记录的界面"""
    if request.session.get('login_status', 0):
        user_id = request.session['user_id']
        log_list = LoginRecord.objects.filter(login_user__user_id__exact=user_id)
        page = request.GET.get('page', 1)
        paginator = Paginator(log_list, 10)  # 分页，每页10项
        log_display = paginator.get_page(page)
        return render(request, 'PC/loginRecordShow.html', {
            'paginator': log_display
        })
    else:
        return redirect('BPlan:index')


def login_record_ask_html(request):
    """返回网站访问量统计界面"""
    today = datetime.date.today()
    base_record = LoginRecord.objects.filter(
        login_user__user_id__exact='9161040G0000'
    )  # 访问量查询集

    '''获取每日访问量'''
    ask_record_display = []  # 每日访问量的数组
    time_label = []  # 存放日期的数组
    if whether_mobile(request):
        day_range = 5  # 日期的显示范围，如果是移动设备，仅显示5天
    else:
        day_range = 10
    for i in range(0, day_range):
        date_num = today - datetime.timedelta(days=i)
        ask_record_display.append(base_record.filter(login_date=date_num).count())
        time_label.append(date_num)

    '''获取访问系统占比'''
    windows_num = base_record.filter(login_system__icontains='windows').count()
    ios_num = base_record.filter(login_system__icontains='iOS').count()
    android_num = base_record.filter(login_system__icontains='Android').count()
    return render(request, 'PC/askRecord.html', {
        'ask_record_display': ask_record_display,  # 每日的访问记录
        'time_label': time_label,  # 横轴，日期
        'wholeCount': base_record.count(),  # 总访问量
        'system_num': [android_num, windows_num, ios_num],
    })


def inventory_operation_chart_html(request):
    """返回每日出入库界面， 显示库存操作的统计数据"""
    if request.session.get('login_status', 0):
        inventory_id = request.GET.get('id')
        if inventory_id:  # 如果有限定是某个库存的操作记录统计，则先过滤一下
            inventory_operation_base = InventoryOperation.objects.filter(inventory_operation_object__inventory_id=inventory_id)
        else:
            inventory_operation_base = InventoryOperation.objects.all()

        '''获取每日出入库量'''
        today = datetime.date.today()  # 获取今天的日期
        in_num = []  # 每日入库的数组
        out_num = []  # 每日出库的数组
        create_num = []  # 每日创建库的数组
        time_label = []  # 存放日期的数组
        if whether_mobile(request):
            day_range = 5  # 日期的显示范围，如果是移动设备，仅显示5天
        else:
            day_range = 10
        for i in range(0, day_range):
            date_num = today - datetime.timedelta(days=i)
            in_num.append(inventory_operation_base.filter(
                inventory_operation_category=0
            ).filter(inventory_operation_create_date=date_num).count())
            out_num.append(inventory_operation_base.filter(
                inventory_operation_category=1
            ).filter(inventory_operation_create_date=date_num).count())
            create_num.append(inventory_operation_base.filter(
                inventory_operation_category=2
            ).filter(inventory_operation_create_date=date_num).count())
            time_label.append(date_num)

        return render(request, 'PC/inventoryOperationChart.html', {
            'time_label': time_label,
            'in_num': in_num,
            'out_num': out_num,
            'create_num': create_num,
        })
    else:
        return redirect('BPlan:index')
