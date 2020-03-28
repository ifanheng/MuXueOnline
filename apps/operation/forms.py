#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/22 3:34
# 什么程序创建：PyCharm
# 作用：

from django import forms

from apps.operation.models import UserFavorite, CourseComments


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ["course", "comments"]
