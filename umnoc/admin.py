from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

from .core.models import (
    Organization,
    ProgramCourse,
    OrganizationCourse,
    Direction,
    Project,
    Program,
    TextBlock
)
from .courses.models import (Course, Competence, Result, Author)
from .learners.models import (ProgramEnrollment)
from .profiles.models import (Profile, Reflection, Question, Answer)


class UMNOCAdminSite(admin.AdminSite):
    site_header = _('UMNOC administration')


umnoc_admin_site = UMNOCAdminSite(name='umnoc_admin')


# inlines
class OrganizationCourseInline(admin.TabularInline):
    model = OrganizationCourse
    extra = 1
    autocomplete_fields = ['course']


class ProgramCourseInline(admin.TabularInline):
    model = ProgramCourse
    extra = 1
    autocomplete_fields = ['course']


class CompetenceInline(OrderableAdmin, admin.TabularInline):
    model = Competence
    # extra = 1
    autocomplete_fields = ['course']
    ordering_field = "order"
    ordering_field_hide_input = True


class ResultInline(OrderableAdmin, admin.TabularInline):
    model = Result
    # extra = 1
    autocomplete_fields = ['course']
    ordering_field = "order"
    ordering_field_hide_input = True


class AuthorInline(OrderableAdmin, admin.TabularInline):
    model = Author
    # extra = 1
    autocomplete_fields = ['course']
    ordering_field = "order"
    ordering_field_hide_input = True


# modeladmins

@admin.register(CourseOverview, site=umnoc_admin_site)
class CourseOverviewAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search view of Course Overviews.
    """
    list_display = [
        'id',
        'display_name',
        'version',
        'enrollment_start',
        'enrollment_end',
        'created',
        'modified',
    ]

    search_fields = ['id', 'display_name']


@admin.register(Course, site=umnoc_admin_site)
class CourseAdmin(admin.ModelAdmin):
    autocomplete_fields = ['course_overview']
    search_fields = ['course_overview__display_name', 'course_overview__id']
    list_display = ('display_name', 'course_id', 'start_date', 'end_date', 'course_program', 'status')
    fieldsets = (
        (None, {
            'fields': (('course_overview', 'status', 'is_removed', 'published_at'),)
        }),
        ('Numeric fields', {
            'classes': ('collapse',),
            'fields': (('min_duration', 'max_duration'), 'labor', 'lectures_count')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('target', 'description', 'course_program', 'prerequisites', 'format'),
        }),
    )
    inlines = [CompetenceInline, ResultInline, AuthorInline]


@admin.register(Program, site=umnoc_admin_site)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'logo', 'active', 'owner')
    list_filter = ('active', 'owner')
    ordering = ('title',)
    filter_horizontal = ['courses']
    search_fields = ('title', 'short_name', 'slug')
    inlines = [ProgramCourseInline]


@admin.register(Organization, site=umnoc_admin_site)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_name', 'logo', 'active')
    list_filter = ('active',)
    ordering = ('title', 'short_name',)
    search_fields = ('title', 'short_name', 'slug')
    inlines = [OrganizationCourseInline]


@admin.register(ProgramEnrollment, site=umnoc_admin_site)
class ProgramEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'external_user_key', 'program_uuid', 'project_uuid', 'status')
    list_filter = ('status',)
    search_fields = ('user',)
    raw_id_fields = ('user',)
