#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/18 14:09
# 什么程序创建：PyCharm
# 作用：

from django import forms

from captcha.fields import CaptchaField

from MuXueOnline.settings import REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile
import redis


class UpdateMobileForm(forms.Form):
    """
    手机动态验证码，用于个人中心修改手机号的
    """
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        """
        针对code字段进行验证（局部钩子）
        :return:
        """
        # 取出moblie和code
        mobile = self.data.get("mobile")  # 注意，这里一定要用data.get来取数据，而不是cleaned_data.get，否则可能可以用，但有时会取不到
        code = self.data.get("code")

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(mobile)
        if code != redis_code:
            # 调用forms里面的方法，抛出异常
            raise forms.ValidationError("手机验证码不正确")
        return self.cleaned_data


class ChangePwdForm(forms.Form):
    """
    这里之所以不用ModelForm，是因为我们定义的model里面只有password字段，而我们要验证两个字段：密码、确认密码
    """
    password1 = forms.CharField(required=True, min_length=6, max_length=16)
    password2 = forms.CharField(required=True, min_length=6, max_length=16)

    def clean(self):
        pwd1 = self.cleaned_data.get("password1", "")
        pwd2 = self.cleaned_data.get("password2", "")

        if pwd1 != pwd2:
            raise forms.ValidationError("密码不一致")
        return self.cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name", "gender", "birthday", "address"]


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


class LoginForm(forms.Form):
    """
    登录需要验证哪些字段
    """
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=6)


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True, min_length=6, max_length=32)
    captcha = CaptchaField()

    def clean_mobile(self):
        mobile = self.data.get("mobile")
        # 验证手机号码，是否已经注册
        is_existed = UserProfile.objects.filter(mobile=mobile)
        if is_existed:
            raise forms.ValidationError("该手机号码已注册")

        return mobile

    def clean_code(self):
        """
        针对code字段进行验证（局部钩子）
        :return:
        """
        # 取出moblie和code
        mobile = self.data.get("mobile")  # 注意，这里一定要用data.get来取数据，而不是cleaned_data.get，否则可能可以用，但有时会取不到
        code = self.data.get("code")

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(mobile)
        if code != redis_code:
            # 调用forms里面的方法，抛出异常
            raise forms.ValidationError("手机验证码不正确")

        return code


class DynamicLoginForm(forms.Form):
    """
    图形验证码
    """
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    """
    手机动态验证码
    """
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        """
        针对code字段进行验证（局部钩子）
        :return:
        """
        # 取出moblie和code
        mobile = self.data.get("mobile")  # 注意，这里一定要用data.get来取数据，而不是cleaned_data.get，否则可能可以用，但有时会取不到
        code = self.data.get("code")

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(mobile)
        if code != redis_code:
            # 调用forms里面的方法，抛出异常
            raise forms.ValidationError("手机验证码不正确")
        return self.cleaned_data
