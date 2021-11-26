from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .core.models import (Organization, Direction, Project, TextBlock)
from .courses.models import (Course, ProgramCourse, OrganizationCourse)
from .learners.models import (ProgramEnrollment)
from .profiles.models import (Profile, Reflection, Question, Answer)


class UMNOCAdminSite(admin.AdminSite):
    site_header = _('UMNOC administration')


umnoc_admin_site = UMNOCAdminSite(name='umnoc_admin')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass
