from django.db import models

from apps.users.models import BaseModel
from apps.courses.models import Course

# 因为我们的User表是继承的django内部的auth_user表，并添加一些自己的字段信息
# 这里直接获取settings.py那里配置的AUTH_USER_MODEL指定的类就行了（那里指定的就是我们继承auth_user的表）
from django.contrib.auth import get_user_model
UserProfile = get_user_model()


class Banner(BaseModel):
    """
    首页 -> 轮播图
    """
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m", max_length=256, verbose_name="轮播图")
    url = models.URLField(max_length=256, verbose_name="跳转地址")
    index = models.IntegerField(default=0, verbose_name="顺序")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name


class UserAsk(BaseModel):
    """
    用户咨询表
    """
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")

    # 这里因为是用户咨询时，手工输入的课程名，所以没必要给课程外键了
    course_name = models.CharField(max_length=50, verbose_name="课程名")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComments(BaseModel):
    """
    课程评论表
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    comments = models.CharField(max_length=256, verbose_name="课程评论")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name


class UserFavorite(BaseModel):
    """
    用户收藏表
    """
    fav_type_choices = (
        (1, "课程"),
        (2, "课程机构"),
        (3, "讲师")
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(verbose_name="搜藏id")
    fav_type = models.IntegerField(choices=fav_type_choices, default=1, verbose_name="收藏类型")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(BaseModel):
    """
    用户消息表，用户产生的个人消息
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    message = models.CharField(max_length=256, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


class UserCourse(BaseModel):
    """
    用户课程表，用户学习了哪些课程
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name
