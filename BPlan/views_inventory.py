from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from .models import *
import datetime
from .request import *
# from .VerificationCode import verification_code_check


# Create your views here.


def inventory_show_all_html(request):
    """返回全部库存"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        inventory_list = Inventory.objects.all().order_by('-inventory_recent_change_time')  # 按最近修改时间的倒序排序
        """筛选不同分组的库存"""
        group_auto_id = request.GET.get('group', '')
        if group_auto_id:
            inventory_list = inventory_list.filter(inventory_group__auto_id=group_auto_id)
        group_list = InventoryGroup.objects.all()
        # page = request.GET.get('page', 1)
        # paginator = Paginator(inventory_list, 6)
        # inventory_display = paginator.get_page(page)
        return render(request, 'PC/inventory/inventoryShowAll.html', {
            'paginator': inventory_list,
            'group_list': group_list,
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
            return render(request, 'PC/inventory/inventoryShowDetail.html', {
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
            group_list = InventoryGroup.objects.all()
            user = User.objects.get(user_id=request.session['user_id'])
            if inventory.inventory_create_user == user.user_id or user.user_identity == 1:
                return render(request, 'PC/inventory/inventoryChangeDetail.html', {
                    'inventory': inventory,
                    'group_list': group_list,
                })
            else:
                return render(request, 'PC/forbidden.html', {
                    'error': '您既不是管理员，该库存也不是您创建的。只有创建者或管理员才有权利更改库存详细信息'
                })
        elif request.method == 'POST':
            inventory_id = request.POST.get('inventory_id')
            inventory = Inventory.objects.get(inventory_id__exact=inventory_id)
            inventory.inventory_name = request.POST['inventory_name']
            # inventory.inventory_category = request.POST['inventory_category']
            inventory.inventory_group = InventoryGroup.objects.get(auto_id=request.POST['inventory_group'])
            inventory.inventory_unit = request.POST['inventory_unit']
            # inventory.inventory_attributes = request.POST['inventory_price']
            # inventory.inventory_details = request.POST['inventory_details']
            # inventory.inventory_value = int(request.POST['inventory_value'])
            # inventory.inventory_package = request.POST['inventory_package']
            inventory.inventory_price = request.POST['inventory_price']
            inventory.inventory_mark = request.POST['inventory_mark']
            inventory.save()
            return HttpResponse('success')
    else:
        return redirect('BPlan:index')


def inventory_group_create_html(request):
    """返回创建新的库存分组的界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        return render(request, 'PC/inventory/inventoryGroupCreate.html')
    else:
        return redirect('BPlan:index')


def inventory_group_create_add(request):
    """创建新的库存分组"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1 and request.method == 'POST':
        name = request.POST['name']
        if InventoryGroup.objects.filter(name=name):
            return HttpResponse('nameExist')
        new_group = InventoryGroup.objects.create(name=name)
        new_group.save()
        return HttpResponse('success')
    else:
        return redirect('BPlan:index')


def inventory_create_html(request):
    """返回创建新的库存的界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        # if whether_mobile(request) is False:
        return render(request, 'PC/inventory/inventoryCreate.html', {
            'group_list': InventoryGroup.objects.all(),
        })
        # else:
        #     return HttpResponse('mobile')
    else:
        return redirect('BPlan:index')


def inventory_create_add(request):
    """创建新的库存"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1 and request.method == 'POST':
        # if verification_code_check(request) is False:
        #     return HttpResponse('codeWrong')
        # inventory_id = request.POST['inventory_id']
        # if Inventory.objects.filter(inventory_id__exact=inventory_id):
        #     return HttpResponse('idExist')
        inventory_name = request.POST['inventory_name']
        # inventory_category = request.POST['inventory_category']
        inventory_group = InventoryGroup.objects.get(auto_id=request.POST['inventory_group'])
        inventory_num = int(request.POST['inventory_num'])
        inventory_unit = request.POST['inventory_unit']
        # inventory_details = request.POST['inventory_details']
        # inventory_value = int(request.POST['inventory_value'])
        # inventory_package = request.POST['inventory_package']
        inventory_price = request.POST['inventory_price']
        inventory_mark = request.POST['inventory_mark']
        inventory_create_user = request.session['user_id']  # 获取创建人的id
        inventory = Inventory.add_inventory(  # 增加库存
            # inventory_id=inventory_id,
            inventory_name=inventory_name,
            # inventory_category=inventory_category,
            inventory_group=inventory_group,
            inventory_num=inventory_num,
            inventory_unit=inventory_unit,
            # inventory_details=inventory_details,
            # inventory_value=inventory_value,
            # inventory_package=inventory_package,
            inventory_price=inventory_price,
            inventory_mark=inventory_mark,
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
        user = User.objects.get(user_id=request.session['user_id'])
        if inventory.inventory_create_user == user.user_id or user.user_identity == 1:
            return render(request, 'PC/inventory/inventoryChange.html', {
                'change_type': change_type,
                'inventory_id': inventory.inventory_id,
                'inventory_name': inventory.inventory_name,
                'inventory_num': inventory.inventory_num,
            })
        else:
            return render(request, 'PC/forbidden.html', {
                'error': '您既不是管理员，该库存也不是您创建的。只有创建者或管理员才有权利出入库'
            })
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
                inventory = []  # 搜索结果的数组
                if search_type == 'all':
                    # inventory = []  # 搜索结果的数组
                    search_split = search.split()  # 把字符串拆分
                    for_count = 0  # 循环次数
                    for search_word in search_split:
                        for_count += 1
                        # if search_word in ['电阻', '电容', '电感']:  # 按分类搜索
                        #     search_word_index = ['电阻', '电容', '电感'].index(search_word)
                        #     inventory_item = Inventory.objects.filter(inventory_category__exact=search_word_index)
                        #     inventory.extend(inventory_item)  # 将搜索结果加入数组
                        #     continue

                        # try:  # 按value搜索
                        #     inventory_item = Inventory.objects.filter(inventory_value=search_word)
                        #     inventory.extend(inventory_item)
                        # except ValueError:
                        #     continue

                        inventory_item = Inventory.objects.filter(
                            # Q(inventory_id__contains=search_word) |
                            Q(inventory_name__contains=search_word)
                            | Q(inventory_group__name__contains=search_word)  # 按库存分组查询
                            # | Q(inventory_value__exact=search_word)
                            # | Q(inventory_package__contains=search_word)
                            | Q(inventory_create_user_name__contains=search_word)
                            | Q(inventory_recent_change_user_name__contains=search_word)
                            | Q(inventory_mark__contains=search_word)
                        )
                        if len(inventory_item):
                            if for_count > 1:
                                inventory = list(set(inventory).intersection(set(inventory_item)))
                            else:
                                inventory.extend(inventory_item)

                        try:  # 搜索数字
                            inventory_item = Inventory.objects.filter(
                                Q(inventory_num=int(float(search_word))) |
                                Q(inventory_price=float(search_word))
                            )
                            # print(float(search_word))
                            # print(Inventory.objects.get(inventory_num=80).inventory_price)
                            if for_count > 1:
                                inventory = list(set(inventory).intersection(set(inventory_item)))
                            else:
                                inventory.extend(inventory_item)
                        except ValueError:
                            continue

                    inventory = list(set(inventory))  # 去掉重复的搜索结果
                # elif search_type == 'inventory_id':
                #     inventory = Inventory.objects.filter(inventory_id__contains=search)
                elif search_type == 'inventory_name':
                    inventory = Inventory.objects.filter(inventory_name__contains=search)
                # elif search_type == 'inventory_value':
                #     inventory = Inventory.objects.filter(inventory_value=search)
                # elif search_type == 'inventory_package':
                #     inventory = Inventory.objects.filter(inventory_package__contains=search)
                elif search_type == 'inventory_num':
                    inventory = Inventory.objects.filter(inventory_num=search)
                elif search_type == 'inventory_price':
                    inventory = Inventory.objects.filter(inventory_price=float(search))
                elif search_type == 'inventory_mark':
                    inventory = Inventory.objects.filter(inventory_mark__contains=search)
                elif search_type == 'inventory_create_user_name':
                    if search == '我':
                        inventory = Inventory.objects.filter(inventory_create_user=request.session['user_id'])
                    else:
                        inventory = Inventory.objects.filter(inventory_create_user_name__contains=search)
                elif search_type == 'inventory_recent_change_user_name':
                    inventory = Inventory.objects.filter(inventory_recent_change_user_name__contains=search)
                # elif inventory.exists() is False:
                #     inventory = ''
                if len(inventory) == 0:
                    inventory = ''
            else:
                inventory = 'noSearch'
            return render(request, 'PC/inventory/inventorySearch.html', {
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
        user_id = request.session.get('user_id')
        if request.GET.get('type', 0) == 'inventory':
            user = User.objects.get(user_id__exact=user_id)
            inventory_id = request.GET.get('id')
            inventory = Inventory.objects.get(inventory_id=inventory_id)
            if user.user_identity == 1 or inventory.inventory_create_user == user_id:
                # return render(request, 'PC/forbidden.html', {
                #     'error': '您不是管理员，只有管理员可以查看操作记录'
                # })
                # inventory_id = request.GET.get('id')
                inventory_operation = InventoryOperation.objects.filter(inventory_operation_object=inventory).order_by(
                    '-inventory_operation_create_time'
                )
            else:
                return render(request, 'PC/forbidden.html', {
                    'error': '您既不是管理员，该库存也不是您创建的。只有创建者或管理员才有权利查看这个库存的操作记录'
                })
        else:
            # user_id = request.session.get('user_id')
            inventory_operation = InventoryOperation.objects.filter(
                inventory_operation_user=user_id
            ).order_by('-inventory_operation_create_time')
        # else:
        #     return render(request, 'PC/inventory/inventoryOperationSearch.html')
        if inventory_operation:
            return render(request, 'PC/inventory/inventoryOperationShow.html', {'paginator': inventory_operation})
        else:
            return render(request, 'PC/inventory/inventoryOperationShow.html', {
                'paginator': ''
            })
    else:
        return redirect('BPlan:index')


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

        return render(request, 'PC/inventory/inventoryOperationChart.html', {
            'time_label': time_label,
            'in_num': in_num,
            'out_num': out_num,
            'create_num': create_num,
        })
    else:
        return redirect('BPlan:index')
