from datetime import date
from typing import List, Dict

import orjson
from django.contrib.auth import get_user_model
from lms.djangoapps.courseware.tabs import (
    CourseInfoTab,
    CourseTab
)
from ninja import NinjaAPI, ModelSchema, Schema
from ninja.orm import create_schema
from ninja.renderers import BaseRenderer
from opaque_keys.edx.keys import UsageKey, CourseKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.core.djangoapps.models.course_details import CourseDetails
from pydantic import validator
from xmodule.course_module import Textbook
from xmodule.tabs import CourseTab

from .core.models import Program, Project, Organization
from .courses.models import Course
from .learners.models import ProgramEnrollment


class CourseTabPydantic(CourseTab):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        def proxy_validate(value):
            return cls.validate(tab_dict=value)

        yield proxy_validate


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def default(self, obj):
        if isinstance(obj, CourseKey):
            return str(obj)

    def render(self, request, data, *, response_status):
        return orjson.dumps(data, default=self.default)


api = NinjaAPI(renderer=ORJSONRenderer())


class UserIn(Schema):
    id: str = None
    username: str = None
    email: int = None


class ProgramEnrollmentIn(Schema):
    user: UserIn
    program_uuid: str = None
    project_uuid: str = None


class ChapterSchema(Schema):
    title: str
    url: str


class CourseTabSchema(Schema):
    type: str = None
    name: str = None


class CourseKeySchema(Schema):
    course: str = None


class TextbookSchema(Schema):
    chapters: List[ChapterSchema] = []


class CourseOverviewProxy(CourseOverview):
    @property
    def description(self):
        return CourseDetails.fetch_about_attribute(self.id, 'description')


BaseCourseOverviewSchema = create_schema(
    CourseOverviewProxy,
    fields=[
        'display_name',
        'start_date',
        'end_date',
        'banner_image_url',
        'course_image_url',
        'lowest_passing_grade',
        'enrollment_start',
        'enrollment_end',
        'invitation_only',
        'max_student_enrollments_allowed',
        'catalog_visibility',
        'short_description',
        'course_video_url',
        'effort',
        'language',
    ],
    custom_fields=[
        ('id', str, None),
        ('number', str, None),
        ('description', str, None),
        ('url_name', str, None),
        ('display_name_with_default', str, None),
        ('display_name_with_default_escaped', str, None),
        ('dashboard_start_display', date, None),
        ('start_date_is_still_default', bool, True),
        ('sorting_score', int, None),
        ('start_type', str, 'empty'),
        ('start_display', str, None),
        ('pre_requisite_courses', List[CourseKeySchema], []),
        ('tabs', List[CourseTabSchema], []),
        ('image_urls', dict, None),
        ('pacing', str, None),
        ('closest_released_language', str, None),
        ('allow_public_wiki_access', bool, None),
        ('textbooks', List[TextbookSchema], []),
        ('pdf_textbooks', List[TextbookSchema], []),
        ('html_textbooks', List[TextbookSchema], []),
        ('course_visibility', str, None),
        ('teams_enabled', bool, None),
    ]
)


class CourseOverviewSchema(BaseCourseOverviewSchema):
    class Config(BaseCourseOverviewSchema.Config):
        arbitrary_types_allowed = True


class CourseSchema(ModelSchema):
    course_overview: CourseOverviewSchema = None

    class Config:
        model = Course
        model_fields = [
            'id'
        ]


class OrganizationSchema(ModelSchema):
    class Config:
        model = Organization
        model_fields = ['uuid', 'title', 'short_name', 'slug', 'description', 'logo', 'image_background', 'status']


class ProgramSchema(ModelSchema):
    owner: OrganizationSchema = None
    courses: List[CourseSchema] = []

    class Config:
        model = Program
        model_fields = ['uuid', 'title', 'short_name', 'slug', 'description', 'number_of_hours', 'logo',
                        'image_background',
                        'edu_start_date', 'edu_end_date', 'issued_document_name', 'enrollment_allowed', 'owner',
                        'courses']


class ProjectSchema(ModelSchema):
    programs: List[ProgramSchema] = []
    owner: OrganizationSchema = None

    class Config:
        model = Project
        model_fields = [
            'title',
            'short_name',
            'slug',
            'owner',
            'description',
            'logo',
            'image_background',
            'active',
            'status',
            'published_at',
        ]


@api.get("/projects", response=List[ProjectSchema])  # description="Creates an order and updates stock"
def projects(request, limit: int = 10, offset: int = 0):
    qs = Project.available_objects.filter(active=True, status='published')
    return qs[offset: offset + limit]


@api.get("/programs", response=List[ProgramSchema])
def programs(request, limit: int = 10, offset: int = 0):
    qs = Program.available_objects.filter(active=True, status='published')
    return qs[offset: offset + limit]


@api.get("/courses", response=List[CourseSchema])
def courses(request, limit: int = 20, offset: int = 0):
    qs = Course.objects.filter(status='published')
    return qs[offset: offset + limit]


@api.post("/enroll", description="Зачисляет пользователя на программу или проект")
def enroll_user_to_program(request, payload: ProgramEnrollmentIn):
    enrollment = ProgramEnrollment.objects.create(**payload.dict())
    return {
        "email": enrollment.user.email,
        "program_uuid": enrollment.program_uuid,
        "project_uuid": enrollment.project_uuid,
        "success": True
    }
