"""
Database models for umnoc_edx courses module.
"""
from django.db import models
from model_utils.models import TimeStampedModel, StatusModel
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

from umnoc_edx.core.models import Program


class Course(TimeStampedModel, StatusModel):
    """
        TODO: replace with a brief description of the model.

        TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
        information, see OEP-30:
        https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
        """

    class Meta:
        app_label = "umnoc_edx"

    course_overview = models.ForeignKey(CourseOverview, db_index=True, related_name="tab_set", on_delete=models.CASCADE)

    # TODO: Добавить поля паспорта
    # TODO: Написать методы

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return f'<Course, ID: {self.course_overview}>'


class ProgramCourse(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    class Meta:
        app_label = "umnoc_edx"
        unique_together = (
            ('course', 'program'),
        )

    course = models.ForeignKey(Course, blank=False, null=False, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, blank=False, null=False, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return f'<ProgramCourse, ID: {self.id}, Course: {self.course.id}, Program: {self.program.id}>'


class OrganizationCourse(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    class Meta:
        app_label = "umnoc_edx"
        unique_together = (
            ('course', 'organization'),
        )

    course = models.ForeignKey(Course, blank=False, null=False, on_delete=models.CASCADE)
    organization = models.ForeignKey(Program, blank=False, null=False, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return f'<OrganizationCourse, ID: {self.id}, Course: {self.course.id}, Organization: {self.organization.id}>'
