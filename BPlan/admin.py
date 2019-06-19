from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'user_id',
        'user_name',
        'user_gender',
        'user_password_encrypted',
    ]
    search_fields = ['user_name']  # 搜索字段


@admin.register(Group)
class ClassesAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'group_id',
        'group_name',
    ]

    search_fields = ['group_id', 'group_name']  # 搜索字段
