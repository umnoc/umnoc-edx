"""
Database models for umnoc courses module.
"""
import re
from datetime import datetime
from typing import List
from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_clone.models import CloneModel
from model_utils import Choices
from model_utils.models import (
    TimeStampedModel,
    SoftDeletableModel,
    StatusField,
    MonitorField)
from simple_history.models import HistoricalRecords

from umnoc.utils import rough_search


class Course(CloneModel, TimeStampedModel, SoftDeletableModel):
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

    external = models.BooleanField(_('External course'), default=False)

    course_overview = models.ForeignKey('course_overviews.CourseOverview', related_name='umnoc_course', blank=True,
                                        null=True, on_delete=models.CASCADE)

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

    # external course addition fields
    course_image_url_f = models.URLField(_('External course image url'), blank=True, null=True)
    start_display_f = models.CharField(_('Start date for display'), max_length=32, blank=True, null=True)
    start_date_f = models.DateTimeField(_('External course start date'), blank=True, null=True)
    end_date_f = models.DateTimeField(_('External course end date'), blank=True, null=True)
    lang = models.CharField(_('Language'), max_length=32, blank=True, null=True)
    display_name_f = models.CharField(_('External display name'), max_length=255, blank=True, null=True)
    organization_f = models.CharField(_('External organization name'), max_length=255, blank=True, null=True)

    history = HistoricalRecords(excluded_fields=['status', 'published_at'])
    STATUS = Choices('draft', 'published')
    status = StatusField(choices_name='STATUS')
    published_at = MonitorField(monitor='status', when=['published'])
    
    enrollment_allowed = models.BooleanField("Доступна запись", default=False)

    # TODO: Добавить поля паспорта
    # TODO: Написать методы

    def __str__(self) -> str:
        if not self.external:
            return f'<UMNOC course, ID: {self.course_overview}, title: {self.course_overview.display_name}>'
        else:
            return f'<External UMNOC course, title: {self.display_name_f}>'

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
        if not self.external:
            return self.course_overview.start_display
        else:
            return self.start_display_f

    @property
    def organization(self) -> str:
        if not self.external:
            return self.course_overview.display_org_with_default
        else:
            return self.organization_f

    @property
    def display_name(self) -> str:
        if not self.external:
            return self.course_overview.display_name
        else:
            return self.display_name_f

    @property
    def course_id(self) -> str:
        if not self.external:
            return self.course_overview.id
        else:
            return f"{self.id}"

    @property
    def course_image_url(self) -> str:
        if not self.external:
            return f'{settings.LMS_ROOT_URL}{self.course_overview.course_image_url}'
        else:
            return self.course_image_url_f

    @property
    def banner_image_url(self) -> str:
        if not self.external:
            return f'{settings.LMS_ROOT_URL}{self.course_overview.banner_image_url}'
        else:
            return self.course_image_url_f

    @property
    def start_date(self) -> Optional[datetime]:
        if not self.external:
            return self.course_overview.start_date
        else:
            return self.start_date_f

    @property
    def end_date(self) -> Optional[datetime]:
        if not self.external:
            return self.course_overview.end_date
        else:
            return self.end_date_f

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
        if not self.external:
            return self.course_overview.short_description
        else:
            return ''

    @property
    def course_video_url(self) -> str:
        if not self.external:
            return self.course_overview.course_video_url
        else:
            return ''

    @property
    def language(self) -> str:
        if not self.external:
            return self.course_overview.language
        else:
            return self.lang

    @property
    def pre_requisite_courses(self):
        return self.course_overview.pre_requisite_courses

    @property
    def results(self) -> List[Optional[str]]:
        return self.result_set.values_list('title', flat=True)

    @property
    def competences(self) -> List[Optional[str]]:
        return self.competence_set.values_list('title', flat=True)

    @property
    def course_program_html(self) -> str:
        lines = self.course_program.split('\r\n')
        return f"<p>{'</p><p>'.join(lines)}</p>"

    @classmethod
    def create_or_update_external(cls, ext_course):
        display_name = rough_search(ext_course, 'display_name')
        target = ext_course.get('target', None)
        description = ext_course.get('description', None)
        course_program = ext_course.get('course_program', None)
        min_duration = ext_course.get('min_duration', 0)
        max_duration = ext_course.get('max_duration', None)
        labor = ext_course.get('labor', 0)
        lectures_count = ext_course.get('lectures_count', 0)
        prerequisites = ext_course.get('prerequisites', None)
        _format = ext_course.get('format', None)
        lang = ext_course.get('lang', None)
        course_image_url_f = ext_course.get('course_image_url', None)
        start_display_f = ext_course.get('startdate', None)
        start_date_f = ext_course.get('startdate', None)
        end_date_f = ext_course.get('enddate', None)

        existing_course = cls.objects.filter(display_name_f=display_name, external=True)

        if existing_course.exists():
            existing_course = existing_course.first()
            existing_course.display_name_f = display_name
            existing_course.target = target
            existing_course.description = description
            existing_course.course_program = course_program
            existing_course.min_duration = min_duration
            existing_course.max_duration = max_duration
            existing_course.labor = labor
            existing_course.lectures_count = lectures_count
            existing_course.prerequisites = prerequisites
            existing_course.format = _format
            existing_course.lang = lang
            existing_course.course_image_url_f = course_image_url_f
            existing_course.start_display_f = start_display_f
            existing_course.start_date_f = start_date_f
            existing_course.end_date_f = end_date_f
            existing_course.save()
        else:
            existing_course = cls.objects.create(display_name_f=display_name,
                                                 target=target,
                                                 description=description,
                                                 course_program=course_program,
                                                 min_duration=min_duration,
                                                 max_duration=max_duration,
                                                 labor=labor,
                                                 lectures_count=lectures_count,
                                                 prerequisites=prerequisites,
                                                 format=_format,
                                                 lang=lang,
                                                 course_image_url_f=course_image_url_f,
                                                 start_display_f=start_display_f,
                                                 start_date_f=start_date_f,
                                                 end_date_f=end_date_f,
                                                 external=True
                                                 )
        return existing_course

        """
          create authors; competences; results objects, bind with course
        """


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
        return f'{settings.LMS_ROOT_URL}{settings.MEDIA_URL}{self.photo}'


class LikedCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user) + str(self.course)

    @classmethod
    def create(cls, username, course_id):
        user = get_user_model().objects.get(username=username)
        course = Course.objects.get(pk=course_id)
        obj = cls.objects.create(user=user, course=course)
        return obj
