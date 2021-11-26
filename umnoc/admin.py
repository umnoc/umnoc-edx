from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .core.models import (
    Organization,
    ProgramCourse,
    OrganizationCourse,
    Direction,
    Project,
    TextBlock
)
from .courses.models import (Course)
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


# modeladmins

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    autocomplete_fields = ['course_overview']
    # search_fields = ['course_overview']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_name', 'logo', 'active',)
    list_filter = ('active',)
    ordering = ('title', 'short_name',)
    search_fields = ('title', 'short_name', 'slug')
    inlines = [OrganizationCourseInline]
