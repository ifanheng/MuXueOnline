from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Course, CourseTag, CourseResource, Video
from apps.operation.models import UserFavorite, UserCourse, CourseComments


class VideoView(LoginRequiredMixin, View):
    """
    视频播放
    """
    login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 获取视频
        video = Video.objects.get(id=int(video_id))

        # 获取课程评论信息
        comments = CourseComments.objects.filter(course=course)

        # 查询用户是否已经关联了该课程，如果没关联就给数据库加个关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1  # 学习人数+1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)  # 学过该课程的所有用户的对象
        user_ids = [user_course.user.id for user_course in user_courses]  # 学过该课程的所有用户id
        # 学习过该课程的同学们的所有的课程(并基于点击数进行倒序排序)(页面只展示5个数据)
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # 生成课程列表，并排除掉当前正在访问的这个课程if user_course.course.id != course.id
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        # 获取课程资源
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "comments": comments,
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    章程章节评论页
    """
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 获取课程评论信息
        comments = CourseComments.objects.filter(course=course)

        # 查询用户是否已经关联了该课程，如果没关联就给数据库加个关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1  # 学习人数+1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)  # 学过该课程的所有用户的对象
        user_ids = [user_course.user.id for user_course in user_courses]  # 学过该课程的所有用户id
        # 学习过该课程的同学们的所有的课程(并基于点击数进行倒序排序)(页面只展示5个数据)
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # 生成课程列表，并排除掉当前正在访问的这个课程if user_course.course.id != course.id
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        # 获取课程资源
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "comments": comments,
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses
        })


class CourseLessonView(LoginRequiredMixin, View):
    """
    章程章节页
    """
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 查询用户是否已经关联了该课程，如果没关联就给数据库加个关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1  # 学习人数+1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)  # 学过该课程的所有用户的对象
        user_ids = [user_course.user.id for user_course in user_courses]  # 学过该课程的所有用户id
        # 学习过该课程的同学们的所有的课程(并基于点击数进行倒序排序)(页面只展示5个数据)
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # 生成课程列表，并排除掉当前正在访问的这个课程if user_course.course.id != course.id
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        # 获取课程资源
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses
        })


class CourseDetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 获取收藏状态
        has_fav_course = False  # 是否收藏课程
        has_fav_org = False  # 是否收藏课程机构
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 通过课程的tag做课程的推荐
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     # 找到对应的tag的课程，并排除当前我们正在看的这个详情页的课程
        #     related_courses = Course.objects.filter(tag=tag).exclude(id=course.id)[:3]

        # 通过课程的tag做课程的推荐
        tags = course.coursetag_set.all()  # 取出课程对应的所有的tag
        tag_list = [tag.tag for tag in tags]  # 遍历tags并把它加入到tag_list

        # 过滤掉当前正在访问的这个课程详情页的课程（推荐的时候不要把自己也推荐出来）
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set()  # 为了去重，这里创建集合而不是list
        for course_tag in course_tags:
            related_courses.add(course_tag.course)

        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses
        })


class CourseListView(View):
    """
    课程机构列表页
    """

    def get(self, request, *args, **kwargs):
        # 默认以添加时间排序
        all_courses = Course.objects.order_by("-add_time")

        # 热门课程
        hot_courses = Course.objects.order_by("-click_nums")[:3]

        # 获取搜索用的keywords关键词
        keywords = request.GET.get("keywords", "")
        search_type = "course"
        # 使用django的ORM的Q查询（or查询）来模糊查询多个字段，这里只针对三个字段进行了模糊查询，可以根据自己的业务选择更多字段
        if keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(degree__icontains=keywords))

        # 课程排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")

        # 分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # per_page=5 每页显示5条数据
        p = Paginator(all_courses, per_page=2, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            "search_type": search_type,
            "keywords": keywords
        })
