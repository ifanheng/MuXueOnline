from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm
from apps.users.forms import RegisterGetForm, RegisterPostForm
from apps.users.forms import UploadImageForm, UserInfoForm, ChangePwdForm, UpdateMobileForm
from MuXueOnline.settings import yunpian_apikey, REDIS_HOST, REDIS_PORT
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile
from apps.operation.models import UserFavorite, UserMessage, Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course

import redis


class CustomAuth(ModelBackend):
    """
    自定义用户验证模块
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 查看用户名 或者 手机号是否等于前端传过来的username
            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                # 会跟数据库里面的那个加密的密码进行比较
                return user
        except Exception as e:
            return None


class MyMessageView(LoginRequiredMixin, View):
    """
    个人中心 -> 我的消息
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)

        # 分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # per_page=5 每页显示5条数据
        p = Paginator(messages, per_page=2, request=request)
        messages = p.page(page)

        # 把消息设置成已读
        for message in messages.object_list:
            message.has_read = True
            message.save()

        current_page = "my_messages"
        return render(request, "usercenter-message.html", {
            "current_page": current_page,
            "messages": messages
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    个人中心 -> 我的收藏 -> 公开课程
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist:
                pass
        current_page = "my_fav_course"
        return render(request, "usercenter-fav-course.html", {
            "current_page": current_page,
            "course_list": course_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    个人中心 -> 我的收藏 -> 授课讲师
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)
        current_page = "my_fav_teacher"
        return render(request, "usercenter-fav-teacher.html", {
            "current_page": current_page,
            "teacher_list": teacher_list
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    个人中心 -> 我的收藏 -> 课程机构
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        current_page = "my_fav_org"
        return render(request, "usercenter-fav-org.html", {
            "current_page": current_page,
            "org_list": org_list
        })


class MyCourseView(LoginRequiredMixin, View):
    """
    个人中心 -> 我的课程
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        # my_courses = UserCourse.objects.filter(user=request.user)

        current_page = "my_course"
        return render(request, "usercenter-mycourse.html", {
            # "my_courses": my_courses,
            "current_page": current_page
        })


class ChangeMobileView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        mobile_form = UpdateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data["mobile"]
            # 已经存在的记录不能重复注册
            if request.user.mobile == mobile:
                return JsonResponse({
                    "mobile": "和当前号码一致"
                })
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    "mobile": "该手机号已经被占用"
                })
            user = request.user
            user.mobile = mobile
            # user.username = mobile  # 根据业务场景来决定，修改手机号的时候，要不要把账号也改成新的手机号
            user.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            JsonResponse(mobile_form.errors)


class ChangePwdView(View):
    """
    用户中心 -> 个人资料 -> 修改密码
    """

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd = request.POST.get("password1", "")
            user = request.user
            user.set_password(pwd)
            user.save()
            # login(request, user)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    """
    用户中心 -> 个人资料 -> 修改头像
    """
    login_url = "/login/"

    def save_file(self, file):
        """
        负责把用户上传的文件写入到本地
        :param fiel: 用户上传的文件
        :return:
        """

    def post(self, request, *args, **kwargs):
        # 获取用户上传的文件
        # request.POST只能接受非文件类型，所以要把文件也传递给它request.FILES
        # 如果不传instance=request.user的话，会被认为是一个新的数据的保存；instance=是在告诉它针对哪个实例进行修改
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })


class UserInfoView(LoginRequiredMixin, View):
    """
    用户中心 - 个人资料
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        # 获取图片验证码（用于手机号修改的）
        captcha_form = RegisterGetForm()

        current_page = "info"
        return render(request, "usercenter-info.html", {
            "captcha_form": captcha_form,
            "current_page": current_page
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({"status": "success"})
        else:
            # 这里配合前端的代码，直接返回form验证的错误数据
            return JsonResponse(user_info_form.errors)


class RegisterView(View):
    """
    注册页面
    """

    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form": register_get_form
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]

            # 新建用户
            user = UserProfile(username=mobile)
            password = register_post_form.cleaned_data["password"]
            user.set_password(password)  # 以密文的方式保存到数据库
            user.mobile = mobile  # 因为这个是必填字段，所以要给mobile也指定一个值
            user.save()

            # 执行登录操作
            login(request, user)
            return redirect(reverse("index"))
        else:
            # 动态图形验证码
            register_get_form = RegisterGetForm()
            return render(request, "register.html", {
                'register_get_form': register_get_form,
                'register_post_form': register_post_form
            })


class DynamicLoginView(View):
    """
    动态验证码登录
    """
    banners = Banner.objects.all()[:5]

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        if login_form.is_valid():
            # 需求：没有注册依然也可以登录
            # 查询表中，有没有这个手机号
            mobile = login_form.cleaned_data["mobile"]
            existed_user = UserProfile.objects.filter(mobile=mobile)

            if existed_user:
                # 如果用户存在的话，就取出这个用户对象
                user = existed_user[0]
            else:
                # 用户不存在，就新建一个用户(这里的用户名当然要指向mobile了)
                user = UserProfile(username=mobile)
                # 因为这个用户是使用设计验证码登录的，以前没有这用户，所以也就没有他的密码，但是密码这个字段有时必填字段
                # 所以要给他一个随机的密码写入到数据库中，反正他也用不到这个密码（只要别人猜不到就行），他只是使用手机验证码登录而已
                password = generate_random(10, 2)  # 生成一个10位的随机密码
                user.set_password(password)  # 以密文的方式保存到数据库
                user.mobile = mobile  # 因为这个是必填字段，所以要给mobile也指定一个值
                user.save()

            # 执行登录操作
            login(request, user)

            # 用户登陆之前正在访问哪个页面，就让他登陆后停留在哪个页面
            next = request.GET.get("next", "")
            if next:
                return redirect(next)

            return redirect(reverse("index"))
        else:
            # 当为手机验证码登录失败是，这里为True
            dynamic_login = True
            # 动态图形验证码
            d_form = DynamicLoginForm()

            return render(request, "login.html", {
                "login_form": login_form,
                "dynamic_login": dynamic_login,
                'd_form': d_form,
                "banners": self.banners
            })


class SendSmsView(View):
    """
    发送短信验证码
    """

    def post(self, request, *args, **kwargs):
        # 验证图形验证码是否正确
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            # 随机生成验证码
            code = generate_random(4, 0)
            re_json = send_single_sms(yunpian_apikey, mobile=mobile, code=code)
            if re_json["code"] == 0:
                re_dict["status"] = "success"

                # 把手机验证码存储到redis
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
                r.set(str(mobile), code)  # 手机号与验证码（有就覆盖，没有就创建）
                r.expire(str(mobile), 300)  # 300秒后过期
            else:
                re_dict["msg"] = re_json["msg"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)


class LogoutView(View):
    """
    退出登录
    """

    def get(self, request, *args, **kwargs):
        # 使用django内置的logout来退出登录
        logout(request)
        return redirect(reverse("index"))


class LoginView(View):
    """
    登录
    """
    banners = Banner.objects.all()[:5]

    def get(self, request, *args, **kwargs):
        # 判断用户是否已经登录
        if request.user.is_authenticated:
            # 已经登录的用户，直接重定向到首页
            return redirect(reverse("index"))

        next = request.GET.get("next", "")
        # 动态图形验证码
        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,
            "banners": self.banners
        })

    def post(self, request, *args, **kwargs):
        # 表单验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

                # 用户登陆之前正在访问哪个页面，就让他登陆后停留在哪个页面
                next = request.GET.get("next", "")
                if next:
                    return redirect(next)
                return redirect(reverse("index"))
            else:
                return render(request, "login.html", {
                    "error_msg": "用户名或密码错误",
                    "login_form": login_form,
                    "banners": self.banners
                })
        else:
            return render(request, "login.html", {
                "login_form": login_form,
                "banners": self.banners
            })
