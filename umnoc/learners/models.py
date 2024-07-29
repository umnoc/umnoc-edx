"""
Database models for umnoc.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords
from user_util import user_util

from ..constants import EnrollmentStatuses


class LearningRequest(TimeStampedModel):
    """Заявка на обучение"""

    STATUS_CHOICES = EnrollmentStatuses.__MODEL_CHOICES__

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="learning_requests",
    )
    course_id = models.PositiveSmallIntegerField()

    last_name = models.CharField("Фамилия", max_length=255, null=False, blank=False)
    first_name = models.CharField("Имя", max_length=255, null=False, blank=False)
    second_name = models.CharField("Отчество", max_length=255, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=255, null=False, blank=False)

    SNILS = models.CharField("Номер СНИЛС", max_length=255, null=True, blank=True)
    specialty = models.CharField(
        "Специальность (направление подготовки)", max_length=355, null=True, blank=True
    )
    country = models.CharField("Гражданство", max_length=255, null=True, blank=True)
    education_level = models.CharField("Уровень базового образования", max_length=255)
    job = models.CharField("Место работы", max_length=2048, null=True, blank=True)
    position = models.CharField("Должность", max_length=2048, null=True, blank=True)
    birth_date = models.CharField("Дата рождения", max_length=16, null=True, blank=True)

    status = models.CharField(max_length=9, default="pending", choices=STATUS_CHOICES)
    historical_records = HistoricalRecords()

    class Meta:
        app_label = "umnoc"
        # unique_together = (
        #     ('user', 'course_id'),
        # )

    def __str__(self):
        return f"<LearningRequest, ID: {self.id}>"


class ProgramEnrollment(TimeStampedModel):
    """
    This is a model for Program Enrollments from the registrar service
    .. pii: PII is found in the external key for a program enrollment
    .. pii_types: other
    .. pii_retirement: local_api
    """

    STATUS_CHOICES = EnrollmentStatuses.__MODEL_CHOICES__

    class Meta:
        app_label = "umnoc"

        # A student enrolled in a given (program, project) should always
        # have a non-null ``user`` or ``external_user_key`` field (or both).
        unique_together = (
            ("user", "program_uuid", "project_uuid"),
            ("external_user_key", "program_uuid", "project_uuid"),
        )

    user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="umnoc_programs",
    )
    external_user_key = models.CharField(db_index=True, max_length=255, null=True)
    program_uuid = models.UUIDField(db_index=True, null=False)
    project_uuid = models.UUIDField(db_index=True, null=False)
    status = models.CharField(max_length=9, default="pending", choices=STATUS_CHOICES)
    historical_records = HistoricalRecords()

    def clean(self):
        if not (self.user or self.external_user_key):
            raise ValidationError(
                _("One of user or external_user_key must not be null.")
            )

    @classmethod
    def retire_user(cls, user_id):
        """
        With the parameter user_id, retire the external_user_key field
        Return True if there is data that was retired
        Return False if there is no matching data
        """

        enrollments = cls.objects.filter(user=user_id)
        if not enrollments:
            return False

        for enrollment in enrollments:
            retired_external_key = user_util.get_retired_external_key(
                enrollment.external_user_key,
                settings.RETIRED_USER_SALTS,
            )
            enrollment.historical_records.update(external_user_key=retired_external_key)
            enrollment.external_user_key = retired_external_key
            enrollment.save()

        return True

    def __str__(self):
        return f"<ProgrammEnrollment, ID: {self.id}>"

    def __repr__(self):
        return (  # lint-amnesty, pylint: disable=missing-format-attribute
            "<ProgramEnrollment"  # pylint: disable=missing-format-attribute
            " id={self.id}"
            " user={self.user!r}"
            " external_user_key={self.external_user_key!r}"
            " program_uuid={self.program_uuid!r}"
            " curriculum_uuid={self.curriculum_uuid!r}"
            " status={self.status!r}"
            ">"
        ).format(self=self)
