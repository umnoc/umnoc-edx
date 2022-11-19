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

    for course in qset:
        enrollments.append({
            "id": course.id,
            'course_id': course.id,
            'display_name': course.display_name,
            'start_date': course.start_date,
            'end_date': course.end_date,
        })

    return enrollments
