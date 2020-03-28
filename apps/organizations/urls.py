#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/21 18:14
# 什么程序创建：PyCharm
# 作用：

from django.urls import path
from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView
from apps.organizations.views import TeacherListView, TeacherDetailView

urlpatterns = [
    path('list/', OrgView.as_view(), name='list'),
    path('add_ask/', AddAskView.as_view(), name='add_ask'),
    # url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    path('<int:org_id>/', OrgHomeView.as_view(), name="home"),
    path('<int:org_id>/teacher/', OrgTeacherView.as_view(), name="teacher"),
    path('<int:org_id>/course/', OrgCourseView.as_view(), name="course"),
    path('<int:org_id>/desc/', OrgDescView.as_view(), name="desc"),

    path('teacher/', TeacherListView.as_view(), name="teacher"),
    path('teacher_detail/<int:teacher_id>', TeacherDetailView.as_view(), name="teacher_detail"),
]
