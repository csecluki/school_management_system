import random

from django.core.management.base import BaseCommand
from timetables.models import GroupTimeTable, LessonUnit, Period
from courses.models import Course


class Command(BaseCommand):
    help = 'Populate the schedules_class_schedule table with sample data'

    def handle(self, *args, **kwargs):
        GroupTimeTable.objects.all().delete()

        period = Period.objects.get(id=10)
        lesson_units = LessonUnit.objects.all()

        for course in Course.objects.all():
            GroupTimeTable.objects.create(
                day_of_week=random.choice(GroupTimeTable.WEEK_DAYS)[0],
                course=course,
                lesson_unit = random.choice(lesson_units),
                period=period
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created ClassSchedule instances. '))
