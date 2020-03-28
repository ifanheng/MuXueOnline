#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/17 21:49
# 什么程序创建：PyCharm
# 作用：

# 引入xadmin
import xadmin
# 引入自己定义的model
from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag
from xadmin.layout import Fieldset, Main, Side, Row
from import_export import resources


class MyCourseResource(resources.ModelResource):
    class Meta:
        model = CourseResource
        # fields = ('name', 'description',)
        # exclude = ()


class NewCourseAdmin(object):
    import_export_args = {'import_resource_class': MyCourseResource, 'export_resource_class': MyCourseResource}
    list_display = ["id", "name", "desc", "degree", "students", "fav_nums", "click_nums", "category", "tag"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "name", "desc", "degree", "students", "fav_nums", "click_nums", "category", "tag",
                     "teacher__name",
                     "learn_times", "youneed_know", "teacher_tell", "detail"]
    list_filter = ["id", "name", "desc", "degree", "students", "fav_nums", "click_nums", "category", "tag",
                   "teacher__name",
                   "learn_times", "youneed_know", "teacher_tell", "detail"]
    list_editable = ["desc", "degree", "category", "tag"]
    model_icon = "fa fa-address-book"
    # 指定对detail字段使用ueditor插件
    style_fields = {
        "detail": "ueditor"
    }

    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                    Main(
                        Fieldset("讲师信息",
                                 'teacher','course_org',
                                 css_class='unsort no_title'
                                 ),
                        Fieldset("基本信息",
                                 'name', 'desc',
                                 Row('learn_times', 'degree'),
                                 Row('category', 'tag'),
                                 'youneed_know', 'teacher_tell', 'detail',
                                 ),
                    ),
                    Side(
                        Fieldset("访问信息",
                                 'fav_nums', 'click_nums', 'students','add_time'
                                 ),
                    ),
                    Side(
                        Fieldset("选择信息",
                                 'is_banner', 'is_classics'
                                 ),
                    )
            )
        return super(NewCourseAdmin, self).get_form_layout()


# 这里就不需要再继承任何东西了
class CourseAdmin(object):
    list_display = ["id", "name", "desc", "degree", "students", "fav_nums", "click_nums", "category", "tag"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "name", "desc", "degree", "students", "fav_nums", "click_nums", "category", "tag", "teacher__name",
                     "learn_times", "youneed_know", "teacher_tell", "detail"]
    list_filter = ["id", "name", "desc", "degree", "students", "fav_nums", "click_nums", "category", "tag", "teacher__name",
                     "learn_times", "youneed_know", "teacher_tell", "detail"]
    list_editable = ["desc", "degree", "category", "tag"]


class LessonAdmin(object):
    list_display = ["id", "name", "learn_times"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "name", "learn_times",  "course__name"]
    list_filter = ["id", "name", "learn_times",  "course__name"]
    list_editable = ["id", "name", "learn_times",  "course__name"]


class VideoAdmin(object):
    list_display = ["id", "name", "learn_times", "lesson", "url"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "name", "learn_times", "lesson", "url"]
    list_filter = ["id", "name", "learn_times", "lesson", "url"]
    list_editable = ["id", "name", "learn_times", "lesson", "url"]


class CourseResourceAdmin(object):
    list_display = ["id", "name", "course", "file"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "name", "course", "file"]
    list_filter = ["id", "name", "course", "file"]
    list_editable = ["id", "name", "course", "file"]


class CourseTagAdmin(object):
    list_display = ["id", "course", "tag", "add_time"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "course", "tag", "add_time"]
    list_filter = ["id", "course", "tag", "add_time"]
    list_editable = ["id", "course", "tag", "add_time"]


xadmin.site.register(Course, NewCourseAdmin)
# xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)
