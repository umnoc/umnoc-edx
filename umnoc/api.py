from datetime import date
from typing import List

from ninja import ModelSchema
from ninja import NinjaAPI
from ninja import Schema
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

from .core.models import Program, Project, Organization
from .courses.models import Course

api = NinjaAPI()


class CourseOverviewSchema(ModelSchema):
    class Config:
        model = CourseOverview
        model_fields = [
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
        ]


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
