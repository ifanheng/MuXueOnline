#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/17 21:49
# 什么程序创建：PyCharm
# 作用：

# 引入xadmin
import xadmin
# 引入自己定义的model
from apps.organizations.models import Teacher, CourseOrg, City


# 这里就不需要再继承任何东西了
class TeacherAdmin(object):
    list_display = ["id", "name", "org", "age", "work_years", "work_company", "work_position", "points", "click_nums",
                    "fav_nums"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "name", "org", "age", "work_years", "work_company", "work_position", "points", "click_nums",
                     "fav_nums"]
    list_filter = ["id", "name", "org", "age", "work_years", "work_company", "work_position", "points", "click_nums",
                   "fav_nums"]
    list_editable = ["id", "name", "org", "age", "work_years", "work_company", "work_position", "points", "click_nums",
                     "fav_nums"]


class CourseOrgAdmin(object):
    list_display = ["id", "name", "category", "city", "click_nums", "fav_nums", "course_nums", "students"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "name", "category", "city", "click_nums", "fav_nums", "course_nums", "students", "desc",
                     "tag", "address"]
    list_filter = ["id", "name", "category", "city", "click_nums", "fav_nums", "course_nums", "students", "desc", "tag",
                   "address"]
    list_editable = ["id", "name", "category", "city", "click_nums", "fav_nums", "course_nums", "students", "desc",
                     "tag", "address"]


class CityAdmin(object):
    list_display = ["id", "name", "desc"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "name", "desc"]
    list_filter = ["id", "name", "desc", "add_time"]
    list_editable = ["name", "desc"]


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)
