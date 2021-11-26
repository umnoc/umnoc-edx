"""
Database models for umnoc courses module.
"""
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

from umnoc.core.models import Program


class Course(TimeStampedModel, StatusModel):
    """
        TODO: replace with a brief description of the model.

        TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
        information, see OEP-30:
        https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
        """

    class Meta:
        app_label = "umnoc"

    course_overview = models.ForeignKey(CourseOverview, db_index=True, related_name="umnoc_courses", on_delete=models.CASCADE)

    STATUS = Choices('draft', 'published')

    # TODO: Добавить поля паспорта
    # TODO: Написать методы

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return f'<UMNOC course, ID: {self.course_overview}, title: {self.course_overview.display_name}>'


