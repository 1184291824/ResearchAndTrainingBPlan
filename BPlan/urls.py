from django.urls import path
from . import views

app_name = "BPlan"


urlpatterns = [
    path('test/', views.test, name="test"),
    path('login/', views.login_html, name='login_html'),
    path('login/login_check/', views.login_check, name='login_check'),
    path('register/base/', views.register_html_base, name='register_html_base'),
    path('register/base/check', views.register_check_base, name='register_check_base'),
    path('register/more/', views.register_html_more, name='register_html_more'),
    path('register/more/check', views.register_check_more, name='register_check_more'),


]
