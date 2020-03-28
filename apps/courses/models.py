from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher, CourseOrg

from DjangoUeditor.models import UEditorField


class Course(BaseModel):
    """
    课程表
    """
    degree_choices = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师")
    # 添加一个字段，用于关联课程机构
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="课程机构")

    name = models.CharField(verbose_name="课程名", max_length=64)
    desc = models.CharField(verbose_name="课程描述", max_length=512)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    degree = models.CharField(verbose_name="难度", choices=degree_choices, max_length=2)
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default="后端开发", max_length=32, verbose_name="课程类别")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=16)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师告诉你")
    notice = models.CharField(verbose_name="课程公告", max_length=300, default="")

    is_banner = models.BooleanField(default=False, verbose_name="是否为广告位")
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="course/ueditor/images/", filePath="course/ueditor/files/", default="")
    image = models.ImageField(upload_to="course/%Y/%m", verbose_name="封面图", max_length=128)

    # 是否为经典课程
    is_classics = models.BooleanField(default=False, verbose_name="是否为经典课程")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        """
        获取课程的章节数
        """
        return self.lesson_set.all().count()


class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    tag = models.CharField(max_length=100, verbose_name="标签名")

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Lesson(BaseModel):
    """
    章节表
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=128, verbose_name="章节名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    class Meta:
        verbose_name = "章节信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    """
    视频表
    """
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="视频名", max_length=128)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    url = models.CharField(max_length=1024, verbose_name="访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    """
    课程资源表
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=128, verbose_name="资源名称")
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=512)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
