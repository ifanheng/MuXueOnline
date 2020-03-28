#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/21 19:19
# 什么程序创建：PyCharm
# 作用：

from django import forms
from apps.operation.models import UserAsk

import re


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(max_length=11, min_length=11, required=True)

    class Meta:
        # 使用哪个model
        model = UserAsk
        # 使用model的哪些字段
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data["mobile"]
        regex_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("请填写正确的手机号", code="mobile_invalid")
