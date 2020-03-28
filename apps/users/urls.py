#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/25 8:19
# 什么程序创建：PyCharm
# 作用：

from django.urls import path
from apps.users.views import UserInfoView, UploadImageView, ChangePwdView, ChangeMobileView, MyCourseView, MyFavOrgView
from apps.users.views import MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='info'),
    path('image/upload/', UploadImageView.as_view(), name='image'),
    path('update/pwd/', ChangePwdView.as_view(), name='update_pwd'),
    path('update/mobile/', ChangeMobileView.as_view(), name='update_mobile'),
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),
    path('myfavorg/', MyFavOrgView.as_view(), name='myfavorg'),
    path('myfav_teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    path('myfav_course/', MyFavCourseView.as_view(), name='myfav_course'),
    path('messages/', MyMessageView.as_view(), name='messages'),
]
