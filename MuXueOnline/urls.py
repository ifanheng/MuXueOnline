"""MuXueOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve

from apps.users.views import LoginView, LogoutView, SendSmsView, DynamicLoginView, RegisterView
from apps.operation.views import IndexView
from MuXueOnline.settings import MEDIA_ROOT

import xadmin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    # 首页
    path('', IndexView.as_view(), name="index"),

    # 登录
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('dynamic_login/', DynamicLoginView.as_view(), name="dynamic_login"),

    # 注册
    # path('register/', csrf_exempt(RegisterView.as_view()), name="register"),
    path('register/', RegisterView.as_view(), name="register"),

    # 图片验证码
    url(r'^captcha/', include('captcha.urls')),
    # 手机短信验证码
    url(r'^send_sms/', SendSmsView.as_view(), name="send_sms"),

    # 上传文件的访问url
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 课程机构
    path('org/', include(('apps.organizations.urls', 'organizations'), namespace='org')),

    # 用户先关操作
    path('op/', include(('apps.operation.urls', 'operations'), namespace='op')),

    # 课程
    path('course/', include(('apps.courses.urls', 'course'), namespace='course')),

    # 个人中心
    path('users/', include(('apps.users.urls', 'users'), namespace='users')),

    # ueditor
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]
