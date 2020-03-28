from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from apps.operation.models import UserFavorite, CourseComments, Banner
from apps.courses.models import Course
from apps.organizations.models import CourseOrg, Teacher
from apps.operation.forms import UserFavForm, CommentForm


class IndexView(View):
    """
    首页
    """
    def get(self, request, *args, **kwargs):
        # 取出轮播图
        banners = Banner.objects.all().order_by("index")
        # 取出不是广告位的6条课程数据（因为前端页面那里，针对不是广告位的只留个6个位置）
        courses = Course.objects.filter(is_banner=False)[:6]
        # 取出广告位的课程数据
        banner_courses = Course.objects.filter(is_banner=True)
        # 取出课程机构数据15条
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "banners": banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs
        })


class AddCommentView(View):
    """
    添加评论
    """

    def post(self, request, *args, **kwargs):
        # 如果用户未登录，是不能评论的
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]

            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments
            comment.course = course
            comment.save()

            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


class AddFavView(View):
    """
    用户收藏、取消收藏的操作
    """
    def post(self, request, *args, **kwargs):

        # 如果用户未登录，是不能收藏的
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]

            # 该数据有没有收藏过
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            # 如果已经收藏了，就把它取消掉（因为收藏按钮只有两个：收藏、取消收藏）
            if existed_records:
                existed_records.delete()  # 删除收藏

                # 对应的收藏数字减1
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })
