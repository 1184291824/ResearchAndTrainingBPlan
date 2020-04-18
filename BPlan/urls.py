from django.urls import path
from . import view_common, view_user, views_inventory, view_customer, view_excel

app_name = "BPlan"


urlpatterns = [
    path('test/', view_excel.test, name="test"),

    # path('index/whetherLogin/', view_common.whether_login, name='whether_login'),
    path('index/', view_common.index, name='index'),
    # path('markdown/', view_common.markdown_html, name='markdown'),

    path('login/', view_user.login_html, name='login'),
    # path('login/loginCheck/', view_user.login_check, name='login_check'),
    path('login/logout/', view_user.login_logout, name='login_logout'),
    path('login/record/', view_user.login_record_html, name='login_record_html'),
    # path('login/record/ask/', view_user.login_record_ask_html, name='login_record_ask_html'),
    # path('register/', view_user.register_html, name='register_html'),
    # path('register/check/', view_user.register_check, name='register_check'),
    # path('change/password/', view_user.change_password_html, name='change_password_html'),
    # path('change/password/check/', view_user.change_password_check, name='change_password_check'),
    # path('change/question/', view_user.change_question_html, name='change_question_html'),
    # path('change/question/check/', view_user.change_question_check, name='change_question_check'),
    # path('change/personalInformation/', view_user.change_personal_information, name='change_personal_information'),

    path('inventory/show/all/', views_inventory.inventory_show_all_html, name='inventory_show_all_html'),
    path('inventory/show/detail/', views_inventory.inventory_show_detail_html, name='inventory_show_detail_html'),
    path('inventory/create/', views_inventory.inventory_create, name='inventory_create_html'),
    # path('inventory/create/add/', views_inventory.inventory_create_add, name='inventory_create_add'),
    path('inventory/change/', views_inventory.inventory_change, name='inventory_change_html'),
    # path('inventory/change/add/', views_inventory.inventory_change_add, name='inventory_change_add'),
    path('inventory/change/detail/', views_inventory.inventory_change_detail, name='inventory_change_detail'),
    path('inventory/search/', views_inventory.inventory_search, name='inventory_search'),
    path('inventory/operation/', views_inventory.inventory_operation_html, name='inventory_operation_html'),
    path('inventory/operation/chart/', views_inventory.inventory_operation_chart_html, name='inventory_operation_chart_html'),
    path('inventory/group/create/', views_inventory.inventory_group_create, name='inventory_group_create_html'),
    # path('inventory/group/create/add/', views_inventory.inventory_group_create_add, name='inventory_group_create_add'),

    path('customer/show/all/', view_customer.customer_show_all_html, name='customer_show_all_html'),
    path('customer/show/detail/', view_customer.customer_show_detail_html, name='customer_show_detail_html'),
    path('customer/search/', view_customer.customer_search, name='customer_search'),
    path('customer/create/', view_customer.customer_create_html, name='customer_create_html'),
    # path('customer/create/add/', view_customer.customer_create_add, name='customer_create_add'),
    path('customer/tracking/', view_customer.customer_tracking, name='customer_tracking'),
    path('customer/change/detail/', view_customer.customer_change_detail, name='customer_change_detail'),
    path('customer/excel/', view_customer.customer_excel, name='customer_excel'),

    path('excel/inventory/', view_excel.inventory_excel, name='excel_inventory'),
    path('excel/inventory_operation/', view_excel.inventory_operation_excel, name='excel_inventory_operation'),
    path('excel/customer/', view_excel.customer_excel, name='excel_customer'),  # 导出全部客户信息
    path('excel/login_record', view_excel.login_record_excel, name='excel_login_record'),

    # path('verificationCode/get/', VerificationCode.verification_code, name='getVerificationCode'),

    # WXApi URL:
    # path('wx/login/', WXApi.wx_login_check, name='wx_login_check'),
    # path('wx/logout/', WXApi.wx_logout, name='wx_logout'),
]
