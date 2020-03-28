from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.http import JsonResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.organizations.models import CourseOrg, City, Teacher
from apps.operation.models import UserFavorite
from apps.organizations.forms import AddAskForm


class TeacherDetailView(View):
    """
    讲师详情
    """
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                org_fav = True

        # 排行榜
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "teacher_fav": teacher_fav,
            "org_fav": org_fav,
            "hot_teachers": hot_teachers
        })


class TeacherListView(View):
    """
    讲师列表页
    """
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()  # 讲师的数量

        # 排行榜
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        # 获取搜索用的keywords关键词
        keywords = request.GET.get("keywords", "")
        search_type = "teacher"
        # 使用django的ORM的Q查询（or查询）来模糊查询多个字段，这里只针对三个字段进行了模糊查询，可以根据自己的业务选择更多字段
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords))

        # 排序
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")

        # 分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # per_page=5 每页显示5条数据
        p = Paginator(all_teachers, per_page=2, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            "hot_teachers": hot_teachers,
            "search_type": search_type,
            "keywords": keywords
        })


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 点击数+1
        course_org.click_nums += 1
        course_org.save()

        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 用于前端页面那里判断是否选中(选中的是谁，就给谁active样式)
        current_page = "desc"
        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


class OrgCourseView(View):
    """
    机构课程，显示一个机构里面有哪些课程以及对应的信息
    """
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 点击数+1
        course_org.click_nums += 1
        course_org.save()

        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 这个机构下面有哪些课程
        all_courses = course_org.course_set.all()

        # 这个机构下面有哪些课程(分页处理)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # per_page=5 每页显示5条数据
        p = Paginator(all_courses, per_page=1, request=request)
        courses = p.page(page)

        # 用于前端页面那里判断是否选中(选中的是谁，就给谁active样式)
        current_page = "course"
        return render(request, "org-detail-course.html", {
            "all_courses": courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


class OrgTeacherView(View):
    """
    机构讲师
    """
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 点击数+1
        course_org.click_nums += 1
        course_org.save()

        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teacher = course_org.teacher_set.all()

        # 用于前端页面那里判断是否选中(选中的是谁，就给谁active样式)
        current_page = "teacher"
        return render(request, "org-detail-teachers.html", {
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


class OrgHomeView(View):
    """
    机构详情页
    """
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 点击数+1
        course_org.click_nums += 1
        course_org.save()

        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 页面只显示3个课程
        all_courses = course_org.course_set.all()[:3]
        # 老师只显示1个
        all_teacher = course_org.teacher_set.all()[:1]

        current_page = "home"
        return render(request, "org-detail-homepage.html", {
            "org_id": org_id,
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


class AddAskView(View):
    """
    处理用户的咨询
    """
    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })


class OrgView(View):
    """
    课程机构页
    """

    def get(self, request, *args, **kwargs):
        # 从数据库中取出获取课程机构的数据
        all_orgs = CourseOrg.objects.all()
        # 获取所有的城市数据
        all_citys = City.objects.all()
        # 使用点击数对课程机构进行排名，只取前3个
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 获取搜索用的keywords关键词
        keywords = request.GET.get("keywords", "")
        search_type = "org"
        # 使用django的ORM的Q查询（or查询）来模糊查询多个字段，这里只针对三个字段进行了模糊查询，可以根据自己的业务选择更多字段
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 对课程机构进行筛选
        # 为什么要get("ct")呢？因为我们前端的页面这里传过来的key就是ct呀<a href="?ct=pxjg&city="><span class="">xxx</span></a>
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 通过所在城市对课程机构进行筛选(通过city id)
        city_id = request.GET.get("city", "")
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))

        # 对机构进行排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        # 统计当前筛选出来的机构一共有多少
        org_nums = all_orgs.count()

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # per_page=5 每页显示5条数据
        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "org_nums": org_nums,
            "all_citys": all_citys,
            "category": category,
            "city_id": city_id,
            "sort": sort,
            "hot_orgs": hot_orgs,
            "search_type": search_type,
            "keywords": keywords
        })
