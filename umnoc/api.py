from datetime import date
from typing import List, Dict

import orjson
from lms.djangoapps.courseware.tabs import (
    CourseInfoTab,
    CourseTab
)
from ninja import NinjaAPI, ModelSchema, Schema
from ninja.orm import create_schema
from ninja.renderers import BaseRenderer
from opaque_keys.edx.keys import UsageKey, CourseKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from xmodule.course_module import Textbook
from xmodule.tabs import CourseTab

from .core.models import Program, Project, Organization
from .courses.models import Course


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def default(self, obj):
        if isinstance(obj, CourseTab):
            return obj.title

    def render(self, request, data, *, response_status):
        return orjson.dumps(data, default=self.default)


api = NinjaAPI(renderer=ORJSONRenderer())

BaseCourseOverviewSchema = create_schema(
    CourseOverview,
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
        ('number', str, None),
        ('url_name', str, None),
        ('display_name_with_default', str, None),
        ('display_name_with_default_escaped', str, None),
        ('dashboard_start_display', date, None),
        ('start_date_is_still_default', bool, True),
        ('sorting_score', int, None),
        ('start_type', str, 'empty'),
        ('start_display', str, None),
        ('pre_requisite_courses', str, None),
        ('tabs', str, None),
        ('image_urls', dict, None),
        ('pacing', str, None),
        ('closest_released_language', str, None),
        ('allow_public_wiki_access', bool, None),
        ('textbooks', List[Dict[str, str]], None),
        ('pdf_textbooks', List[Dict[str, str]], None),
        ('html_textbooks', List[Dict[str, str]], None),
        ('course_visibility', str, None),
        ('teams_enabled', bool, None),

    ]

)


class CourseOverviewSchema(BaseCourseOverviewSchema):
    pre_requisite_courses: List[CourseKey] = []
    tabs: List[CourseTab] = []

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

    class Config:
        model = Program
        model_fields = ['uuid', 'title', 'short_name', 'slug', 'description', 'number_of_hours', 'logo',
                        'image_background',
                        'edu_start_date', 'edu_end_date', 'issued_document_name', 'enrollment_allowed', 'owner']


@api.get("/programs", response=List[ProgramSchema])
def programs(request, limit: int = 10, offset: int = 0):
    qs = Program.available_objects.filter(active=True, status='published')
    return qs[offset: offset + limit]


@api.get("/courses", response=List[CourseSchema])
def courses(request, limit: int = 20, offset: int = 0):
    qs = Course.objects.filter(status='published')
    return qs[offset: offset + limit]
