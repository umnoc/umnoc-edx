"""
Database models for umnoc core.
"""
import json

import requests
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField, MonitorField, UUIDField
from model_utils.models import TimeStampedModel, SoftDeletableModel
from simple_history.models import HistoricalRecords
from umnoc.courses.models import Course


class Organization(TimeStampedModel, SoftDeletableModel):
    """
    Организация. Правообладатель курса.
    """
    STATUS = Choices('draft', 'published')

    uuid = UUIDField(version=4, editable=False, unique=True)

    title = models.CharField('Название', blank=False, null=True, max_length=1024)
    short_name = models.CharField('Аббревиатура', null=True, unique=True, max_length=64)
    slug = models.CharField('Человеко-понятный уникальный идентификатор', null=True, max_length=64, unique=True)
    description = models.TextField('Описание', blank=True, null=True)
    logo = models.ImageField(
        upload_to='org_logos',
        help_text='Please add only .PNG files for logo images. This logo will be used on Organization logo.',
        null=True, blank=True
    )
    image_background = models.ImageField(
        upload_to='org_background',
        help_text='Please add only .PNG files for background images. This image will be used on Organization background image.',
        null=True, blank=True
    )
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'организация'
        verbose_name_plural = 'организации'

    def get_courses(self):
        return self.organizationcourse_set.all()

    status = StatusField()
    published_at = MonitorField(monitor='status', when=['published'])

    def __str__(self):
        return f'<Organization, title: {self.title}>'


class Direction(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<Direction, ID: {}>'.format(self.id)


class Project(TimeStampedModel, SoftDeletableModel):
    """
    Образовательный проект. Позволяет расширить набор программ
    """

    uuid = UUIDField(primary_key=True, version=4, editable=False)

    title = models.CharField('Название', blank=False, null=False, max_length=1024, default="")
    short_name = models.CharField('Аббревиатура', blank=False, null=False, max_length=64, default="", unique=True)
    slug = models.CharField('Человеко-понятный уникальный идентификатор', blank=False, null=False, max_length=64,
                            default="", unique=True)
    owner = models.ForeignKey('Organization', related_name="projects", blank=True, null=True,
                              on_delete=models.SET_NULL)
    description = models.TextField('Описание', blank=True, null=True)
    logo = models.ImageField(
        upload_to='project_logos',
        help_text='Please add only .PNG files for logo images. This logo will be used on Project logo.',
        null=True, blank=True, max_length=255
    )
    image_background = models.ImageField(
        upload_to='project_background',
        help_text='Please add only .PNG files for background images. This image will be used on Project background image.',
        null=True, blank=True
    )
    active = models.BooleanField(default=True)

    STATUS = Choices('draft', 'published')
    status = StatusField()
    published_at = MonitorField(monitor='status', when=['published'])

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return f'<UMNOC Project, uuid: {self.uuid}, title: {self.title}>'


class Program(TimeStampedModel, SoftDeletableModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    uuid = UUIDField(primary_key=True, version=4, editable=False)

    ENROLLMENT_STATUSES = Choices("Недоступна", "Доступна", "По расписанию")
    STATUS = Choices('draft', 'published')

    enrollment_allowed = StatusField(choices_name="ENROLLMENT_STATUSES")

    title = models.CharField('Наименование', blank=False, null=False, max_length=1024, default="")
    short_name = models.CharField('Аббревиатура', blank=False, null=False, max_length=64, default="", unique=True)
    slug = models.CharField('Человеко-понятный уникальный идентификатор', blank=False, null=False, max_length=64,
                            default="", unique=True)
    description = models.TextField('Описание', blank=True, null=True)
    logo = models.ImageField(
        upload_to='program_logos',
        help_text='Please add only .PNG files for logo images. This logo will be used on Program logo.',
        null=True, blank=True, max_length=255
    )
    image_background = models.ImageField(
        upload_to='program_background',
        help_text='Please add only .PNG files for background images. This image will be used on Program background image.',
        null=True, blank=True
    )

    owner = models.ForeignKey(Organization, related_name="programs", blank=True, null=True,
                              on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, related_name="realized_programs", blank=True, null=True,
                                on_delete=models.SET_NULL)
    direction = models.ForeignKey(Direction, blank=True, null=True, on_delete=models.SET_NULL)
    id_unit_program = models.CharField("UNI UUID", blank=True, null=True, max_length=64)
    edu_start_date = models.DateField("Дата начала программы", null=True, blank=True)
    edu_end_date = models.DateField("Дата завершения программы", null=True, blank=True)
    number_of_hours = models.PositiveSmallIntegerField("Количество часов", null=True, blank=True)
    issued_document_name = models.CharField("Выдаваемый Документ", null=True, blank=True, max_length=128)
    courses = models.ManyToManyField(Course, blank=True)

    active = models.BooleanField(default=True)

    status = StatusField(choices_name="STATUS")
    published_at = MonitorField(monitor='status', when=['published'])

    class Meta:
        verbose_name = "образовательная программа"
        verbose_name_plural = "образовательные программы"

    def get_courses(self):
        return self.programcourse_set.all()

    def content(self):
        return TextBlock.objects.filter(object_id=self.id, content_type__model="Program")

    @classmethod
    def get_program(cls, slug):
        if cls.objects.select_related().filter(slug=slug).exists():
            return cls.objects.select_related().filter(slug=slug).first()
        else:
            return None

    def export_students(self):
        """TODO: implement method from admin"""
        raise NotImplementedError

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return f'<Program, title: {self.title}>'


class ProgramCourse(TimeStampedModel):
    """
    Курс образовательной программы
    """

    class Meta:
        app_label = "umnoc"
        unique_together = (
            ('course', 'program'),
        )

    course = models.ForeignKey('Course', blank=False, null=False, on_delete=models.CASCADE)
    program = models.ForeignKey('Program', blank=False, null=False, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'<ProgramCourse, ID: {self.id}, Course: {self.course}, Program: {self.program}>'


class OrganizationCourse(TimeStampedModel):
    """
    Курс организации
    """

    class Meta:
        app_label = "umnoc"
        unique_together = (
            ('course', 'organization'),
        )

    course = models.ForeignKey('Course', blank=False, null=False, on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', blank=False, null=False, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'<OrganizationCourse, ID: {self.id}, Course: {self.course}, Organization: {self.organization}>'


class TextBlock(TimeStampedModel):
    # TODO: add field definitions

    STATUS = Choices('draft', 'published')
    status = StatusField()
    published_at = MonitorField(monitor='status', when=['published'])

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<TextBlock, ID: {}>'.format(self.id)


class ExternalPlatform(TimeStampedModel):
    """
    Платформа-источник курсов
    """

    title = models.CharField(_('Название'), blank=False, null=False, max_length=255)
    sources_list_url = models.URLField(blank=True, null=True)
    history = HistoricalRecords()

    def get_courses(self):
        # TODO: Implement method
        response = requests.get(self.sources_list_url, verify=False)
        courses = response.json()
        return courses
        # for course_data in courses:
