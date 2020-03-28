from django.db import models
from datetime import datetime

# django本身的用户表auth_user的抽象类
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        # 防止这个类会去数据库里面生成一张表
        abstract = True


class UserProfile(AbstractUser):
    """
    继承django内部的auth_user表，并添加一些自己的字段信息
    """
    GENDER_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )

    nick_name = models.CharField(max_length=64, verbose_name="昵称", null=True, blank=True)
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICES, max_length=16)
    address = models.CharField(max_length=128, verbose_name="地址", null=True, blank=True)
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    image = models.ImageField(upload_to="head_image/%Y/%m", default="head_image/default.jpg", verbose_name="头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def unread_nums(self):
        """
        未读消息数
        """
        return self.usermessage_set.filter(has_read=False).count()

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username
