import logging
from typing import List

import orjson
from common.djangoapps.student.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, FilterSchema, Field, Query
from ninja.renderers import BaseRenderer
from ninja.security import django_auth
from ninja.pagination import paginate
from ninja_extra.searching import searching, Searching
from ninja_extra import api_controller, route, NinjaExtraAPI
from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.enrollments import api as enrollments_api

from typing import Optional
from .core.models import Program, Project, Organization
from .courses.data_api import get_course_enrollments, get_liked_courses
from .courses.models import Course, LikedCourse
from .learners.models import ProgramEnrollment, LearningRequest
from .profiles.models import UrFUProfile
from .schema import (UserProfileSchema,
                     UrFUProfileSchema,
                     UrFUProfileIn,
                     ProgramEnrollmentIn,
                     LikedCourseIn,
                     CourseSchema,
                     OrganizationSchema,
                     ProgramSchema,
                     ProjectSchema
                     )

log = logging.getLogger(__name__)


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def default(self, obj):
        if isinstance(obj, CourseKey):
            return str(obj)

    def render(self, request, data, *, response_status):
        return orjson.dumps(data, default=self.default)


api = NinjaAPI(renderer=ORJSONRenderer(), csrf=True)


class CourseFilterSchema(FilterSchema):
    search: Optional[str] = Field(q=['course_overview__display_name__icontains'])


@api.get("/me", auth=django_auth, response=UserProfileSchema)
def me(request):
    user = User.objects.get(username=request.auth)
    profile = UserProfile.objects.get(user=user)
    return profile


@api.get('me/profile', auth=django_auth, response=UrFUProfileSchema)
def profile(request):
    user = User.objects.get(username=request.auth)
    verified_profile = UrFUProfile.objects.get(user=user)
    return verified_profile


@api.post('me/learning_request', auth=django_auth, description="Создание, наполнение профиля пользователя и заявки на обучение")
def fill_profile(request, payload: UrFUProfileIn):
    user = User.objects.get(username=request.auth)
    data = payload.dict()
    learning_request_data = {'course_id': data.get('course'), 'user': user}
    del data['course']
    verified_profile = UrFUProfile(**data)
    verified_profile.user = user
    verified_profile.save()
    # TODO send lead to bitrix24

    learning_request = LearningRequest.objects.create(learning_request_data)
    return verified_profile, learning_request


@api.get("/courses/my", auth=django_auth)
def my(request):
    enrollments = get_course_enrollments(request.auth, include_inactive=False)
    return enrollments


@api.get("/courses/{int:course_id}/my", auth=django_auth)
def add_course_enrollment(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    enrollment = enrollments_api.get_enrollment(request.auth, str(course.course_id))
    return enrollment



@api.get("/me/enroll/{int:course_id}", auth=django_auth)
def add_course_enrollment(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    enrollment = enrollments_api.add_enrollment(request.auth, str(course.course_id))
    return enrollment


@api.get("/orgs", response=List[OrganizationSchema])
def orgs(request, limit: int = 10, offset: int = 0):
    qs = Organization.objects.filter(active=True, status='published')
    return qs[offset: offset + limit]


@api.get("/projects", response=List[ProjectSchema])  # description="Creates an order and updates stock"
def projects(request, limit: int = 10, offset: int = 0):
    qs = Project.available_objects.filter(active=True, status='published')
    return qs[offset: offset + limit]


@api.get("/programs", response=List[ProgramSchema])
def programs(request, limit: int = 10, offset: int = 0):
    qs = Program.available_objects.filter(active=True, status='published')
    return qs[offset: offset + limit]


@api.get("/courses", response=List[CourseSchema])
@paginate
def courses(request, filters: CourseFilterSchema = Query(default=FilterSchema())):
    qs = Course.objects.filter(status='published').order_by('id')
    qs = filters.filter(qs)
    return qs


@api.get("/courses/{int:course_id}", response=CourseSchema)
def get_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    return course


@api.post("/enroll", description="Зачисляет пользователя на программу или проект")
def enroll_user_to_program(request, payload: ProgramEnrollmentIn):
    enrollment = ProgramEnrollment.objects.create(**payload.dict())
    return {
        "email": enrollment.user.email,
        "program_uuid": enrollment.program_uuid,
        "project_uuid": enrollment.project_uuid,
        "success": True
    }


@api.post('/courses/like', description='Mark course as liked')
def like_course(request, payload: LikedCourseIn):
    liked = LikedCourse.create(
        username=payload.dict()['username'],
        course_id=payload.dict()['course_id']
    )
    return {"success": bool(liked)}


@api.get('/courses/likes', auth=django_auth, description='List liked courses')
def liked_course(request):
    liked_courses = get_liked_courses(request.auth)
    return liked_courses
