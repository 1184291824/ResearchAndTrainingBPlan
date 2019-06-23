from django.db import models


class Group(models.Model):
    group_id = models.CharField(verbose_name='组编号', max_length=12)
    group_name = models.CharField(verbose_name='组名称', max_length=12)

    def __str__(self):
        return self.group_id

    class Meta:
        db_table = "Group"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '分组'


class User(models.Model):
    user_id = models.CharField(verbose_name='用户id', max_length=12)
    user_password = models.CharField(max_length=20, verbose_name='密码')
    user_group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='所属组')

    user_name = models.CharField(max_length=12, default='保密', verbose_name='姓名')
    user_gender = models.CharField(max_length=1, default='男', verbose_name='性别')  # true 代表男性，false 代表女性
    user_identity = models.CharField(max_length=20, default='1', verbose_name='身份与权限')  # 1:职员，2:管理员，3:总管理员
    user_question = models.CharField(default='', max_length=20, blank=True, verbose_name='密保问题')  # 密保问题
    user_question_answer = models.CharField(default='', max_length=20, blank=True, verbose_name='密保问题答案')  # 密保问题答案
    user_create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 用户的创建时间

    @classmethod
    def add_user(cls, user_id, user_password, user_group):
        """
        :param user_id: 用户id
        :param user_password: 用户密码
        :param user_group: 组对象
        :return: user
        """
        user = cls(user_id=user_id, user_password=user_password, user_group=user_group)
        return user

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "User"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '用户'
