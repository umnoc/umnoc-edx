"""
Database models for umnoc core.
"""
from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField, MonitorField, UUIDField
from model_utils.models import TimeStampedModel, SoftDeletableModel


class Organization(TimeStampedModel, SoftDeletableModel):
    """
    Организация. Правообладатель курса.
    """
    STATUS = Choices('draft', 'published')

    uuid = UUIDField(version=4, editable=False, unique=True)

    title = models.CharField('Название', blank=False, null=False, max_length=1024)
    short_name = models.CharField('Аббревиатура', null=True, unique=True, max_length=64)
    slug = models.CharField('Человеко-понятный уникальный идентификатор', blank=False, null=False, max_length=64,
                            unique=True)
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

    def __str__(self):
        return self.title

    def get_courses(self):
        return self.organizationcourse_set.all()

    class Meta:
        """ Meta class for this Django model """
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    status = StatusField()
    published_at = MonitorField(monitor='status', when=['published'])

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<Organization, ID: {}>'.format(self.id)


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
    enrollment_allowed = StatusField(choices_name="ENROLLMENT_STATUSES")

    published_at = MonitorField(monitor='status', when=['published'])
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
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(Organization, related_name="programs", blank=True, null=True,
                              on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, related_name="realized_programs", blank=True, null=True,
                                on_delete=models.SET_NULL)
    direction = models.ForeignKey(Direction, blank=True, null=True, on_delete=models.SET_NULL)
    enrollment_allowed = models.CharField("Доступность записи", choices=ENROLLMENT_STATUSES, max_length=1, default="2")
    id_unit_program = models.CharField("Программа ID", blank=True, null=True, max_length=64)
    edu_start_date = models.DateField("Дата начала программы", null=True, blank=True)
    edu_end_date = models.DateField("Дата завершения программы", null=True, blank=True)
    number_of_hours = models.PositiveSmallIntegerField("Количество часов", null=True, blank=True)
    issued_document_name = models.CharField("Выдаваемый Документ", null=True, blank=True, max_length=128)

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

    class Meta:
        verbose_name = "образовательная программа"
        verbose_name_plural = "образовательные программы"

    def __str__(self):
        return self.title

    def export_students(self):
        """TODO: implement method from admin"""
        return None

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<Program, ID: {}>'.format(self.id)


class ProgramCourse(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
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
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return f'<ProgramCourse, ID: {self.id}, Course: {self.course.id}, Program: {self.program.id}>'


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
        return f'<OrganizationCourse, ID: {self.id}, Course: {self.course.id}, Organization: {self.organization.id}>'


class TextBlock(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

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
