from admin_ordering.admin import OrderableAdmin
from common.djangoapps.student.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from model_clone import CloneModelAdmin

from .core.models import (
    Organization,
    ProgramCourse,
    OrganizationCourse,
    Program
)
from .courses.models import (Course, Competence, Result, Author, LikedCourse)
from .learners.models import (ProgramEnrollment)
from .profiles.models import (Role, UrFUProfile, LeadRequest)


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
class CourseAdmin(CloneModelAdmin):
    autocomplete_fields = ['course_overview']
    search_fields = ['course_overview__display_name', 'course_overview__id']
    list_display = ('display_name', 'course_id', 'start_date', 'end_date', 'course_program', 'status')
    fieldsets = (
        (None, {
            'fields': (('course_overview', 'status', 'is_removed'), 'published_at')
        }),
        ('Численная информация', {
            'classes': ('wide',),
            'fields': (('min_duration', 'max_duration'), 'labor', 'lectures_count')
        }),
        ('Текстовая информация', {
            'classes': ('wide',),
            'fields': ('target', 'description', 'course_program', 'prerequisites', 'format'),
        }),
    )
    inlines = [CompetenceInline, ResultInline, AuthorInline]

    include_duplicate_action = True
    include_duplicate_object_link = True


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


@admin.register(Role, site=umnoc_admin_site)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(UrFUProfile, site=umnoc_admin_site)
class UrFUProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'SNILS', 'specialty', 'country',
        'education_level', 'job',
        'position', 'birth_date'
    )
    filter_horizontal = ('roles',)
    # list_filter = ('type',)


@admin.register(LeadRequest, site=umnoc_admin_site)
class LeadRequestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'method', 'title', 'name', 'last_name', 'status_id', 'email', 'phone', 'status', 'created')
    readonly_fields = ('method', 'title', 'name', 'second_name', 'last_name', 'status_id', 'email', 'phone', 'status')
    list_filter = ('status',)


def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


make_active.short_description = 'Активировать учетки'

User = get_user_model()

try:
    admin.site.unregister(User)
except NotRegistered:
    pass


@admin.register(User, site=umnoc_admin_site)
class UserAdmin(BaseUserAdmin):
    actions = (make_active,)
    list_display = BaseUserAdmin.list_display + ('is_active', 'date_joined')
    save_on_top = True

    # search_fields = BaseUserAdmin.search_fields

    def get_ordering(self, request):
        return ['-date_joined']


@admin.register(LikedCourse, site=umnoc_admin_site)
class LikedCourseAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
