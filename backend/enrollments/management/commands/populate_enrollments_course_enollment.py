import random

from django.core.management.base import BaseCommand

from courses.models import Course
from enrollments.models import GroupEnrollment


class Command(BaseCommand):
    help = 'Populate the enrollments_group_enrollment table with sample data'

    def handle(self, *args, **kwargs):

        courses = Course.objects.all()

        for course in courses:
            GroupEnrollment.objects.get_or_create(
                course
            )
            self.stdout.write(self.style.SUCCESS(f'Course {subject_name} created. '))
