"""
Database models for umnoc courses module.
"""
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel, SoftDeletableModel

from umnoc.core.models import Program


class Course(TimeStampedModel, SoftDeletableModel):
    """
        Онлайн-курс. Модель позволяет расширить course_overview.
    """

    class Meta:
        app_label = "umnoc"
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    course_overview = models.ForeignKey('course_overviews.CourseOverview', db_index=True, related_name='umnoc_courses',
                                        on_delete=models.CASCADE)

    STATUS = Choices('draft', 'published')
    status = StatusField(choices_name="STATUS")
    published_at = MonitorField(monitor='status', when=['published'])

    # TODO: Добавить поля паспорта
    # TODO: Написать методы

    def __str__(self):
        return f'<UMNOC course, ID: {self.course_overview}, title: {self.course_overview.display_name}>'
