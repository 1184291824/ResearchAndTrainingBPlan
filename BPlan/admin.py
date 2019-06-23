from django.contrib import admin

# Register your models here.

from .models import *


admin.site.site_header = '库存管理系统后台'  # 网站登录页和H1
admin.site.site_title = '库存管理系统后台'   # 网站标题


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user_id',
        'user_password',
        'user_group',
        'user_name',
        'user_gender',
        'user_identity',
        'user_question',
        'user_question_answer',
        'user_create_time',
    ]
    search_fields = ['user_id', 'user_name']  # 搜索字段


@admin.register(Group)
class ClassesAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'group_id',
        'group_name',
    ]

    search_fields = ['group_id', 'group_name']  # 搜索字段
