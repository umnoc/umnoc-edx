from datetime import date
from typing import List

from ninja import ModelSchema
from ninja import NinjaAPI
from ninja import Schema

from .core.models import Program, Project, Organization
from .courses.models import Course

api = NinjaAPI()


class CourseSchema(ModelSchema):
    class Config:
        model: Course
        model_fields = [
            'course_overview__id',
            'course_overview__display_name',
            'course_overview__start_date',
            'course_overview__end_date',
            'course_overview__banner_image_url',
            'course_overview__course_image_url',
            'course_overview__lowest_passing_grade',
            'course_overview__enrollment_start',
            'course_overview__enrollment_end',
            'course_overview__invitation_only',
            'course_overview__max_student_enrollments_allowed',
            'course_overview__catalog_visibility',
            'course_overview__short_description',
            'course_overview__course_video_url',
            'course_overview__effort',
            'course_overview__language',
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
    qs = Program.objects.filter(active=True, status='published')
    return qs
