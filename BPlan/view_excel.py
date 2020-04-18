# coding=utf8
"""
创建者：马子轩
贡献者：
创建时间: 2020年04月15日
最后保存时间: 2020年04月15日
"""
from django.shortcuts import render, HttpResponse, redirect
from django.utils.http import urlquote
from .models import *
from io import BytesIO  # 输出excel时往内存里存东西
import xlwt
import pandas as pd

# 库存题头
INVENTORY_TITLE = [
    '库存ID', '库存分组', '库存名称', '数量', '单位',
    '规格', '创建人', '创建时间', '最近领用人', '最近修改时间', '备注',
]

# 库存字段
INVENTORY_FIELD = [
    'inventory_id', 'inventory_group__name', 'inventory_name', 'inventory_num',
    'inventory_unit', 'inventory_specification', 'inventory_create_user__user_name',
    'inventory_create_time', 'inventory_recent_change_user__user_name',
    'inventory_recent_change_time', 'inventory_mark',
]

# 库存操作记录题头
INVENTORY_OPERATION_TITLE = [
    '操作ID', '领用人', '库存', '操作类别', '操作数量', '库存余量',
    '操作时间', '操作者ip', '浏览器', '操作系统', '设备'
]

# 库存操作记录字段
INVENTORY_OPERATION_FIELD = [
    'pk', 'inventory_operation_user__user_name',
    'inventory_operation_object__inventory_name', 'inventory_operation_category',
    'inventory_operation_num', 'inventory_num', 'inventory_operation_create_time',
    'inventory_operation_user_ip', 'inventory_operation_user_browser',
    'inventory_operation_user_system', 'inventory_operation_user_device',
]

# 客户信息题头
CUSTOMER_TITLE = [
    '客户ID', '客户名称', '项目名称', '项目签订时间', '业务填写人',
    '联系人', '联系方式', '项目金额', '付款方式', '项目技术要求或主要条款'
]

# 客户信息字段
CUSTOMER_FIELD = [
    'pk', 'name', 'project_name', 'project_date', 'user_id__user_name',
    'contact', 'tel', 'project_amount', 'payment_method', 'mark',
]

# 登录记录题头
LOGIN_RECORD_TITLE = [
    '登录记录ID', '用户', '登录时间', 'IP', '浏览器', '操作系统', '设备'
]

# 登录记录字段
LOGIN_RECORD_FIELD = [
    'pk', 'login_user__user_name', 'login_time', 'login_ip',
    'login_browser', 'login_system', 'login_device',
]


def test(request):
    pass
    # inventory = Inventory.objects.all()
    # inventory_list = list(inventory.values_list(
    #     'inventory_id',
    #     'inventory_group__name',
    #     'inventory_name',
    #     'inventory_num',
    #     'inventory_unit',
    #     'inventory_specification',
    #     'inventory_create_user__user_name',
    #     'inventory_create_time',
    #     'inventory_recent_change_user__user_name',
    #     'inventory_recent_change_time',
    #     'inventory_mark',
    # ))
    # data = pd.DataFrame(inventory_list, columns=INVENTORY_TITLE)
    # # 修改时间格式
    # data['创建时间'] = data['创建时间'].dt.date
    # data['最近修改时间'] = data['最近修改时间'].dt.date
    # return get_response(data, u"全部库存信息")


def get_response(data, filename):
    """
    获得输出应答
    :param data: 数据，pandas.DataFrame对象
    :param filename: 文件名称
    :return: response
    """
    # 创建输出流对象
    output = BytesIO()
    # 将数据写入输出流
    data.to_excel(output, index=False)
    # 重新定位到开始
    output.seek(0)
    # 创建返回应答
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  # 这是xlsx的content_type
    response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(urlquote(filename))  # urlquote是为了兼容中文名称
    # 写入应答数据
    response.write(output.getvalue())
    return response


def inventory_excel(request):
    """库存转excel"""
    pk_list = request.session['excel_list']  # 获取id列表
    inventory = Inventory.objects.filter(inventory_id__in=pk_list)  # 获得库存
    inventory_list = list(inventory.values_list(*INVENTORY_FIELD))  # 将内容提取
    # 转为df对象
    data = pd.DataFrame(inventory_list, columns=INVENTORY_TITLE)
    # 修改时间格式
    data['创建时间'] = data['创建时间'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    data['最近修改时间'] = data['最近修改时间'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    return get_response(data, u"库存信息")


def inventory_operation_excel(request):
    """库存记录转excel"""
    pk_list = request.session['excel_list']  # 获取id列表
    inventory_operation = InventoryOperation.objects.filter(pk__in=pk_list)  # 获得库存操作记录
    inventory_operation_list = list(
        inventory_operation.values_list(*INVENTORY_OPERATION_FIELD)
    )  # 将内容提取
    # 转为df对象
    data = pd.DataFrame(inventory_operation_list, columns=INVENTORY_OPERATION_TITLE)
    # 修改时间格式
    data['操作时间'] = data['操作时间'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    # 修改操作类型
    data['操作类别'].replace({0: '入库', 1: '出库', 2: '创建'}, inplace=True)

    return get_response(data, u"库存“{}”的操作记录".format(inventory_operation[0].inventory_operation_object.inventory_name))


def customer_excel(request):
    """客户信息转excel"""
    pk_list = request.session['excel_list']  # 获取id列表
    customer = Customer.objects.filter(pk__in=pk_list)  # 获得客户信息
    customer_list = list(customer.values_list(*CUSTOMER_FIELD))  # 将信息转为列表

    # 转为df对象
    data = pd.DataFrame(customer_list, columns=CUSTOMER_TITLE)
    # 修改时间格式
    # data['项目签订时间'] = data['项目签订时间'].dt.strftime('%Y-%m-%d').tolist()

    return get_response(data, u"客户信息")


def login_record_excel(request):
    """登录记录转excel"""
    pk_list = request.session['excel_list']  # 获取id列表
    login_record = LoginRecord.objects.filter(pk__in=pk_list)  # 获取登录信息
    login_record_list = list(login_record.values_list(*LOGIN_RECORD_FIELD))  # 将信息转为列表

    # 转为df对象
    data = pd.DataFrame(login_record_list, columns=LOGIN_RECORD_TITLE)

    # 修改时间格式
    data['登录时间'] = data['登录时间'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()

    return get_response(data, u"用户“{}”的登录记录".format(login_record[0].login_user.user_name))



