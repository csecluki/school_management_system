import random

from django.core.management.base import BaseCommand
from timetables.models import Period
from courses.models import Course, CourseGroup


class Command(BaseCommand):
    help = 'Populate the courses_course_group table with sample data'

    def handle(self, *args, **kwargs):
        FIXED_PERIOD = 4

        RANDOMIZER = {
            0: 0.2,
            1: 0.6,
            2: 0.85,
            3: 0.95
        }

        CourseGroup.objects.all().delete()

        period = Period.objects.get(id=FIXED_PERIOD)

        for course in Course.objects.all():
            course_counter = 0
            while random.random() > RANDOMIZER.get(course_counter, 1):
                CourseGroup.objects.create(
                    course=course,
                    period=period
                )
                course_counter += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created CourseGroup instances. '))
