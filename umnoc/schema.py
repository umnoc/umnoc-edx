import logging
from datetime import date
from typing import List, Any

from common.djangoapps.student.models import UserProfile
from django.contrib.auth.models import User
from ninja import ModelSchema, Schema
from ninja.orm import create_schema
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.core.djangoapps.models.course_details import CourseDetails

from .core.models import Program, Project, Organization
from .courses.models import Course, Author, Competence, Result, LikedCourse
from .profiles.models import Role, UrFUProfile

log = logging.getLogger(__name__)


class RoleSchema(ModelSchema):
    class Config:
        model = Role
        model_fields = ['title']


class UrFUProfileSchema(ModelSchema):
    roles: List[str]
    class Config:
        model = UrFUProfile

        model_fields = [
            'last_name',
            'first_name',
            'second_name',
            'phone',
            'SNILS',
            'specialty',
            'country',
            'education_level',
            'job',
            'position',
            'birth_date',
            'roles'
        ]

    @staticmethod
    def resolve_roles(obj):
        return [role.title for role in obj.roles.all()]


class LikedCourseSchema(ModelSchema):
    class Config:
        model = LikedCourse
        model_fields = ['course', 'user']


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['username', 'email', 'is_staff', 'is_active']


UserProfileSchema = create_schema(
    UserProfile,
    fields=[
        'name',
        'year_of_birth',
        'mailing_address',
        'city',
        'goals',
        'allow_certificate',
        'bio',
        'phone_number',
    ],
    custom_fields=[
        ('user', UserSchema, None),
        ('has_profile_image', bool, False),
        ('age', int, None),
        ('level_of_education_display', str, None),
        ('gender_display', str, None),
        ('country', Any, None)
    ]
)


class UserIn(Schema):
    id: str = None
    username: str = None
    email: int = None


class ProgramEnrollmentIn(Schema):
    user: UserIn
    program_uuid: str = None
    project_uuid: str = None


class LikedCourseIn(Schema):
    username: str = None
    course_id: str = None


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


AuthorSchema = create_schema(
    Author,
    fields=[
        'name',
        'description'
    ],
    custom_fields=[
        ('photo_url', str, None)
    ]
)


class CompetenceSchema(ModelSchema):
    class Config:
        model = Competence
        model_fields = ["title"]


class ResultSchema(ModelSchema):
    class Config:
        model = Result
        model_fields = ["title"]


class CourseOverviewProxy(CourseOverview):
    @property
    def description(self):
        return CourseDetails.fetch_about_attribute(self.id, 'description')


BaseCourseOverviewSchema = create_schema(
    CourseOverviewProxy,
    fields=[
        'id',
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
        # ('id', CourseKeySchema, None),
        ('number', str, None),
        ('description', str, 'Not implemented'),
        ('url_name', str, None),
        ('display_name_with_default', str, None),
        ('dashboard_start_display', date, None),
        ('start_type', str, 'empty'),
        ('start_display', str, None),
        ('pre_requisite_courses', List[CourseKeySchema], []),
        ('tabs', List[CourseTabSchema], []),
        ('image_urls', dict, None),
        ('pacing', str, None),
        ('textbooks', List[TextbookSchema], []),
        ('pdf_textbooks', List[TextbookSchema], []),
        ('html_textbooks', List[TextbookSchema], []),
        ('course_visibility', str, None),
    ]
)


class CourseOverviewSchema(BaseCourseOverviewSchema):
    id: Any

    class Config(BaseCourseOverviewSchema.Config):
        arbitrary_types_allowed = True


CourseSchema = create_schema(
    Course,
    depth=2,
    fields=[
        'id',
        'target',
        'description',
        'course_program',
        'lectures_count',
        'prerequisites',
        'format',
    ],
    custom_fields=[
        ('course_id', Any, None),
        ('display_name', str, None),
        ('organization', str, None),
        ('course_image_url', str, None),
        ('banner_image_url', str, None),
        ('course_video_url', str, None),
        ('short_description', str, None),
        ('duration', str, None),
        ('credits', str, None),
        ('start_display', str, None),
        ('start_date', Any, None),
        ('end_date', str, None),
        ('enrollment_start', str, None),
        ('enrollment_end', str, None),
        ('invitation_only', bool, None),
        ('max_student_enrollments_allowed', str, None),
        ('language', str, None),
        ('pre_requisite_courses', List[Any], []),
        ('authors', List[AuthorSchema], []),
        ('competences', List[str], []),
        ('results', List[str], []),
        ('course_program_html', str, None),
        # ('course_overview', CourseOverviewSchema, None),
    ]

)


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
