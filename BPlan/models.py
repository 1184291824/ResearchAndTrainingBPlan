from django.db import models


# class Group(models.Model):
#     """组"""
#     group_id = models.CharField(verbose_name='组编号', max_length=12)
#     group_name = models.CharField(verbose_name='组名称', max_length=12)
#     group_create_time = models.DateTimeField(auto_now_add=True, verbose_name='组创建时间')
#
#     def __str__(self):
#         return self.group_name
#
#     class Meta:
#         db_table = "Groups"
#         ordering = ['id']  # 以id为标准升序
#         verbose_name_plural = '分组'


class User(models.Model):
    """用户"""
    '''选项'''
    USER_GENDER_CHOICE = (  # 性别选项
        (True, '男'),
        (False, '女'),
    )
    USER_IDENTITY_CHOICE = (  # 身份选项
        (0, '普通职员'),
        (1, '管理员'),
    )
    # USER_QUESTION_CHOICE = (  # 密保问题选项
    #     (0, '我最喜欢的颜色'),
    #     (1, '我的家乡'),
    #     (2, '我的出生年月（如2000.3.1）'),
    #     (3, '我的小学班主任是'),
    #     (4, '我的初中班主任是'),
    #     (5, '我的高中班主任是'),
    #     (6, '我配偶的姓名'),
    #     (7, '我的大学辅导员是'),
    #     (8, '我父亲的名字'),
    #     (9, '我母亲的名字'),
    #     (10, '我大学里最好的朋友是'),
    #     (11, '我最想去的地方'),
    #     (12, '我的科研训练导师是'),
    # )

    '''基础信息'''
    user_id = models.CharField(verbose_name='用户id', max_length=12)
    user_password = models.CharField(max_length=20, verbose_name='密码')
    # user_group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='所属组')

    '''需要完善的信息'''
    user_name = models.CharField(max_length=12, default='保密', verbose_name='姓名')
    user_gender = models.BooleanField(
        default=True,
        choices=USER_GENDER_CHOICE,
        verbose_name='性别'
    )  # true 代表男性，false 代表女性
    user_identity = models.PositiveSmallIntegerField(
        default=0,
        choices=USER_IDENTITY_CHOICE,
        verbose_name='身份与权限'
    )  # 0:职员，1:管理员
    # user_question = models.PositiveSmallIntegerField(
    #     choices=USER_QUESTION_CHOICE,
    #     default=0,
    #     verbose_name='密保问题'
    # )  # 密保问题
    # user_question_answer = models.CharField(default='', max_length=20, verbose_name='密保问题答案')  # 密保问题答案
    user_create_time = models.DateTimeField(auto_now_add=True, verbose_name='用户注册时间')

    # @classmethod
    # def add_user(cls, user_id, user_password):
    #     """用于增加一个用户"""
    #     user = cls(user_id=user_id, user_password=user_password)
    #     return user

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = "User"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '用户'


class Customer(models.Model):
    """客户信息"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='业务填写人')
    # user_id = models.CharField(max_length=12, verbose_name='业务填写人id')
    name = models.CharField(max_length=50, verbose_name='客户名称')
    contact = models.CharField(max_length=20, verbose_name='联系人')
    tel = models.CharField(max_length=20, verbose_name='联系方式')
    project_name = models.CharField(max_length=50, verbose_name='项目名称')
    project_date = models.DateField(verbose_name='项目签订时间')
    project_amount = models.CharField(max_length=20, verbose_name='项目金额')
    payment_method = models.CharField(max_length=20, verbose_name='付款方式')
    mark = models.TextField(max_length=1000, verbose_name='项目技术要求或主要条款', default='无')

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'Customer'
        ordering = ['id']
        verbose_name_plural = '客户信息'


class InventoryGroup(models.Model):
    """库存的组"""
    auto_id = models.BigAutoField(primary_key=True, verbose_name='组编号')
    name = models.CharField(max_length=20, verbose_name='组名称')
    # attributes_name = models.CharField(max_length=50, verbose_name='属性的字段名称')  # 以“,”分割
    # attributes_num = models.PositiveSmallIntegerField(verbose_name='属性数量')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "InventoryGroup"
        ordering = ['auto_id']  # 以id为标准升序
        verbose_name_plural = '库存的组'


class Inventory(models.Model):
    """库存"""
    # """选项"""
    # INVENTORY_CATEGORY_CHOICE = (  # 库存类别选项
    #     (0, '电阻'),
    #     (1, '电容'),
    #     (2, '电感'),
    # )

    inventory_id = models.BigAutoField(max_length=12, verbose_name='编号', primary_key=True)
    inventory_name = models.CharField(max_length=20, verbose_name='名称')
    # inventory_category = models.CharField(max_length=12, verbose_name='类别')
    # inventory_category = models.PositiveSmallIntegerField(
    #     default=0,
    #     choices=INVENTORY_CATEGORY_CHOICE,
    #     verbose_name='库存类别'
    # )
    inventory_group = models.ForeignKey(InventoryGroup, on_delete=models.CASCADE, verbose_name='分组')
    inventory_num = models.PositiveIntegerField(verbose_name='数量')
    inventory_unit = models.CharField(max_length=12, default='个', verbose_name='单位')
    inventory_specification = models.CharField(max_length=50, verbose_name='规格')
    # inventory_details = models.TextField(max_length=300, default='无', verbose_name='详细信息')
    # inventory_value = models.IntegerField(default=0, verbose_name='库存的特性值')
    # inventory_package = models.CharField(default='', max_length=20, verbose_name='封装')
    inventory_mark = models.CharField(default='无', max_length=300, verbose_name='备注')
    # inventory_create_user = models.CharField(max_length=12, verbose_name='创建人id')
    # inventory_create_user_name = models.CharField(max_length=20, verbose_name='创建人姓名')
    inventory_create_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建人', related_name='create_user')
    inventory_create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # inventory_recent_change_user = models.CharField(max_length=12, verbose_name='最近领用人id')
    # inventory_recent_change_user_name = models.CharField(max_length=20, verbose_name='最近领用人姓名')
    inventory_recent_change_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='最近领用人', related_name='change_user')
    inventory_recent_change_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    # @classmethod
    # def add_inventory(
    #         cls,
    #         # inventory_id,
    #         inventory_name,
    #         inventory_group,
    #         inventory_num,
    #         inventory_unit,
    #         # inventory_details,
    #         # inventory_value,
    #         # inventory_package,
    #         inventory_price,
    #         inventory_mark,
    #         inventory_create_user,
    #         inventory_create_user_name,
    # ):
    #     inventory = cls(
    #         # inventory_id=inventory_id,
    #         inventory_name=inventory_name,
    #         inventory_group=inventory_group,
    #         inventory_num=inventory_num,
    #         inventory_unit=inventory_unit,
    #         # inventory_details=inventory_details,
    #         # inventory_value=inventory_value,
    #         # inventory_package=inventory_package,
    #         inventory_price=inventory_price,
    #         inventory_mark=inventory_mark,
    #         inventory_create_user=inventory_create_user,
    #         inventory_create_user_name=inventory_create_user_name,
    #         inventory_recent_change_user=inventory_create_user,
    #         inventory_recent_change_user_name=inventory_create_user_name,
    #     )
    #     return inventory

    def __str__(self):
        return self.inventory_name

    class Meta:
        db_table = "Inventory"
        ordering = ['inventory_id']  # 以id为标准升序
        verbose_name_plural = '库存'


class InventoryOperation(models.Model):
    """对库存的操作，注意在每次新建库存后都要增加一个此对象"""
    '''选项'''
    INVENTORY_OPERATION_CHOICE = (
        (0, '入库'),
        (1, '出库'),
        (2, '创建'),
    )

    '''属性'''
    inventory_operation_create_date = models.DateField(auto_now_add=True, verbose_name='操作日期')
    inventory_operation_create_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    # inventory_operation_user = models.CharField(max_length=12, verbose_name='操作者id')
    # inventory_operation_user_name = models.CharField(max_length=20, verbose_name='操作者姓名')
    inventory_operation_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='领用人')
    inventory_operation_user_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, verbose_name='操作者ip')
    inventory_operation_user_browser = models.CharField(max_length=30, default='未知的浏览器', verbose_name='浏览器')
    inventory_operation_user_system = models.CharField(max_length=30, default='未知的系统', verbose_name='操作系统')
    inventory_operation_user_device = models.CharField(max_length=30, default='未知的设备', verbose_name='设备')
    inventory_operation_category = models.PositiveSmallIntegerField(
        default=0,
        choices=INVENTORY_OPERATION_CHOICE,
        verbose_name='操作类别'
    )
    inventory_operation_num = models.PositiveIntegerField(verbose_name='操作数量')
    inventory_operation_object = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name='操作的库存对象')

    inventory_num = models.PositiveIntegerField(verbose_name='库存余量')

    # @classmethod
    # def add_inventory_operation(  # 增加一个库存的操作
    #         cls,
    #         inventory_operation_user,
    #         inventory_operation_user_name,
    #         inventory_operation_user_ip,
    #         inventory_operation_user_browser,
    #         inventory_operation_user_system,
    #         inventory_operation_user_device,
    #         inventory_operation_category,
    #         inventory_operation_num,
    #         inventory_num,
    #         inventory_operation_object,
    # ):
    #     inventory_operation = cls(
    #         inventory_operation_user=inventory_operation_user,
    #         inventory_operation_user_name=inventory_operation_user_name,
    #         inventory_operation_user_ip=inventory_operation_user_ip,
    #         inventory_operation_user_browser=inventory_operation_user_browser,
    #         inventory_operation_user_system=inventory_operation_user_system,
    #         inventory_operation_user_device=inventory_operation_user_device,
    #         inventory_operation_category=inventory_operation_category,
    #         inventory_operation_num=inventory_operation_num,
    #         inventory_num=inventory_num,
    #         inventory_operation_object=inventory_operation_object,
    #     )
    #     return inventory_operation

    def __int__(self):
        return self.pk

    class Meta:
        db_table = "InventoryOperation"
        ordering = ['-inventory_operation_create_time']  # 以创建时间为倒序
        verbose_name_plural = '库存操作'


class LoginRecord(models.Model):
    """用户的登录记录"""
    login_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    login_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, verbose_name='登录ip')
    login_browser = models.CharField(max_length=30, default='未知的浏览器', verbose_name='浏览器')
    login_system = models.CharField(max_length=30, default='未知的系统', verbose_name='操作系统')
    login_device = models.CharField(max_length=30, default='未知的设备', verbose_name='设备')
    # login_location = models.CharField(max_length=30, default='未知位置', verbose_name='位置')
    login_date = models.DateField(auto_now_add=True, verbose_name='登录日期')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')

    # @classmethod
    # def add_login_record(  # 增加一个访问记录
    #         cls,
    #         login_user,
    #         login_ip,
    #         login_browser,
    #         login_system,
    #         login_device,
    #         # login_location,
    # ):
    #     login_record = cls(
    #         login_user=login_user,
    #         login_ip=login_ip,
    #         login_browser=login_browser,
    #         login_system=login_system,
    #         login_device=login_device,
    #         # login_location=login_location,
    #     )
    #     return login_record

    def __int__(self):
        return self.pk

    class Meta:
        db_table = "LoginRecord"
        ordering = ['-login_time']  # 以id为标准升序
        verbose_name_plural = '访问记录'


class CustomerTracking(models.Model):
    """客户跟踪状态"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    track_date = models.DateField(verbose_name='跟踪时间记录')
    track_state = models.CharField(max_length=50, verbose_name='项目跟踪状态')

    def __str__(self):
        return self.customer.name

    class Meta:
        db_table = "CustomerTracking"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '客户跟踪状态'


# class MarkdownFile(models.Model):
#     """markdown文件库"""
#     name = models.CharField(max_length=30, verbose_name='文件名')
#     file = models.FileField(verbose_name='文件')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table = "MarkdownFile"
#         ordering = ['id']  # 以id为标准升序
#         verbose_name_plural = 'markdown文件库'
