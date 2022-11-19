import logging

from common.djangoapps.student.models import (
    CourseEnrollment
)
from openedx.core.djangoapps.enrollments.serializers import CourseEnrollmentSerializer

log = logging.getLogger(__name__)


def get_course_enrollments(username, include_inactive=False):
    enrollments = []
    qset = CourseEnrollment.objects.filter(
        user__username=username,
    ).order_by('created')

    if not include_inactive:
        qset = qset.filter(is_active=True)

    for enrollment in qset:
        umnoc_course = enrollment.course.umnoc_course.first()
        enrollments.append({
            "id": umnoc_course.id if umnoc_course else None,
            'course_id': enrollment.course.id,
            'display_name': enrollment.course.display_name,
            'start_date': enrollment.course.start_date,
            'end_date': enrollment.course.end_date,
        })

    return enrollments
