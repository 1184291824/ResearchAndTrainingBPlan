from django.db import models


class Group(models.Model):
    group_id = models.CharField(max_length=12)
    group_name = models.CharField(max_length=12)

    def __str__(self):
        return self.group_id

    class Meta:
        db_table = "Group"
        ordering = ['id']  # 以id为标准升序


class User(models.Model):
    user_id = models.CharField(max_length=12)
    user_password_encrypted = models.CharField(max_length=100)  # 加密过的密码
    user_name = models.CharField(max_length=12)
    user_gender = models.BooleanField(default=True)  # true 代表男性，false 代表女性

    @classmethod
    def add_user(cls, user_id, user_password_encrypted, user_name, group_id):
        """
        :param user_id: 用户id
        :param user_password_encrypted: 用户密码
        :param user_name: 用户姓名
        :param group_id: 班级对象
        :return: user对象
        """
        user = cls(user_id=user_id, user_password=user_password_encrypted, user_name=user_name, group_id=group_id)
        return user

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "User"
        ordering = ['id']  # 以id为标准升序
