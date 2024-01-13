import logging

from celery import shared_task
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import EnrollmentPhase


logger = logging.getLogger(__name__)


@shared_task
def enrollment_start_date():
    logger.info(f'Checking if any EnrollmentPhase reached start_date. ')
    now = timezone.now()
    enrollment_phases = EnrollmentPhase.objects.filter(
        start_date__gte=now - timezone.timedelta(minutes=1),
        start_date__lte=now
    )
    logger.info(f"Found {enrollment_phases.count()} enrollment phases with start_date. ")
    for phase in enrollment_phases:
        for group_enrollment in phase.enrollment.group_enrollments.filter(status__in=[0, 1]):
            try:
                group_enrollment.open()
            except ValidationError:
                continue
    return {'status': 'success'}


@shared_task
def application_deadline():
    logger.info(f'Checking if any EnrollmentPhase reached application_deadline. ')
    now = timezone.now()
    enrollment_phases = EnrollmentPhase.objects.filter(
        application_deadline__gte=now - timezone.timedelta(minutes=1),
        application_deadline__lte=now
    )
    logger.info(f"Found {enrollment_phases.count()} enrollment phases with application_deadline. ")
    for phase in enrollment_phases:
        for group_enrollment in phase.enrollment.group_enrollments.filter(status=1):
            group_enrollment.resolve()
    return {'status': 'success'}


@shared_task
def decision_deadline():
    logger.info(f'Checking if any EnrollmentPhase reached decision_deadline. ')
    now = timezone.now()
    enrollment_phases = EnrollmentPhase.objects.filter(
        decision_deadline__gte=now - timezone.timedelta(minutes=1),
        decision_deadline__lte=now
    )
    logger.info(f"Found {enrollment_phases.count()} enrollment phases with decision_deadline. ")
    for phase in enrollment_phases:
        for group_enrollment in phase.enrollment.group_enrollments.filter(status=1):
            group_enrollment.close(phase.is_last)
    return {'status': 'success'}


@shared_task
def dupa():
    logger.info('Dupa')
