from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from .models import Customer, CustomerTracking, User
from io import BytesIO  # 输出excel时往内存里存东西
import xlwt
# from django.contrib.auth import logout
# from django.core.paginator import Paginator
# import datetime
# from .request import *


# Create your views here.


def customer_show_all_html(request):
    """返回全部客户信息"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        customer_list = Customer.objects.all().order_by('-id')  # 按最近修改时间的倒序排序
        return render(request, 'PC/customer/customerShowAll.html', {
            'paginator': customer_list,
        })
    else:
        return redirect('BPlan:index')


def customer_show_detail_html(request):
    """返回某客户的详细信息"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        customer_id = request.GET.get('id')
        try:
            customer = Customer.objects.get(id=customer_id)
            tracking = CustomerTracking.objects.filter(customer=customer)
            user = User.objects.get(user_id=customer.user_id)
            return render(request, 'PC/customer/customerShowDetail.html', {
                'customer': customer,
                'tracking': tracking,
                'user': user,
            })
        except Customer.DoesNotExist:
            return redirect('BPlan:customer_show_all_html')
    else:
        return redirect('BPlan:index')


def customer_change_detail(request):
    """改变客户的详细信息"""
    if request.session.get('login_status', 0):
        if request.method == 'GET':
            customer_id = request.GET.get('id')
            customer = Customer.objects.get(id=customer_id)
            user = User.objects.get(user_id=request.session['user_id'])
            if customer.user_id == user.user_id or user.user_identity == 1:
                return render(request, 'PC/customer/customerChangeDetail.html', {
                    'customer': customer,
                })
            else:
                return render(request, 'PC/forbidden.html', {
                    'error': '您既不是管理员，该客户信息也不是您创建的。只有创建者或管理员才有权利更改客户信息'
                })
        elif request.method == 'POST':
            customer_id = request.POST.get('id')
            customer = Customer.objects.get(id=customer_id)
            customer.name = request.POST['name']
            # print(request.POST['name'])
            # print(customer.name)
            customer.contact = request.POST['contact']
            customer.tel = request.POST['tel']
            customer.project_name = request.POST['project_name']
            # project_date = request.POST['project_date'],
            customer.project_amount = request.POST['project_amount']
            customer.payment_method = request.POST['payment_method']
            customer.mark = request.POST['mark']
            # customer.name = request.POST['inventory_name']
            # # customer.inventory_category = request.POST['inventory_category']
            # customer.inventory_unit = request.POST['inventory_unit']
            # customer.inventory_attributes = request.POST['inventory_price']
            # # customer.inventory_details = request.POST['inventory_details']
            # # customer.inventory_value = int(request.POST['inventory_value'])
            # # customer.inventory_package = request.POST['inventory_package']
            # customer.inventory_mark = request.POST['inventory_mark']
            customer.save()
            return HttpResponse('success')
    else:
        return redirect('BPlan:index')


def customer_create_html(request):
    """返回创建客户信息界面"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        return render(request, 'PC/customer/customerCreate.html')
    else:
        return redirect('BPlan:index')


def customer_create_add(request):
    """创建客户信息"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1 and request.method == 'POST':
        new_customer = Customer.objects.create(
            user_id=request.session['user_id'],
            name=request.POST['name'],
            contact=request.POST['contact'],
            tel=request.POST['tel'],
            project_name=request.POST['project_name'],
            project_date=request.POST['project_date'],
            project_amount=request.POST['project_amount'],
            payment_method=request.POST['payment_method'],
            mark=request.POST['mark'],
        )
        new_customer.save()
        return HttpResponse('success')
    else:
        return redirect('BPlan:index')


def customer_tracking(request):
    """添加项目跟踪"""
    login_status = request.session.get('login_status', 0)
    if login_status == 1:
        if request.method == 'GET':
            customer_id = request.GET.get('id', 0)
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                return redirect('BPlan:customer_show_all_html')
            user_id = request.session['user_id']
            user = User.objects.get(user_id=user_id)
            if customer.user_id == user_id or user.user_identity == 1:
                return render(request, 'PC/customer/customerTracking.html', {
                    'name': customer.name,
                    'id': customer.id,
                })
            else:
                return render(request, 'PC/forbidden.html', {
                    'error': '您既不是管理员，该客户信息也不是您创建的。只有创建者或管理员才有权利添加项目跟踪记录'
                })
        elif request.method == 'POST':
            customer_id = request.POST['id']
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                return redirect('BPlan:customer_show_all_html')
            tracking = CustomerTracking.objects.create(
                customer=customer,
                track_date=request.POST['track_date'],
                track_state=request.POST['track_state'],
            )
            tracking.save()
            return HttpResponse('success')
    else:
        return redirect('BPlan:index')


def customer_search(request):
    """查询客户"""
    if request.session.get('login_status', 0):
        if request.method == 'GET':
            search_type = request.GET.get('search_type', '')
            search = request.GET.get('search', '')
            if search_type and search:
                customer = []  # 搜索结果的数组
                if search_type == 'all':
                    search_split = search.split()  # 把字符串拆分
                    for_count = 0  # 循环次数
                    for search_word in search_split:
                        for_count += 1
                        customer_item = Customer.objects.filter(
                            Q(name__contains=search_word)
                            | Q(contact__contains=search_word)
                            | Q(tel=search_word)
                            | Q(project_name__contains=search_word)
                            | Q(project_amount__contains=search_word)
                            | Q(payment_method__contains=search_word)
                            | Q(mark__contains=search_word)
                        )
                        if len(customer_item):
                            if for_count > 1:
                                customer = list(set(customer).intersection(set(customer_item)))
                            else:
                                customer.extend(customer_item)

                    customer = list(set(customer))  # 去掉重复的搜索结果
                elif search_type == 'user':
                    if search == '我':
                        customer = Customer.objects.filter(user_id=request.session['user_id'])
                    else:
                        try:
                            user = User.objects.get(user_name=search)
                            customer = Customer.objects.filter(user_id=user.user_id)
                        except User.DoesNotExist:
                            customer = []
                elif search_type == 'name':
                    customer = Customer.objects.filter(name__contains=search)
                elif search_type == 'contact':
                    customer = Customer.objects.filter(contact__contains=search)
                elif search_type == 'tel':
                    customer = Customer.objects.filter(tel=search)
                elif search_type == 'project_name':
                    customer = Customer.objects.filter(project_name__contains=search)
                elif search_type == 'project_amount':
                    customer = Customer.objects.filter(project_amount__contains=search)
                elif search_type == 'payment_method':
                    customer = Customer.objects.filter(payment_method__contains=search)
                elif search_type == 'mark':
                    customer = Customer.objects.filter(mark__contains=search)
                if len(customer) == 0:
                    customer = ''
            else:
                customer = 'noSearch'
            return render(request, 'PC/customer/customerSearch.html', {
                'paginator': customer,
                'search_type': search_type,
                'search': search,
            })
    else:
        return redirect('BPlan:index')


def customer_excel(request):
    """将用户信息导出excel"""
    # 获取数据
    customer_id = request.GET['id']
    customer = Customer.objects.get(id=customer_id)
    user = User.objects.get(user_id=customer.user_id)
    tracking_list = CustomerTracking.objects.filter(customer=customer)
    foo = 0
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename='+customer.name+'.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')

    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name 宋体,
                height 0xF0;
            align:
                wrap off,
                vert center,
                horiz center;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)

    # 写入数据
    sheet.write_merge(0, 0, 0, 3, '锐达思普/中安锐达南京分公司客户信息跟踪表', style_heading)
    sheet.write(1, 3, '业务填写人：'+user.user_name, style_heading)
    sheet.write(2, 0, '客户名称', style_heading)
    sheet.write_merge(2, 2, 1, 3, customer.name, style_heading)
    sheet.write(3, 0, '联系人', style_heading)
    sheet.write(3, 1, customer.contact, style_heading)
    sheet.write(3, 2, '联系方式', style_heading)
    sheet.write(3, 3, customer.tel, style_heading)
    sheet.write(4, 0, '项目名称', style_heading)
    sheet.write_merge(4, 4, 1, 3, customer.project_name, style_heading)
    sheet.write(5, 0, '项目签订时间', style_heading)
    sheet.write(5, 1, customer.project_date.strftime('%Y-%m-%d'), style_heading)
    sheet.write(5, 2, '项目金额', style_heading)
    sheet.write(5, 3, customer.project_amount, style_heading)
    sheet.write(6, 0, '付款方式', style_heading)
    sheet.write_merge(6, 6, 1, 3, customer.payment_method, style_heading)
    sheet.write_merge(7, len(tracking_list)+7, 0, 1, customer.mark, style_heading)
    sheet.write(7, 2, '跟踪记录时间', style_heading)
    sheet.write(7, 3, '项目跟踪状态', style_heading)
    for track in tracking_list:
        sheet.write(8+foo, 2, track.track_date.strftime('%Y-%m-%d'), style_heading)
        sheet.write(8+foo, 3, track.track_state, style_heading)
        foo += 1

    # 调整格式
    sheet.col(0).width = 5000  # 3333 = 1" (one inch).
    sheet.col(1).width = 8000  # 3333 = 1" (one inch).
    sheet.col(2).width = 5000  # 3333 = 1" (one inch).
    sheet.col(3).width = 8000  # 3333 = 1" (one inch).
    for i in range(len(tracking_list)+8):
        sheet.row(i).height_mismatch = True
        sheet.row(i).height = 600  # 3000对应150

    # # 写入数据
    # data_row = 1
    # # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    # for i in UserTable.objects.all():
    #     # 格式化datetime
    #     pri_time = i.pri_date.strftime('%Y-%m-%d')
    #     oper_time = i.operating_time.strftime('%Y-%m-%d')
    #     sheet.write(data_row, 0, i.loan_id)
    #     sheet.write(data_row, 1, i.name)
    #     sheet.write(data_row, 2, i.user_phone)
    #     sheet.write(data_row, 3, i.user_card)
    #     sheet.write(data_row, 4, pri_time)
    #     sheet.write(data_row, 5, i.emp.emp_name)
    #     sheet.write(data_row, 6, i.statu.statu_name)
    #     sheet.write(data_row, 7, oper_time)
    #     data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response

