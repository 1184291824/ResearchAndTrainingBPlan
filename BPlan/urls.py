from django.urls import path
from . import views

app_name = "BPlan"


urlpatterns = [
    path('test/', views.test, name="test"),
    path('login/', views.login_html, name='login_html'),
    path('login_check/', views.login_check, name='login_check')

]
