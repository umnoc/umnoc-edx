"""
Database models for umnoc courses module.
"""
import re
from datetime import datetime
from typing import List
from typing import Optional

from django.conf import settings
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

    @staticmethod
    def week_conv(n):
        es = ['неделя', 'недели', 'недель']
        n = n % 100
        if 11 <= n <= 19:
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
        app_label = 'umnoc'
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    course_overview = models.ForeignKey('course_overviews.CourseOverview', db_index=True, related_name='umnoc_courses',
                                        on_delete=models.CASCADE)

    target = models.TextField('Описание направленности и целевого назначения курса', blank=True, null=True)
    description = models.TextField('О курсе, общая информация о курсе', blank=True, null=True)
    course_program = models.TextField('Программа курса', blank=True, null=True)
    min_duration = models.PositiveSmallIntegerField(verbose_name='Длительность изучения курса, мин',
                                                    help_text='недель', default=0)
    max_duration = models.PositiveSmallIntegerField(verbose_name='Длительность изучения курса, макс',
                                                    help_text='Оставьте пустым, если значение точное',
                                                    blank=True, null=True)
    labor = models.PositiveSmallIntegerField('Трудоемкость', default=0,
                                             help_text='Зачётных единиц')
    lectures_count = models.PositiveSmallIntegerField('Количество лекций', default=0)
    prerequisites = models.TextField('Пререквизиты', blank=True, null=True)
    format = models.TextField('Формат обучения', blank=True, null=True)

    STATUS = Choices('draft', 'published')
    status = StatusField(choices_name='STATUS')
    published_at = MonitorField(monitor='status', when=['published'])

    # TODO: Добавить поля паспорта
    # TODO: Написать методы

    def __str__(self) -> str:
        return f'<UMNOC course, ID: {self.course_overview}, title: {self.course_overview.display_name}>'

    @property
    def duration(self) -> str:
        if self.min_duration == 0:
            return ''
        if not self.max_duration or self.max_duration == 0:
            return '{} {}'.format(self.min_duration, self.week_conv(self.min_duration))
        else:
            return '{}-{} {}'.format(self.min_duration, self.max_duration, self.week_conv(self.max_duration))

    @property
    def credits(self) -> str:
        if self.labor > 0:
            return f'{self.labor} з.е.'
        else:
            return ''

    @property
    def start_display(self) -> str:
        return self.course_overview.start_display

    @property
    def display_name(self) -> str:
        return self.course_overview.display_name

    @property
    def course_id(self) -> str:
        return self.course_overview.id

    @property
    def course_image_url(self) -> str:
        return self.course_overview.course_image_url

    @property
    def banner_image_url(self) -> str:
        return self.course_overview.banner_image_url

    @property
    def start_date(self) -> Optional[datetime]:
        return self.course_overview.start_date

    @property
    def end_date(self) -> Optional[datetime]:
        return self.course_overview.end_date

    @property
    def enrollment_start(self) -> Optional[datetime]:
        return self.course_overview.enrollment_start

    @property
    def enrollment_end(self) -> Optional[datetime]:
        return self.course_overview.enrollment_end

    @property
    def invitation_only(self) -> Optional[datetime]:
        return self.course_overview.invitation_only

    @property
    def max_student_enrollments_allowed(self) -> bool:
        return self.course_overview.max_student_enrollments_allowed

    @property
    def short_description(self) -> str:
        return self.course_overview.short_description

    @property
    def course_video_url(self) -> str:
        return self.course_overview.course_video_url

    @property
    def language(self) -> str:
        return self.course_overview.language

    @property
    def pre_requisite_courses(self):
        return self.course_overview.pre_requisite_courses

    @property
    def results(self) -> List[Optional[str]]:
        return self.result_set.values_list('title', flat=True)

    @property
    def competences(self) -> List[Optional[str]]:
        return self.competence_set.values_list('title', flat=True)


class Competence(models.Model):
    title = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('order',)
        verbose_name = 'компетенция'
        verbose_name_plural = 'компетенции'

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args, **kwargs):
        title = re.sub('\s+', ' ', str(self.title))
        self.title = title.strip()
        super(Competence, self).save(*args, **kwargs)


class Result(models.Model):
    title = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('order',)
        verbose_name = 'результат обучения'
        verbose_name_plural = 'результаты обучения'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        title = re.sub('\s+', ' ', str(self.title))
        self.title = title.strip()
        super(Result, self).save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField('ФИО', max_length=255)
    photo = models.ImageField('Фотография')
    description = models.TextField('Краткая справка о регалиях')
    course = models.ForeignKey(Course, related_name='authors', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('order',)
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

    def __str__(self) -> str:
        return str(self.name)

    @property
    def photo_url(self) -> str:
        return f'{settings.LMS_ROOT_URL}{self.photo}'
