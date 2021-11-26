from datetime import date
from typing import List

from ninja import ModelSchema
from ninja import NinjaAPI
from ninja import Schema
from ninja.orm import create_schema
from opaque_keys.edx.keys import UsageKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

from .core.models import Program, Project, Organization
from .courses.models import Course

api = NinjaAPI()

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
        # ('start_date_is_still_default', str, None),
        # ('sorting_score', str, None),
        # ('start_type', str, None),
        # ('start_display', str, None),
        # ('pre_requisite_courses', str, None),
        # ('tabs', str, None),
        # ('image_urls', str, None),
        # ('pacing', str, None),
        # ('closest_released_language', str, None),
        # ('allow_public_wiki_access', str, None),
        # ('textbooks', str, None),
        # ('pdf_textbooks', str, None),
        # ('html_textbooks', str, None),
        # ('hide_progress_tab', str, None),
        # ('edxnotes', str, None),
        # ('enable_ccx', str, None),
        # ('course_visibility', str, None),
        # ('teams_enabled', str, None),
        # ('show_calculator', bool, False),
        # ('edxnotes_visibility', bool, False),
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

    class Config:
        model = Program
        model_fields = ['uuid', 'title', 'short_name', 'slug', 'description', 'number_of_hours', 'logo',
                        'image_background',
                        'edu_start_date', 'edu_end_date', 'issued_document_name', 'enrollment_allowed', 'owner']


@api.get("/programs", response=List[ProgramSchema])
def programs(request):
    qs = Program.available_objects.filter(active=True, status='published')
    return qs


@api.get("/courses", response=List[CourseSchema])
def courses(request):
    qs = Course.objects.filter(status='published')
    return qs
