"""
Database models for umnoc courses module.
"""
from django.db import models
from model_utils import Choices
from model_utils.models import (
    TimeStampedModel,
    SoftDeletableModel,
    StatusField,
    MonitorField)


class Course(TimeStampedModel, SoftDeletableModel):
    """
        Онлайн-курс. Модель позволяет расширить course_overview.
    """

    def week_conv(self, n):
        es = ['неделя', 'недели', 'недель']
        n = n % 100
        if n >= 11 and n <= 19:
            s = es[2]
        else:
            i = n % 10
            if i == 1:
                s = es[0]
            elif i in [2, 3, 4]:
                s = es[1]
            else:
                s = es[2]
        return s

    class Meta:
        app_label = "umnoc"
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    course_overview = models.ForeignKey('course_overviews.CourseOverview', db_index=True, related_name='umnoc_courses',
                                        on_delete=models.CASCADE)

    title = models.CharField("Название курса", max_length=255)
    target = models.TextField("Описание направленности и целевого назначения курса", blank=True, null=True)
    description = models.TextField("О курсе, общая информация о курсе", blank=True, null=True)
    course_program = models.TextField("Программа курса", blank=True, null=True)
    min_duration = models.PositiveSmallIntegerField(verbose_name="Длительность изучения курса, мин", default=0)
    max_duration = models.PositiveSmallIntegerField(verbose_name="Длительность изучения курса, макс",
                                                    help_text="Оставьте пустым, если значение точное",
                                                    blank=True, null=True)
    labor = models.PositiveSmallIntegerField("Трудоемкость, з.е.", default=0)
    lectures_count = models.PositiveSmallIntegerField("Количество лекций", default=0)
    prerequisites = models.TextField("Пререквизиты", null=True)
    language = models.CharField("Язык курса", max_length=16, default="русский")
    format = models.TextField("Формат обучения", null=True)

    STATUS = Choices('draft', 'published')
    status = StatusField(choices_name="STATUS")
    published_at = MonitorField(monitor='status', when=['published'])

    # TODO: Добавить поля паспорта
    # TODO: Написать методы

    def __str__(self):
        return f'<UMNOC course, ID: {self.course_overview}, title: {self.course_overview.display_name}>'

    @property
    def duration(self):
        if not self.max_duration or self.max_duration == 0:
            return '{} {}'.format(self.min_duration, self.week_conv(self.min_duration))
        else:
            return '{} - {} {}'.format(self.min_duration, self.max_duration, self.week_conv(self.max_duration))


class Competence(models.Model):
    title = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Result(models.Model):
    title = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField("ФИО", max_length=255)
    photo = models.ImageField("Фотография")
    description = models.TextField("Краткая справка о регалиях")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
