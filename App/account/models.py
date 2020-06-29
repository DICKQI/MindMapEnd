from django.db import models
from django.utils.timezone import now


# Create your models here.

class UserPassword(models.Model):
    """账户密码表"""
    password = models.CharField(verbose_name='用户密码', max_length=1000, blank=False, default=None)

    class Meta:
        verbose_name = '用户密码'
        verbose_name_plural = verbose_name
        db_table = 'Account_UserPassword'


class UserInfo(models.Model):
    """主账户表"""
    email = models.EmailField(verbose_name='登录邮箱', blank=False, default=None, unique=True)

    nickname = models.CharField(verbose_name='昵称', max_length=20, default=None, blank=False, unique=True)

    password = models.ForeignKey(UserPassword, verbose_name='密码', default='', blank=False, on_delete=models.CASCADE)

    join_date = models.DateTimeField(verbose_name='注册日期', default=now)

    sex = models.CharField(verbose_name='性别', max_length=10, default='secrecy', blank=False)

    signature = models.CharField(verbose_name='签名', max_length=100, blank=True)

    head = models.TextField(verbose_name='头像', blank=True, default='')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name + '列表'
        ordering = ['-join_date']
        db_table = 'Account_UserInfo'

