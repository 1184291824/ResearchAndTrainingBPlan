from django.shortcuts import render, HttpResponse, redirect
# from .models import MarkdownFile
# import datetime
# from .request import *
# import codecs
# import markdown
# from ResearchAndTrainingBPlan.settings import PythonAnywhere
from django.core.paginator import Paginator


# Create your views here.


def test(request):
    return render(request, 'PC/forbidden.html', {
        'error': '该客户信息不是您创建的，只有创建者有权利添加项目跟踪记录'
    })


# def whether_login(request):
#     """判断是否处于登录状态"""
#     login_status = request.session.get('login_status', 0)
#     user_id = request.session.get('user_id', 0)
#     user_name = request.session.get('user_name', 0)
#     result = {
#         'login_status': login_status,
#         'user_id': user_id,
#         'user_name': user_name,
#     }
#     return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def index(request):
    """主页"""
    login_status = request.session.get('login_status', 0)
    if login_status == 0:
        return redirect('BPlan:login')
    else:
        return render(request, 'PC/index.html')


def get_paginator(iterator_object, page_num):
    """获取分页器及其内容"""
    paginator = Paginator(iterator_object, 30)
    page = paginator.get_page(page_num)
    return paginator, page


# def login_record_ask_html(request):
#     """返回网站访问量统计界面"""
#     today = datetime.date.today()
#     base_record = LoginRecord.objects.filter(
#         login_user__user_id__exact='9161040G0000'
#     )  # 访问量查询集
#
#     '''获取每日访问量'''
#     ask_record_display = []  # 每日访问量的数组
#     time_label = []  # 存放日期的数组
#     if whether_mobile(request):
#         day_range = 5  # 日期的显示范围，如果是移动设备，仅显示5天
#     else:
#         day_range = 10
#     for i in range(0, day_range):
#         date_num = today - datetime.timedelta(days=i)
#         ask_record_display.append(base_record.filter(login_date=date_num).count())
#         time_label.append(date_num)
#
#     '''获取访问系统占比'''
#     windows_num = base_record.filter(login_system__icontains='windows').count()
#     ios_num = base_record.filter(login_system__icontains='iOS').count()
#     android_num = base_record.filter(login_system__icontains='Android').count()
#
#     # '''获取访问的地理位置占比'''
#     # location_num = [
#     #     base_record.filter(login_location__contains='上海').count(),
#     #     base_record.filter(login_location__contains='江苏').count(),
#     #     base_record.filter(login_location__contains='浙江').count(),
#     #     base_record.filter(login_location__contains='广东').count(),
#     #     base_record.filter(login_location__contains='河北').count(),
#     #     base_record.filter(login_location__contains='陕西').count(),
#     #     base_record.filter(login_location__contains='未知').count(),
#     # ]
#     # other_location_num = base_record.count() - sum(location_num)
#     # location_num.append(other_location_num)
#     return render(request, 'PC/askRecord.html', {
#         'ask_record_display': ask_record_display,  # 每日的访问记录
#         'time_label': time_label,  # 横轴，日期
#         'wholeCount': base_record.count(),  # 总访问量
#         'system_num': [android_num, windows_num, ios_num],  # 访问系统分类
#         # 'location_num': location_num,  # 访问地址分类
#     })


# def markdown_html(request):
#     """返回操作手册界面"""
#     if request.session.get('login_status', 0):
#         # 获取markdown文件名
#         file_name = request.GET.get('file', '操作手册')
#         # if file_name == 'README':
#         #     title = '操作手册'
#         # else:
#         #     title = file_name
#
#         # 读取 markdown 文本
#         # input_file = codecs.open('md/'+file_name+".md", mode="r", encoding="utf-8")
#         input_file = MarkdownFile.objects.get(name=file_name)
#         # print(input_file.file.name)
#         text = input_file.file.read().decode()  # 读取文件并解码
#         # print(text)

    #     # 转为 html 文本
    #     html = markdown.markdown(text)
    #
    #     # 输出html文本
    #     return render(request, 'PC/markdown.html', {
    #         'markdown_html': html,
    #         'title': file_name,
    #     })
    #     # return HttpResponse(text)
    # else:
    #     return redirect('BPlan:index')
