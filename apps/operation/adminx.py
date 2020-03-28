#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/17 23:32
# 什么程序创建：PyCharm
# 作用：

import xadmin

from apps.operation.models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse, Banner


class BannerAdmin(object):
    list_display = ["title", "url", "index", "image"]
    search_fields = ["title", "url", "index"]
    list_filter = ['title']


class GlobalSettings(object):
    site_title = "有趣后台管理系统"
    site_footer = "有趣在线网"
    # 配置左侧菜单栏是否折叠
    # menu_style = "accordion"


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class UserAskAdmin(object):
    list_display = ["id", "name", "mobile", "course_name"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "name", "mobile", "course_name"]
    list_filter = ["id", "name", "mobile", "course_name"]
    list_editable = ["id", "name", "mobile", "course_name"]


class CourseCommentsAdmin(object):
    list_display = ["id", "user", "course", "comments"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "user", "course", "comments"]
    list_filter = ["id", "user", "course", "comments"]
    list_editable = ["id", "user", "course", "comments"]


class UserFavoriteAdmin(object):
    list_display = ["id", "user", "fav_id", "fav_type"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "user", "fav_id", "fav_type"]
    list_filter = ["id", "user", "fav_id", "fav_type"]
    list_editable = ["id", "user", "fav_id", "fav_type"]


class UserMessageAdmin(object):
    list_display = ["id", "user", "message", "has_read"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "user", "message", "has_read"]
    list_filter = ["id", "user", "message", "has_read"]
    list_editable = ["id", "user", "message", "has_read"]


class UserCourseAdmin(object):
    list_display = ["id", "user", "course"]
    # 指定搜索的时候，会搜索哪些字段
    search_fields = ["id", "user", "course"]
    list_filter = ["id", "user", "course"]
    list_editable = ["id", "user", "course"]


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
