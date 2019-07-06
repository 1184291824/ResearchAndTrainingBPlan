from django.urls import path
from . import views, VerificationCode

app_name = "BPlan"


urlpatterns = [
    path('test/', views.test, name="test"),

    path('index/whetherLogin', views.whether_login, name='whether_login'),
    path('index/', views.index, name='index'),
    path('login/', views.login_html, name='login_html'),
    path('login/loginCheck/', views.login_check, name='login_check'),
    path('login/logout', views.login_logout, name='login_logout'),
    path('register/', views.register_html, name='register_html'),
    path('register/check', views.register_check, name='register_check'),
    # path('register/more/', views.register_html_more, name='register_html_more'),
    # path('register/more/check', views.register_check_more, name='register_check_more'),
    path('change/password/', views.change_password_html, name='change_password_html'),
    path('change/password/check', views.change_password_check, name='change_password_check'),
    path('change/question', views.change_question_html, name='change_question_html'),
    path('change/question/check', views.change_question_check, name='change_question_check'),

    path('inventory/show/all/', views.inventory_show_all_html, name='inventory_show_all_html'),
    path('inventory/show/detail/', views.inventory_show_detail_html, name='inventory_show_detail_html'),
    path('inventory/create/', views.inventory_create_html, name='inventory_create_html'),
    path('inventory/create/add/', views.inventory_create_add, name='inventory_create_add'),
    path('inventory/change/', views.inventory_change_html, name='inventory_change_html'),
    path('inventory/change/add', views.inventory_change_add, name='inventory_change_add'),
    path('inventory/operation/inventory/', views.inventory_operation_html_inventory, name='inventory_operation_html_inventory'),
    path('inventory/operation/user/', views.inventory_operation_html_user, name='inventory_operation_html_user'),
    path('inventory/operation/user/check/', views.inventory_operation_check_user, name='inventory_operation_check_user'),
    path('verificationCode/get', VerificationCode.verification_code, name='getVerificationCode'),


]
