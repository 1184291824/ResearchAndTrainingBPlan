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
        # 'user_group',
        'user_name',
        'user_gender',
        'user_identity',
        # 'user_question',
        # 'user_question_answer',
        'user_create_time',
    ]
    search_fields = ['user_id', 'user_name']  # 搜索字段
    list_per_page = 20


# class UserInfo(admin.TabularInline):
#     """预添加1个用户"""
#     model = User
#     extra = 1


# @admin.register(Group)
# class ClassesAdmin(admin.ModelAdmin):
#     list_display = [
#         'pk',
#         'group_id',
#         'group_name',
#         'group_create_time',
#     ]
#
#     search_fields = ['group_id', 'group_name']  # 搜索字段
#     date_hierarchy = 'group_create_time'  # 按创建的时间分层筛选
#     inlines = [UserInfo]  # 在创建组时预添加用户
#     list_per_page = 20


class InventoryOperationInfo(admin.TabularInline):
    """在添加库存时预添加一条记录"""
    model = InventoryOperation
    extra = 1


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'inventory_id',
        'inventory_name',
        'inventory_group',
        'inventory_num',
        'inventory_unit',
        # 'inventory_details',
        # 'inventory_value',
        # 'inventory_package',
        'inventory_specification',
        'inventory_mark',
        'inventory_create_user',
        'inventory_create_time',
        'inventory_recent_change_user',
        'inventory_recent_change_time',
    ]
    search_fields = ['inventory_id', 'inventory_name']  # 搜索字段
    list_filter = (
        'inventory_group',
    )  # 筛选器
    date_hierarchy = 'inventory_create_time'  # 详细时间分层筛选
    inlines = [InventoryOperationInfo]  # 在添加库存时预添加一条记录
    list_per_page = 20


@admin.register(InventoryOperation)
class InventoryOperationAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'inventory_operation_create_time',
        'inventory_operation_object',
        'inventory_operation_user',
        # 'inventory_operation_user_name',
        'inventory_operation_user_ip',
        'inventory_operation_category',
        'inventory_operation_num',
        'inventory_operation_user_browser',
        'inventory_operation_user_system',
        'inventory_operation_user_device',
        # 'inventory_operation_review_user',
        # 'inventory_operation_review_user_ip',
        # 'inventory_operation_review_opinion',
        # 'inventory_operation_review_time',
        'inventory_num',
    ]
    search_fields = ['inventory_operation_user', 'inventory_operation_user_name']  # 搜索字段
    list_filter = (
        'inventory_operation_object',
        'inventory_operation_category',
        'inventory_operation_num',
        # 'inventory_operation_review_opinion',
    )  # 筛选器
    date_hierarchy = 'inventory_operation_create_time'  # 详细时间分层筛选
    list_per_page = 20


@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'login_user',
        'login_ip',
        'login_browser',
        'login_system',
        'login_device',
        # 'login_location',
        'login_time',
    ]
    list_filter = ['login_user']  # 筛选器
    date_hierarchy = 'login_time'  # 详细时间分层筛选
    list_per_page = 20


@admin.register(InventoryGroup)
class InventoryGroupAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'auto_id',
        'name',
        # 'attributes_name',
        # 'attributes_num',
    ]

    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user_id',
        'name',
        'contact',
        'tel',
        'project_name',
        'project_date',
        'project_amount',
        'payment_method',
        'mark',
    ]
    search_fields = ['name', 'project_name']
    list_per_page = 20


@admin.register(CustomerTracking)
class CustomerTrackingAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'customer',
        'track_date',
        'track_state',
    ]
    search_fields = ['customer']
    list_per_page = 20


# @admin.register(MarkdownFile)
# class MarkdownFileAdmin(admin.ModelAdmin):
#     list_display = [
#         'pk',
#         'name',
#         'file',
#     ]
#     search_fields = ['name']
