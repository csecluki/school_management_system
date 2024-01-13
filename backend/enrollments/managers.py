from django.db import models
from django.db.models import Q
from django.utils import timezone


class EnrollmentManager(models.Manager):

    def get_active(self):
        now = timezone.now()
        return self.filter(
            phases__decision_deadline__gte=now,
            phases__start_date__lte=now
        ).distinct()

    def get_applicable(self):
        now = timezone.now()
        return self.filter(
            phases__application_deadline__gte=now,
            phases__start_date__lte=now
        ).distinct()


class EnrollmentPhaseManager(models.Manager):

    def get_active(self):
        now = timezone.now()
        return self.filter(Q(decision_deadline__gte=now) & Q(start_date__lte=now))

    def get_applicable(self):
        now = timezone.now()
        return self.filter(Q(phases__application_deadline__gte=now) & Q(start_date__lte=now))


class GroupEnrollmentManager(models.Manager):

    def get_open(self):
        return self.filter(status=1)


class StudentEnrollmentManager(models.Manager):

    def has_student_pending_request_to_group(self, student, group_enrollment):
        return self.filter(
            student=student,
            group_enrollment=group_enrollment,
            status=0
        ).exists()
