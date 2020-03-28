#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/22 3:20
# 什么程序创建：PyCharm
# 作用：

from django.urls import path
from apps.operation.views import AddFavView, AddCommentView

urlpatterns = [
    path('fav/', AddFavView.as_view(), name="fav"),
    path('comment/', AddCommentView.as_view(), name="comment"),
]
