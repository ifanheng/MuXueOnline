from django.db import models

from apps.users.models import BaseModel


class City(BaseModel):
    """
    城市表
    """
    name = models.CharField(max_length=20, verbose_name="城市名")
    desc = models.CharField(max_length=256, verbose_name="城市描述")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    """
    课程机构表
    """
    category_choices = (
        ("pxjg", "培训机构"),
        ("gr", "个人"),
        ("gx", "高校")
    )
    name = models.CharField(max_length=64, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    tag = models.CharField(default="全国知名", max_length=10, verbose_name="机构标签")
    category = models.CharField(default="pxjg", max_length=20, choices=category_choices, verbose_name="机构类别")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", max_length=128, verbose_name="logo")
    address = models.CharField(max_length=150, verbose_name="机构地址")
    course_nums = models.IntegerField(default=0, verbose_name="课程数量")
    students = models.IntegerField(default=0, verbose_name="学习人数")

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")

    is_auth = models.BooleanField(default=False, verbose_name="是否认证")
    is_gold = models.BooleanField(default=False, verbose_name="是否为金牌")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def courses(self):
        courses = self.course_set.filter(is_classics=True)[:3]
        return courses


from apps.users.models import UserProfile
class Teacher(BaseModel):
    """
    讲师表
    """
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="用户")
    name = models.CharField(max_length=50, verbose_name="讲师名")
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=64, verbose_name="就职公司")
    work_position = models.CharField(max_length=64, verbose_name="公司职位")
    points = models.CharField(max_length=64, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(default="", upload_to="teacher/%Y/%m", max_length=128, verbose_name="头像")

    class Meta:
        verbose_name = "讲师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        """
        用于获取某个老师所拥有的课程数
        :return:
        """
        return self.course_set.all().count()
